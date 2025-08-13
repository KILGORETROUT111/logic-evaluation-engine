# src/engine/adapters/legal.py
from __future__ import annotations
from typing import Any, Dict
from .base import BaseAdapter

class LegalAdapter(BaseAdapter):
    def enrich(self, norm_expr: str) -> Dict[str, Any]:
        out: Dict[str, Any] = {
            "domain": "legal",
            "pattern": norm_expr,
            "score": 0.5,
            "tags": ["implication", "boolean"] if "->" in norm_expr else [],
        }

        # Pass-through to optional counterfactual hook (tests monkeypatch this)
        cf = self.hooks.get("counterfactual_analyze") or self.hooks.get("cf_analyze")
        if callable(cf):
            try:
                out["counterfactual"] = cf(norm_expr)
            except Exception:
                # Never let adapter hooks break the pipeline
                pass

        return out

from __future__ import annotations
import re
from typing import Dict, List
from .base import DomainAdapter

class LegalAdapter(DomainAdapter):
    def __init__(self) -> None:
        super().__init__(name="legal")

    def analyze(self, text: str) -> Dict:
        s = text.strip()
        # patterns: "A implies B", "A results in B", "A entails B", "A causes B"
        m = re.search(r"\b([A-Za-z][\w]*)\s+(implies|results in|entails|causes)\s+([A-Za-z][\w]*)\b", s, re.I)
        if m:
            p, rel, q = m.group(1), m.group(2).lower(), m.group(3)
            return {"pattern": f"{p} -> {q}", "tags": [f"rel:{rel}", "implication:nl"]}
        return {}
