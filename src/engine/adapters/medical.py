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
