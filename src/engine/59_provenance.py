# src/engine/provenance.py
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
import json


@dataclass
class ProvenanceEvent:
    run_id: str
    step: int
    kind: str                    # 'start','parse','rewrite','detect','archive','resolution','transition',...
    phase_before: Optional[str]  # 'ALIVE'/'JAM'/'MEM'/'VAC' or None
    phase_after: Optional[str]
    reason: str                  # e.g. 'canon','whnf','implication-jam','archive'
    details: Dict[str, Any]
    ts: str


class ProvenanceRecorder:
    """Canonical provenance collector. Independent of evaluation semantics."""
    def __init__(self, run_id: str):
        self.run_id = run_id
        self._events: List[ProvenanceEvent] = []
        self._step = 0

    def record(
        self,
        *,
        kind: str,
        phase_before: Optional[str],
        phase_after: Optional[str],
        reason: str,
        details: Dict[str, Any] | None = None,
    ) -> None:
        self._step += 1
        pe = ProvenanceEvent(
            run_id=self.run_id,
            step=self._step,
            kind=kind,
            phase_before=phase_before,
            phase_after=phase_after,
            reason=reason,
            details=details or {},
            ts=datetime.now(timezone.utc).isoformat(),
        )
        self._events.append(pe)

    def to_rows(self) -> List[Dict[str, Any]]:
        return [asdict(e) for e in self._events]

    def to_jsonl(self) -> str:
        return "\n".join(json.dumps(r, ensure_ascii=False) for r in self.to_rows())

    def clear(self) -> None:
        self._events.clear()
        self._step = 0
