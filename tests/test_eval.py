import pytest
from core.expressions import Functor, Value, Var
from core.evaluation import evaluate_full
from core.state import State

def test_jam_evaluation():
    context = {"x": 1}
    expr = Functor("Root", [
        Functor("EX", [Var("x"), Functor("JAM")]),
    ])
    state, trace = evaluate_full(expr, context)
    assert state == State.JAM
    assert "JAM" in trace
    assert trace["JAM"][-1].name == "Root"

def test_mem_evaluation():
    context = {"z": 9}
    expr = Functor("Node", [
        Value(3), Functor("MEM"), Var("z")
    ])
    state, trace = evaluate_full(expr, context)
    assert state == State.MEM
    assert "MEM" in trace
    assert any(isinstance(item, Functor) for item in trace["MEM"])
