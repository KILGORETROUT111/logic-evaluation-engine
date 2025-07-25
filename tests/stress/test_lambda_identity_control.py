import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from core.expressions import Lambda, Variable, Application
from core.evaluation import evaluate_full
from core.states import State

@pytest.mark.stress
def test_lambda_identity_control():
    identity = Lambda("x", Variable("x"))
    expr = Application(identity, Variable("x"))
    result, _ = evaluate_full(expr, env={"x": State.ALIVE})
    print(f"[TRACE] Result: {result}")
    assert result == State.ALIVE
