# src/core/contradiction.py
from __future__ import annotations
from typing import Any, Dict, Tuple

def _as_tuple(x: Any) -> Tuple:
    return x if isinstance(x, tuple) else ()

def analyze(expr: Any) -> Dict[str, Any]:
    """
    Returns:
      - 'is_contradiction': bool
      - 'mode': 'implication-jam' | 'local-refutation' | 'none'
      - 'witness': dict with details:
          * implication: {'kind':'implication','pattern':'1 -> 0','antecedent':1,'consequent':0}
          * local refutation: {'kind':'local-refutation','pattern':'X & ~X','X': <symbol>}
    """
    # --- tuple AST path ------------------------------------------------------
    t = _as_tuple(expr)
    if t:
        op = t[0] if len(t) > 0 else None

        # implication ('->', lhs, rhs)
        if op in ("->", "IMPLIES", "⇒", "→") and len(t) >= 3:
            l, r = t[1], t[2]
            if l in (1, "1") and r in (0, "0"):
                return {
                    "is_contradiction": True,
                    "mode": "implication-jam",
                    "witness": {
                        "kind": "implication",
                        "pattern": "1 -> 0",
                        "antecedent": 1 if l in (1, "1") else l,
                        "consequent": 0 if r in (0, "0") else r,
                    },
                }
            if l in (1, "1") and r in (1, "1"):
                return {"is_contradiction": False, "mode": "none", "witness": None}

        # local refutation: And(X, Not(X))
        if op in ("And", "AND", "∧") and len(t) >= 3:
            X, rhs = t[1], t[2]
            rt = _as_tuple(rhs)
            if rt and rt[0] in ("Not", "NOT", "¬", "~") and len(rt) >= 2 and rt[1] == X:
                return {
                    "is_contradiction": True,
                    "mode": "local-refutation",
                    "witness": {
                        "kind": "local-refutation",
                        "pattern": "X & ~X",
                        "X": X,
                    },
                }

    # --- string fallback (best-effort) ---------------------------------------
    try:
        s = str(expr).replace(" ", "")
    except Exception:
        s = ""

    if "->" in s:
        if "1->0" in s:
            return {
                "is_contradiction": True,
                "mode": "implication-jam",
                "witness": {
                    "kind": "implication",
                    "pattern": "1 -> 0",
                    "antecedent": 1,
                    "consequent": 0,
                },
            }
        if "1->1" in s:
            return {"is_contradiction": False, "mode": "none", "witness": None}

    if "And(" in s and ("Not(" in s or "~" in s or "¬" in s):
        return {
            "is_contradiction": True,
            "mode": "local-refutation",
            "witness": {
                "kind": "local-refutation",
                "pattern": "X & ~X",
                # unknown X in string fallback
            },
        }

    return {"is_contradiction": False, "mode": "none", "witness": None}
