from evaluation.unifier import unify
from evaluation.utils_expr import substitute_expr
from evaluation.logic_truth import evaluate_truth

class BranchManager:
    def __init__(self):
        self.branches = {}  # branch_id: ProofState
        self.counter = 1  # for unique names

    def create_branch(self, parent_state, from_expr):
        new_id = f"{parent_state.branch}_{self.counter}"
        self.counter += 1
        new_state = ProofState(branch=new_id)
        new_state.trace.append(f"↳ Forked from '{parent_state.branch}' (phase {parent_state.phase}) due to contradiction with {from_expr}")
        self.branches[new_id] = new_state
        return new_state
    
    def to_proof_chain(self):
        branches = []
        for branch_id, state in self.branches.items():
            b = ProofBranch(branch_id, state.phase)
            for trace_entry in state.trace:
                if "→ Derived" in trace_entry:
                    parts = trace_entry.split("→ Derived ")[1]
                    parts = parts.split(" via ")
                    expr = parts[0].strip()
                    source = rule = None
                    if len(parts) > 1:
                        via = parts[1].split(" using ")
                        source = via[0].strip()
                        if len(via) > 1:
                            rule = via[1].strip()
                b.add_step(ProofStep(expr, source, rule, phase=state.phase))
        branches.append(b)
    
    def get_branches():
        branches = [...]
        return branches  # ✅ correct indentation
    

class Expr:
    def __init__(self, functor, args):
        self.functor = functor
        self.args = args

    def __repr__(self):
        return f"{self.functor}({', '.join(map(str, self.args))})"

    def __eq__(self, other):
        return isinstance(other, Expr) and self.functor == other.functor and self.args == other.args

    def __hash__(self):
        return hash((self.functor, tuple(self.args)))

class Axiom:
    def __init__(self, pattern, rule_name):
        self.pattern = pattern
        self.rule_name = rule_name

class ProofState:
    def __init__(self, branch="main"):
        self.trace = []
        self.known = set()
        self.branch = branch
        self.phase = self.compute_phase(branch)
        self.contradictions = []

    def compute_phase(self, branch):
        if branch == "main":
            return "ϕ₀"
        try:
            suffix = int(branch.split("_")[-1])
            return f"ϕ{suffix + 1}"
        except:
            return "ϕ?"

    def add(self, expr, source=None, rule=None, manager=None):
        entry = f"[{self.phase}] → Derived {expr}"
        if source and rule:
            entry += f" via {source} using {rule}"
        elif source:
            entry += f" via {source}"
        self.trace.append(entry)

        if self.is_contradictory(expr):
            warning = f"⚠ CONTRADICTION in branch '{self.branch}': {expr} conflicts with existing knowledge."
            self.trace.append(warning)
            self.contradictions.append((expr, source, rule))
            self.trace.append(f"✳ Branch '{self.branch}' marked UNSAFE due to contradiction.")
            if manager:
                fork = manager.create_branch(self, expr)
                return fork
            return None

        self.known.add(str(expr))
        return self

    def has(self, expr):
        return str(expr) in self.known

    def is_contradictory(self, expr):
        if expr.functor == "¬":
            return str(expr.args[0]) in self.known
        negated_form = Expr("¬", [expr])
        return str(negated_form) in self.known

    def is_stable(self):
        return len(self.contradictions) == 0

def prove(goal, facts, axioms):
    manager = BranchManager()
    state = ProofState()
    manager.branches[state.branch] = state

    for fact in facts:
        state = state.add(fact, manager=manager) or state

    queue = list(facts)

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
                        if not state.has(result_expr):
                            new_state = state.add(result_expr, source=str(current), rule=axiom.rule_name, manager=manager)
                            if new_state is not None:
                                state = new_state
                                queue.append(result_expr)
                            if result_expr == goal:
                                state.trace.append(f"✅ Goal {goal} reached in branch '{state.branch}'.")
                                return True, state.trace

    state.trace.append(f"✖ Goal {goal} could not be reached in branch '{state.branch}'.")
    return False, state.trace

if __name__ == "__main__":
    print("=== Test 1: Direct Proof ===")
    axiom1 = Axiom(Expr("∨", [Expr("¬", [Expr("P", ["x"])]), Expr("Q", ["x"])]), rule_name="Disjunctive Syllogism")
    axiom2 = Axiom(Expr("∨", [Expr("¬", [Expr("Q", ["x"])]), Expr("R", ["x"])]), rule_name="Disjunctive Syllogism")

    fact = Expr("P", ["a"])
    goal = Expr("R", ["a"])

    result, trace = prove(goal, [fact], [axiom1, axiom2])
    print("Proof result:", result)
    print("Trace:")
    for step in trace:
        print(step)

    print("\n=== Test 2: Attempt to Prove Contradiction ===")
    contradict = Expr("¬", [Expr("R", ["a"])])
    result, trace = prove(contradict, [fact], [axiom1, axiom2])
    print("Proof result (with contradiction):", result)
    print("Trace:")
    for step in trace:
        print(step)

    print("\n=== Test 3: Inject Contradiction and Fork ===")
    manager = BranchManager()
    state = ProofState(branch="main")
    manager.branches[state.branch] = state

    state = state.add(fact, manager=manager) or state
    queue = [fact]

    for axiom in [axiom1, axiom2]:
        if axiom.pattern.functor == "∨":
            negated, consequence = axiom.pattern.args
            if negated.functor == "¬":
                original = negated.args[0]
                substitution = unify(original, fact)
                if substitution:
                    result_expr = substitute_expr(consequence, substitution)
                    if not state.has(result_expr):
                        new_state = state.add(result_expr, source=str(fact), rule=axiom.rule_name, manager=manager)
                        if new_state is not None:
                            state = new_state
                            queue.append(result_expr)
                    fact = result_expr

    contradiction = Expr("¬", [Expr("R", ["a"])])
    state = state.add(contradiction, source="manual injection", rule="test", manager=manager) or state

    for branch_id, bstate in manager.branches.items():
        print(f"\nBranch: {branch_id} (phase {bstate.phase})")
        for line in bstate.trace:
            print(line)