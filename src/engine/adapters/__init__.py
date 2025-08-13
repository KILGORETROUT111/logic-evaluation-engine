from __future__ import annotations
from typing import Optional
from .base import DomainAdapter

# Lazy import to avoid import cycles at startup
def get_adapter(domain: str) -> Optional[DomainAdapter]:
    d = (domain or "").strip().lower()
    try:
        if d in ("legal", "law"):
            from .legal import LegalAdapter
            return LegalAdapter()
        if d in ("medical", "med", "health"):
            from .medical import MedicalAdapter
            return MedicalAdapter()
        if d in ("defense", "def"):
            from .defense import DefenseAdapter
            return DefenseAdapter()
    except Exception:
        return None
    return None
