class Quantifier:
    def __init__(self, kind, var, formula):
        if kind not in ('forall', 'exists'):
            raise ValueError("Quantifier kind must be 'forall' or 'exists'")
        self.kind = kind  # 'forall' or 'exists'
        self.var = var    # variable name (e.g., 'x')
        self.formula = formula  # lambda or callable taking var

    def evaluate(self, domain):
        results = []
        for value in domain:
            outcome = self.formula(value)
            results.append(outcome)
            if self.kind == 'exists' and outcome:
                return True
            if self.kind == 'forall' and not outcome:
                return False
        return all(results) if self.kind == 'forall' else any(results)

class AxiomManager:
    def __init__(self):
        self.axioms = {}

    def add_axiom(self, label, expression):
        self.axioms[label] = expression

    def get_axiom(self, label):
        return self.axioms.get(label)

    def list_axioms(self):
        return list(self.axioms.keys())

# Example Usage:
if __name__ == "__main__":
    # ∀x ∈ [1,2,3], P(x) = x > 0
    q = Quantifier("forall", "x", lambda x: x > 0)
    print("∀x>0:", q.evaluate([1, 2, 3]))  # True

    # ∃x ∈ [1,2,3], P(x) = x == 2
    q2 = Quantifier("exists", "x", lambda x: x == 2)
    print("∃x==2:", q2.evaluate([1, 2, 3]))  # True

    axioms = AxiomManager()
    axioms.add_axiom("A1", "∀x.¬P(x) ∨ Q(x)")
    print("Stored Axioms:", axioms.list_axioms())
