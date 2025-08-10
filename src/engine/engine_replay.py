
# src/engine/replay.py
from __future__ import annotations
from typing import Any, Dict, List, Optional

class Replay:
    """Reconstructs a phase timeline from EventLog JSON (no engine needed)."""
    def __init__(self, events: List[Dict[str, Any]]):
        self.events = events

    def phases(self) -> List[str]:
        out: List[str] = []
        for ev in self.events:
            ph = ev.get("data",{}).get("phase")
            if ph:
                out.append(ph)
        return out

    def last_witness(self) -> Optional[Dict[str, Any]]:
        for ev in reversed(self.events):
            if ev.get("type") == "jam":
                return ev.get("data",{}).get("details",{}).get("witness")
        return None
