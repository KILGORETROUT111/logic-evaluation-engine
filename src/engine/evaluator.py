# src/engine/evaluator.py

from typing import Union
from core.state import State
from core.phase_geometry import Phase   # ← change is here
from nlp.parser import parse

def _beta_reduce(ast):
    return ast  # stub

def evaluate_full(expr: Union[str, object]) -> State:
    ast = parse(expr) if isinstance(expr, str) else expr
    state = State()
    state.transition(Phase.ALIVE)
    state.trace.append("evaluate_full: parsed and (stub) reduced")
    _beta_reduce(ast)
    return state

def evaluate_expression(text: str) -> State:
    return evaluate_full(text)