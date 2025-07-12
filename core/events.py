# core/events.py

from core.phase import EventPhase

class LEEEvent:
    def __init__(self, expr=None, value=None, phase=EventPhase.LITERAL):
        self.expr = expr
        self.value = value
        self.phase = phase

    def to_dict(self):
        return {
            "expr": str(self.expr),
            "value": str(self.value),
            "phase": self.phase.name
        }