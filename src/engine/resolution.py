# src/engine/resolution.py
from __future__ import annotations
from typing import Any, Dict, List, Optional, Protocol


class ResolutionStrategy(Protocol):
    def name(self) -> str: ...
    def try_resolve(self, *, expr: Any, witness: Dict) -> Optional[Dict]:
        """
        Return a dict like:
          {"expr": <rewritten_expr>, "note": "<human hint>"}
        or None if not applicable.
        Must never raise.
        """
        ...


class ImplicationGuardStrategy:
    """
    If witness is the canonical 1 -> 0, suggest guarding it to VAC (toy demo).
    This demonstrates the API without committing to policy.
    """
    def name(self) -> str:
        return "implication_guard"

    def try_resolve(self, *, expr: Any, witness: Dict) -> Optional[Dict]:
        try:
            if witness.get("pattern") == "1 -> 0":
                return {"expr": ("vac",), "note": "guarded jam (1->0) to VAC"}
        except Exception:
            pass
        return None


class LocalRefutationDecompose:
    """
    If witness is X & ~X, suggest replacing with VAC (toy demo).
    """
    def name(self) -> str:
        return "refutation_decompose"

    def try_resolve(self, *, expr: Any, witness: Dict) -> Optional[Dict]:
        try:
            if witness.get("pattern") == "X & ~X":
                X = witness.get("X")
                if X is not None:
                    return {"expr": ("vac",), "note": "replaced X&~X with VAC to proceed"}
        except Exception:
            pass
        return None


class Resolver:
    """
    Tries strategies in order; records whether anything applied.
    Does NOT re-evaluate; it only proposes and returns metadata.
    """
    def __init__(self, strategies: Optional[List[ResolutionStrategy]] = None):
        self.strategies = strategies or [ImplicationGuardStrategy(), LocalRefutationDecompose()]

    def attempt(self, *, expr: Any, witness: Optional[Dict]) -> Dict:
        """
        Returns:
          {"attempted": True, "applied": False}
          or {"attempted": True, "applied": True, "strategy": name, "note": ..., "expr": ...}
        Never raises.
        """
        if not witness:
            return {"attempted": True, "applied": False, "note": "no witness"}

        for s in self.strategies:
            try:
                res = s.try_resolve(expr=expr, witness=witness)
                if res and "expr" in res:
                    return {"attempted": True, "applied": True, "strategy": s.name(), **res}
            except Exception:
                continue
        return {"attempted": True, "applied": False}
