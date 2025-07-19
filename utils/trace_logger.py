# utils/trace_logger.py

from core.events import LEEEvent
from core.phase import EventPhase

def log_event(expr=None, value=None, phase=EventPhase.LITERAL):
    """
    Returns a LEEEvent with the given parameters.
    """
    return LEEEvent(expr=expr, value=value, phase=phase)