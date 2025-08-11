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
