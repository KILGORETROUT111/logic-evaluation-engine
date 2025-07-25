import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from core.expressions import Lambda, Variable, Application, Literal
from core.evaluation import evaluate_full
from core.states import State

@pytest.mark.stress
def test_universal_quantifier_define_and_apply():
    identity = Lambda("x", Variable("x"))
    expr = Application(identity, Literal(7))
    result, _ = evaluate_full(expr)
    print(f"[TRACE] Result: {result}")
    assert result == State.ALIVE