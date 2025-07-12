import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from core.expressions import Application, Literal
from core.evaluation import evaluate_full
from core.states import State

@pytest.mark.stress
def test_safe_failure_on_invalid_expression():
    invalid_expr = Application(Literal(42), Literal(7))
    result, _ = evaluate_full(invalid_expr)
    print(f"[TRACE] Result: {result}")
    assert result == State.ALIVE
