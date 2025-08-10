# src/engine/state_manager.py
from __future__ import annotations
from typing import List, Dict, Any
from core.state import State
from core.phase_geometry import Phase

class StateManager:
    """
    Tracks phase transitions and exposes a compact snapshot for diagnostics.
    """
    def __init__(self):
        self.history: List[Dict[str, Any]] = []

    def record(self, state: State, note: str | None = None) -> None:
        self.history.append({
            "phase": getattr(state, "phase", None),
            "trace_len": len(getattr(state, "trace", []) or []),
            "note": note,
        })

    def transition(self, state: State, phase: Phase, note: str | None = None) -> None:
        state.transition(phase)
        if hasattr(state, "trace"):
            state.trace.append(f"transition→{phase.name}" + (f": {note}" if note else ""))
        self.record(state, note=note)

    def snapshot(self) -> Dict[str, Any]:
        return {
            "steps": len(self.history),
            "phases": [h["phase"].name if h["phase"] else None for h in self.history],
        }
