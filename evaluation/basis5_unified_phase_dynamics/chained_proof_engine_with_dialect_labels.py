from evaluation.unifier import unify
from evaluation.utils_expr import substitute_expr
from evaluation.logic_truth import evaluate_truth

class Expr:
    def __init__(self, functor, args):
        self.functor = functor
        self.args = args

    def __repr__(self):
        return f"{self.functor}({', '.join(map(str, self.args))})"

class Axiom:
    def __init__(self, pattern, rule_name):
        self.pattern = pattern
        self.rule_name = rule_name  # Proof dialect label

class ProofState:
    def __init__(self):
        self.trace = []
        self.known = set()

    def add(self, expr, source=None, rule=None):
        self.known.add(str(expr))
        entry = f"→ Derived {expr}"
        if source and rule:
            entry += f" via {source} using {rule}"
        elif source:
            entry += f" via {source}"
        self.trace.append(entry)

    def has(self, expr):
        return str(expr) in self.known

def prove(goal, facts, axioms):
    state = ProofState()
    for fact in facts:
        state.add(fact)

    frontier = facts[:]
    while frontier:
        current = frontier.pop(0)
        
        
        known_set = set(str(f) for f in known)
        queue = known[:]

        while queue:
            current = queue.pop(0)
            for axiom in axioms:
                substitution = unify(axiom.pattern.args[0], current)
                if substitution:
                    result_expr = substitute_expr(axiom.pattern.args[1], substitution)

                    if str(result_expr) in known_set:
                        continue  # already derived

                    trace.append(f"→ Derived {result_expr} via {axiom.rule_name} + {current}")
                    if result_expr == goal:
                        trace.append(f"✅ Goal {goal} reached.")
                        return True, trace

                    queue.append(result_expr)
                    known_set.add(str(result_expr))
 
# Sample usage
if __name__ == "__main__":
    # Axiom: ¬P(x) ∨ Q(x)  → in our model: if P(a), then Q(a)
    axiom1 = Axiom(Expr("∨", [Expr("¬", [Expr("P", ["x"])]), Expr("Q", ["x"])]), rule_name="Disjunctive Syllogism")
    axiom2 = Axiom(Expr("∨", [Expr("¬", [Expr("Q", ["x"])]), Expr("R", ["x"])]), rule_name="Disjunctive Syllogism")

    # Given fact
    fact = Expr("P", ["a"])
    goal = Expr("R", ["a"])

    result, trace = prove(goal, [fact], [axiom1, axiom2])

    print("Proof result:", result)
    print("Trace:")
    for step in trace:
        print(step)
