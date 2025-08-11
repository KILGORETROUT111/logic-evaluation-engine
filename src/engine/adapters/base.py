# src/engine/adapters/base.py
from __future__ import annotations
from typing import Any, Dict, Optional

class BaseAdapter:
    def __init__(self, *, hooks: Optional[Dict[str, Any]] = None) -> None:
        self.hooks: Dict[str, Any] = hooks or {}

    def enrich(self, norm_expr: str) -> Dict[str, Any]:
        # Minimal default enrichment
        return {
            "pattern": norm_expr,
            "score": 0.0,
            "tags": [],
        }
