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
        new_state.trace.append(f"↳ Forked from '{parent_state.branch}' due to contradiction with {from_expr}")
        self.branches[new_id] = new_state
        return new_state

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
    # Convert "main", "main_1", "main_2" to ϕ₀, ϕ₁, etc.
    if branch == "main":
        return "ϕ₀"
    try:
        suffix = int(branch.split("_")[-1])
        return f"ϕ{suffix + 1}"
    except:
        return "ϕ?"
entry = f"[{self.phase}] → Derived {expr}"

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
        print(f"\nBranch: {branch_id}")
        for line in bstate.trace:
            print(line)