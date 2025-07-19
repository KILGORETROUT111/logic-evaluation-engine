import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from core.expressions import Lambda, Variable, Application, Literal
from core.evaluation import evaluate_full
from core.states import State

@pytest.mark.stress
def test_nested_lambda_identity():
    inner_lambda = Lambda("y", Variable("y"))
    outer_lambda = Lambda("x", inner_lambda)
    first_application = Application(outer_lambda, Literal(1))
    full_application = Application(first_application, Literal(2))
    result, _ = evaluate_full(full_application)
    print(f"[TRACE] Result: {result}")
    assert result == State.ALIVE