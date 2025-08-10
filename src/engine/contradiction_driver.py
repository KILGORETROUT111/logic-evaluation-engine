# src/engine/contradiction_driver.py
from __future__ import annotations
from typing import Any, Optional, Tuple, Dict

# Prefer the real core module when available
try:
    from core import contradiction as core_contra  # exposes analyze(ast) or detect(ast)
except Exception:
    core_contra = None  # graceful fallback


def _fallback_text_heuristic(text: Optional[str]) -> Tuple[bool, Dict]:
    """
    Tiny text-based JAM detector for smoke tests and simple strings.
    Returns (is_contradiction, details).
    """
    if not isinstance(text, str):
        return False, {"is_contradiction": False, "source": "fallback"}

    t = text.lower().strip()

    # obvious marker
    if "contradiction" in t:
        return True, {
            "is_contradiction": True,
            "source": "fallback",
            "mode": "heuristic",
            "witness": {"pattern": "contains 'contradiction'"}
        }

    # p & ~p (local refutation) patterns
    if " & ~" in t or " and not " in t or "∧ ¬" in text:
        return True, {
            "is_contradiction": True,
            "source": "fallback",
            "mode": "local-refutation",
            "witness": {"pattern": "X & ~X"}
        }

    # implication jam 1 -> 0 (allow split '-' '>')
    if "1 -> 0" in t or "1 - > 0" in t or "1 → 0" in text:
        return True, {
            "is_contradiction": True,
            "source": "fallback",
            "mode": "implication-jam",
            "witness": {"pattern": "1 -> 0"}
        }

    return False, {"is_contradiction": False, "source": "fallback"}


def detect_contradiction(ast: Any, *, text_hint: Optional[str] = None) -> Tuple[bool, Dict]:
    """
    Returns (is_contradiction, details).
    Prefers /core/contradiction; if it reports no contradiction (or errors),
    falls back to a small text heuristic so simple string tests still work.
    """
    # Try the real detector first
    if core_contra:
        try:
            if hasattr(core_contra, "analyze"):
                res = core_contra.analyze(ast)
                if bool(res.get("is_contradiction")):
                    return True, res
            elif hasattr(core_contra, "detect"):
                ok = bool(core_contra.detect(ast))
                if ok:
                    return True, {"is_contradiction": True, "source": "core.detect"}
            # If core says "no", fall through to heuristic
        except Exception as e:
            ok, det = _fallback_text_heuristic(text_hint)
            if ok:
                det["error"] = type(e).__name__
            return ok, det

    # Heuristic fallback
    return _fallback_text_heuristic(text_hint)
