from __future__ import annotations
import re
from typing import Dict
from .base import DomainAdapter

class DefenseAdapter(DomainAdapter):
    def __init__(self) -> None:
        super().__init__(name="defense")

    def analyze(self, text: str) -> Dict:
        s = text.strip()
        # "X triggers Y"
        m = re.search(r"\b([A-Za-z][\w]*)\s+(triggers|provokes)\s+([A-Za-z][\w]*)\b", s, re.I)
        if m:
            p, rel, q = m.group(1), m.group(2).lower(), m.group(3)
            return {"pattern": f"{p} -> {q}", "tags": [f"rel:{rel}", "implication:nl"]}
        return {}
