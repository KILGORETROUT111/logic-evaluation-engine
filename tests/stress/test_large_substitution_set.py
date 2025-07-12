import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from core.expressions import Lambda, Variable, Application, Literal, Substitution
from core.evaluation import evaluate_full
from core.states import State

@pytest.mark.stress
def test_large_substitution_set():
    param = Variable("x")
    expr = Lambda("x", param)
    arg_expr = Literal(1)
    app_expr = Application(expr, arg_expr)
    result, _ = evaluate_full(app_expr)
    print(f"[TRACE] Result: {result}")
    assert result == State.ALIVE