from evaluation.quantifier_engine import Quantifier
from evaluation.context_scope import ScopedContext
from evaluation.evaluate import LogicEvaluator

def test_quantifiers():
    ctx = ScopedContext()
    ctx.bind("x", [1, 2, 3])
    evaluator = LogicEvaluator(ctx)

    # Test 1: ∀x ∈ [1,2,3], x > 0  → True
    q1 = Quantifier("forall", "x", lambda x: x > 0)
    print("Test 1 (∀x > 0):", evaluator.evaluate(q1))  # Expected: True

    # Test 2: ∀x ∈ [1,2,3], x < 3  → False
    q2 = Quantifier("forall", "x", lambda x: x < 3)
    print("Test 2 (∀x < 3):", evaluator.evaluate(q2))  # Expected: False

    # Test 3: ∃x ∈ [1,2,3], x == 2 → True
    q3 = Quantifier("exists", "x", lambda x: x == 2)
    print("Test 3 (∃x == 2):", evaluator.evaluate(q3))  # Expected: True

    # Test 4: ∃x ∈ [1,2,3], x > 5  → False
    q4 = Quantifier("exists", "x", lambda x: x > 5)
    print("Test 4 (∃x > 5):", evaluator.evaluate(q4))  # Expected: False

    # Test 5: Variable shadowing test
    ctx.bind("x", 1000)
    q5 = Quantifier("forall", "x", lambda x: x < 10)
    print("Test 5 (shadowed ∀x < 10):", evaluator.evaluate(q5))  # Expected: True

if __name__ == "__main__":
    test_quantifiers()
