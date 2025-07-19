import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from core.expressions import Lambda, Variable, Application, Literal, Substitution
from core.evaluation import evaluate_full
from core.states import State

def test_universal_quantifier_failure():
    # ∀x. P(x) fails when not all instances satisfy the condition
    expr = Application(Lambda("x", Application(Variable("P"), Variable("x"))), Literal(5))
    result, _ = evaluate_full(expr)
    assert result == State.JAM