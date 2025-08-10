import pytest

from core.expressions import Variable, Lambda, Application
from core.phase_geometry import Phase
from engine.evaluator import evaluate_full
from nlp.parser import parse

def test_identity_beta_reduction_runs_without_jam():
    # (λx. x) y  → should evaluate without throwing and not JAM
    x = Variable("x")
    y = Variable("y")
    expr = Application(Lambda(x, x), y)

    state = evaluate_full(expr)
    assert hasattr(state, "phase"), "evaluate_full should return a State-like object"
    assert state.phase in {Phase.MEM, Phase.ALIVE, Phase.VAC}, f"unexpected phase: {state.phase}"

def test_parse_and_eval_lambda_runs():
    # Parser → Evaluator round trip
    expr = parse("lambda x . x")
    state = evaluate_full(expr)
    assert state is not None
    assert state.phase in {Phase.MEM, Phase.ALIVE, Phase.VAC}

def test_tensor_archive_is_importable():
    # Sanity check: analytic layer is wired (no runtime use)
    from analytic.tensor_archive import TensorArchive, ContradictionTensor  # noqa: F401
    assert True
