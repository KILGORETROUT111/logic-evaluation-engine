import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from core.expressions import Lambda, Variable, Application, Literal
from core.evaluation import evaluate_full
from core.states import State

@pytest.mark.stress
def test_simple_evaluation_returns_alive():
    identity = Lambda("x", Variable("x"))
    expr = Application(identity, Literal(42))
    result, _ = evaluate_full(expr)
    print(f"[TRACE] Result: {result}")
    assert result == State.ALIVE
