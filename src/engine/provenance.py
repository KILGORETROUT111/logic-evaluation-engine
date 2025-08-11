# src/engine/provenance.py
from __future__ import annotations
import json
from typing import Any, Dict, List

class ProvenanceRecorder:
    def __init__(self, run_id: str):
        self.run_id = run_id
        self._events: List[Dict[str, Any]] = []
        self._step = 0

    def record(self, *, kind: str, phase_before: str | None, phase_after: str | None,
               reason: str, details: Dict[str, Any] | None = None) -> None:
        self._step += 1
        ev = {
            "run_id": self.run_id,
            "step": self._step,
            "kind": kind,
            "phase_before": phase_before,
            "phase_after": phase_after,
            "reason": reason,
            "details": details or {},
        }
        self._events.append(ev)

    def to_jsonl(self) -> str:
        return "\n".join(json.dumps(e, ensure_ascii=False) for e in self._events)
