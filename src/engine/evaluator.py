# src/engine/evaluator.py
from __future__ import annotations
from typing import Union, Optional, Any
import json
import hashlib

from core.state import State
from core.phase_geometry import Phase
from nlp.parser import parse
from .contradiction_driver import detect_contradiction

# Optional Phase-8 helpers (no-ops if missing)
try:
    from nlp.canonicalize import canonicalize as _canon
except Exception:
    def _canon(x: Any) -> Any:  # type: ignore
        return x

try:
    from .reducer import whnf as _whnf
except Exception:
    def _whnf(x: Any) -> Any:  # type: ignore
        return x

try:
    from .event_log import EventLog
except Exception:
    EventLog = None  # type: ignore


def _log_safe(logger: Optional["EventLog"], kind: str, payload: dict) -> None:
    if not logger:
        return
    try:
        logger.event(kind, payload)
    except Exception:
        pass  # never let logging break evaluation


def _ast_metrics(node: Any) -> tuple[int, int]:
    """Return (size, max_depth). Cheap and defensive."""
    try:
        seen = 0
        maxd = 0
        stack = [(node, 1)]
        while stack:
            n, d = stack.pop()
            seen += 1
            if d > maxd:
                maxd = d

            # tuples: treat ('op', a, b) specially
            if isinstance(n, tuple):
                if n and isinstance(n[0], str):
                    it = n[1:]
                else:
                    it = n
                for c in it:
                    stack.append((c, d + 1))
                continue

            # dicts: common fields
            if isinstance(n, dict):
                for k, v in n.items():
                    if k in ("args", "children") and isinstance(v, (list, tuple)):
                        for c in v:
                            stack.append((c, d + 1))
                    elif isinstance(v, (dict, tuple)):
                        stack.append((v, d + 1))
                continue

            # objects with func/arg/body/param/left/right
            for attr in ("func", "arg", "body", "param", "left", "right"):
                if hasattr(n, attr):
                    stack.append((getattr(n, attr), d + 1))
    except Exception:
        return 1, 1
    return seen, maxd


def _hash_witness(w: Any) -> str:
    try:
        s = json.dumps(w, sort_keys=True) if isinstance(w, (dict, list, tuple)) else str(w)
        return hashlib.md5(s.encode("utf-8")).hexdigest()[:16]
    except Exception:
        return ""


def evaluate_full(expr: Union[str, Any], *, logger: Optional["EventLog"] = None) -> State:
    """
    Evaluate a text or AST into a State.
    Pipeline: parse (if str) → canonicalize (if available) → WHNF (if available) → contradiction detect.
    Transitions: MEM→ALIVE; ALIVE→JAM iff contradiction is detected (w/ witness logged).
    """
    # Parse if needed
    ast: Any = parse(expr) if isinstance(expr, str) else expr

    # Phase-8 prepasses (safe no-ops if modules not present)
    ast = _canon(ast)
    ast = _whnf(ast)

    state = State()
    _log_safe(logger, "parse", {"phase": "INIT"})
    state.transition(Phase.ALIVE)
    if hasattr(state, "trace"):
        state.trace.append("evaluate_full: parsed; canonicalized; reduced(WHNF)")

    # Contradiction analysis
    is_contra, details = detect_contradiction(ast, text_hint=expr if isinstance(expr, str) else None)
    if is_contra:
        state.transition(Phase.JAM)
        if hasattr(state, "trace"):
            mode = details.get("mode", "jam")
            state.trace.append(f"detect: {mode} → JAM")

        # metrics for BI/OLAP
        size, depth = _ast_metrics(ast)
        lite = {k: v for k, v in details.items() if k != "witness"}
        if "witness" in details:
            lite["witness"] = details["witness"]
            lite["witness_hash"] = _hash_witness(details["witness"])
        lite["ast_size"] = size
        lite["depth"] = depth

        _log_safe(
            logger,
            "jam",
            {
                "phase": "JAM",
                "mode": details.get("mode", "jam"),
                "details": lite,
            },
        )

    # Always log current phase at the end
    if getattr(state, "phase", None):
        _log_safe(logger, "alive", {"phase": state.phase.name})

    return state


def evaluate_expression(text: str, *, logger: Optional["EventLog"] = None) -> State:
    return evaluate_full(text, logger=logger)


def evaluate_object(obj: Any, *, logger: Optional["EventLog"] = None) -> State:
    return evaluate_full(obj, logger=logger)