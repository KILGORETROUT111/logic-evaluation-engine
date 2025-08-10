# src/engine/diagnostics.py
from __future__ import annotations
from typing import Any, Dict
from core.state import State

def summarize_state(state: State) -> Dict[str, Any]:
    return {
        "phase": getattr(state, "phase", None).name if getattr(state, "phase", None) else None,
        "trace": list(getattr(state, "trace", []) or []),
    }
