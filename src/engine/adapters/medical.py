# src/engine/adapters/medical.py
from __future__ import annotations
from typing import Any, Dict, List
from .base import BaseAdapter

class MedicalAdapter(BaseAdapter):
    def enrich(self, norm_expr: str) -> Dict[str, Any]:
        out: Dict[str, Any] = {
            "domain": "medical",
            "pattern": norm_expr,
            "score": 0.3,
        }

        # Risk via divergence classifier (tests monkeypatch dm_classify)
        risk = "low"
        dm = self.hooks.get("divergence_classify") or self.hooks.get("dm_classify")
        if callable(dm):
            try:
                risk = dm(norm_expr)
            except Exception:
                pass
        out["risk"] = risk

        # Entities via optional NER hook (tests monkeypatch ner_extract)
        ner = self.hooks.get("ner_extract")
        if callable(ner):
            try:
                ents = ner(norm_expr)
                if isinstance(ents, list):
                    out["entities"] = ents
            except Exception:
                pass

        return out

from __future__ import annotations
import re
from typing import Dict
from .base import DomainAdapter

class MedicalAdapter(DomainAdapter):
    def __init__(self) -> None:
        super().__init__(name="medical")

    def analyze(self, text: str) -> Dict:
        s = text.strip()
        # "X indicates Y", "X suggests Y"
        m = re.search(r"\b([A-Za-z][\w]*)\s+(indicates|suggests)\s+([A-Za-z][\w]*)\b", s, re.I)
        if m:
            p, rel, q = m.group(1), m.group(2).lower(), m.group(3)
            return {"pattern": f"{p} -> {q}", "tags": [f"rel:{rel}", "implication:nl"]}
        return {}
