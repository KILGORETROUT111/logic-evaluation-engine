from evaluation.quantifier_engine import Quantifier
from evaluation.context_scope import ScopedContext

class LogicEvaluator:
    def __init__(self, context=None):
        self.context = context if context else {}

    def evaluate(self, expr):
        if isinstance(expr, Quantifier):
            try:
                domain = self.context.lookup(expr.var)
            except NameError:
                domain = []

            print(f"Evaluating quantifier over domain: {domain}")
            return expr.evaluate(domain)

        # Dummy fallback (to be extended)
        return f"Evaluated: {expr}"

# Example usage
if __name__ == "__main__":
    # Setup evaluation context
    context = {
        "x": [1, 2, 3]
    }

    evaluator = LogicEvaluator(context)

    q1 = Quantifier("forall", "x", lambda x: x > 0)
    q2 = Quantifier("exists", "x", lambda x: x == 2)

    print("∀x > 0:", evaluator.evaluate(q1))  # True
    print("∃x == 2:", evaluator.evaluate(q2))  # True
