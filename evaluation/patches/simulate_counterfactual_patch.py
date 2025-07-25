def simulate_counterfactual(manager, assumptions, axioms, base_branch="main"):
    if base_branch not in manager.branches:
        raise ValueError(f"Base branch '{base_branch}' not found.")
    base_state = manager.branches[base_branch]
    fork = manager.create_branch(base_state, from_expr="modal simulation")

    queue = []
    for assumption in assumptions:
        fork = fork.add(assumption, source="⟦counterfactual⟧", rule="modal injection", manager=manager) or fork
        queue.append(assumption)

    while queue:
        current = queue.pop(0)
        for axiom in axioms:
            if axiom.pattern.functor == "∨":
                negated, consequence = axiom.pattern.args
                if negated.functor == "¬":
                    original = negated.args[0]
                    substitution = unify(original, current)
                    if substitution:
                        result_expr = substitute_expr(consequence, substitution)
                        if not fork.has(result_expr):
                            new_fork = fork.add(result_expr, source=str(current), rule=axiom.rule_name, manager=manager)
                            if new_fork is not None:
                                fork = new_fork
                                queue.append(result_expr)
    return fork