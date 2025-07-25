# core/lee_event.py

from enum import Enum, auto

class EventPhase(Enum):
    LITERAL = auto()
    VARIABLE = auto()
    LAMBDA = auto()
    APPLICATION = auto()
    DEFINE = auto()
    SUBSTITUTION = auto()
    MEMORY = auto()
    QUANTIFIER = auto()
    IF_THEN_ELSE = auto()
    BINARY_OP = auto()
    UNKNOWN = auto()

class LEEEvent:
    def __init__(self, phase: EventPhase, expr_repr: str = "", value=None):
        self.phase = phase
        self.expr_repr = expr_repr
        self.value = value

    def to_dict(self):
        return {
            "phase": self.phase.name,
            "expr": self.expr_repr,
            "value": self.value
        }

    @staticmethod
    def from_dict(data):
        phase = EventPhase[data["phase"]]
        expr = data.get("expr", "")
        value = data.get("value", None)
        return LEEEvent(phase, expr, value)

    def __repr__(self):
        return f"LEEEvent({self.phase}, {self.expr_repr}, {self.value})"

