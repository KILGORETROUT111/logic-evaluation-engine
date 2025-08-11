# src/engine/adapters/__init__.py
from __future__ import annotations
from typing import Any, Dict, Optional

from .base import BaseAdapter
from .legal import LegalAdapter
from .medical import MedicalAdapter

class AdapterRegistry:
    @staticmethod
    def create(domain: str, *, hooks: Optional[Dict[str, Any]] = None) -> BaseAdapter:
        if domain == "legal":
            return LegalAdapter(hooks=hooks)
        if domain == "medical":
            return MedicalAdapter(hooks=hooks)
        return BaseAdapter(hooks=hooks)
