def prove(goal, facts, axioms, log_json=False, log_md=False, log_path_json="proof_trace.json", log_path_md="proof_trace.md"):
    from .evaluate import LogicEvaluator
    from .quantifier_engine import Quantifier
    from .unifier import match

    evaluator = LogicEvaluator()
    evaluator.context['x'] = ['a', 'b', 'c']  # default domain for demo

    trace = []
    derived_facts = set(facts)

    if goal in derived_facts:
        trace.append(f"→ Goal {goal} already known.")
        result = True
    else:
        result = False
        for axiom in axioms:
            for fact in derived_facts:
                subs = match(axiom, f"¬{fact} ∨ {goal}")
                if subs:
                    instantiated = axiom
                    for var, val in subs.items():
                        instantiated = instantiated.replace(var, val)
                    eval_result = evaluator.evaluate(instantiated)
                    trace.append(f"Given fact: {fact}")
                    trace.append(f"Axiom A1: {axiom}")
                    trace.append(f"Substitution: {subs}")
                    trace.append(f"Instantiated: {instantiated}")
                    trace.append(f"Truth Eval: {eval_result}")
                    if eval_result:
                        trace.append(f"→ Derived {goal} via disjunctive syllogism on A1")
                        result = True
                    else:
                        trace.append(f"✖ Axiom instantiation did not evaluate to true")
                    break
            if result:
                break
        if not result:
            trace.append(f"✖ Could not derive {goal}")

    if log_json:
        import json
        json_trace = {
            "goal": goal,
            "result": result,
            "trace": trace
        }
        with open(log_path_json, "w", encoding="utf-8") as f:
            json.dump(json_trace, f, indent=2)

    if log_md:
        md_trace = f"# Proof Trace – Goal: {goal}\n\n"
        md_trace += f"**Result**: {'✅ Proven' if result else '❌ Not Proven'}\n\n"
        md_trace += "## Trace\n\n"
        for line in trace:
            md_trace += f"- {line}\n"
        with open(log_path_md, "w", encoding="utf-8") as f:
            f.write(md_trace)

    for line in trace:
        print(line)
    return result
