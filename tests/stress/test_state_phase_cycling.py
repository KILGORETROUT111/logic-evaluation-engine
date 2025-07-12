import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from core.expressions import Lambda, Variable, Application, Literal
from core.evaluation import evaluate_full
from core.states import State

@pytest.mark.stress
def test_state_phase_cycle():
    expr1 = Application(Lambda("x", Variable("x")), Literal(42))
    result1, _ = evaluate_full(expr1)
    print(f"[TRACE] Result: {result1}")
    assert result1 == State.ALIVE