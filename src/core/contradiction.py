# core/contradiction.py

from core.expressions import Expression
from core.state import State
from core.phase_geometry import Phase

class Contradiction(Exception):
    def __init__(self, message, trace=None):
        super().__init__(message)
        self.trace = trace or []


def detect_contradiction(expr: Expression, state: State) -> bool:
    """
    Scans current state bindings for a contradiction with expr.
    Returns True if contradiction found, else False.
    """
    for binding in state.bindings:
        if expr == binding and state.phase == Phase.JAM:
            return True
    return False


def jam_state(expr: Expression, state: State) -> State:
    """
    Transitions state to JAM phase if contradiction detected.
    Archives the event into state's contradiction trace.
    """
    if detect_contradiction(expr, state):
        state.phase = Phase.JAM
        state.trace.append({"event": "JAM", "expr": repr(expr)})
    return state


def assert_no_contradiction(expr: Expression, state: State):
    """
    Raises Contradiction if contradiction is detected.
    """
    if detect_contradiction(expr, state):
        raise Contradiction(f"Contradiction detected in phase {state.phase}", trace=state.trace)
