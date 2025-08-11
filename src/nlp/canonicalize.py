# src/nlp/canonicalize.py
from __future__ import annotations
from typing import Any, List, Tuple, Union

Atom = Union[str, int]

def _is_app(node: Any) -> bool:
    # tolerate multiple encodings of "application"
    if hasattr(node, "func") and hasattr(node, "arg"):
        return True
    if hasattr(node, "f") and hasattr(node, "x"):
        return True
    if isinstance(node, tuple) and len(node) == 3 and node[0] in ("App", "Application"):
        return True
    return False

def _app_func(node: Any) -> Any:
    if hasattr(node, "func"): return node.func
    if hasattr(node, "f"):    return node.f
    if isinstance(node, tuple): return node[1]
    return None

def _app_arg(node: Any) -> Any:
    if hasattr(node, "arg"): return node.arg
    if hasattr(node, "x"):   return node.x
    if isinstance(node, tuple): return node[2]
    return None

def _atomize(x: Any) -> Atom:
    # Pull out a printable token
    if isinstance(x, (str, int)):
        return x
    # common mini-AST atoms like Variable(name='-')
    if hasattr(x, "name"):
        name = getattr(x, "name")
        return name if isinstance(name, (str, int)) else str(name)
    # last resort, string
    return str(x)

def _flatten_application(root: Any) -> List[Atom]:
    """
    Turn left-associated application into a flat token list.
    Example (pseudo): App(App(App(1, '-'), '>'), 0) -> [1, '-', '>', 0]
    """
    out: List[Atom] = []
    n = root
    while _is_app(n):
        out.append(_atomize(_app_arg(n)))
        n = _app_func(n)
    out.append(_atomize(n))
    out.reverse()
    return out

def canonicalize(text: Any) -> Any:
    """
    Accepts either a string *or* an AST-like application tree.
    - If string: normalize IMPLIES/⇒/→ to '->' and return string.
    - If application AST representing 1 - > 0: return ('->', 1, 0).
      (More generally: collapse [lhs, '-', '>', rhs] -> ('->', lhs, rhs))
    Otherwise, return the input unchanged.
    """
    # AST case
    if _is_app(text):
        toks = _flatten_application(text)  # e.g., [1, '-', '>', 0]
        if len(toks) == 4:
            lhs, t1, t2, rhs = toks
            if str(t1).strip() in {"-", "−", "–", "—"} and str(t2).strip() in {">", "→", "⇒"}:
                return ("->", lhs, rhs)
        if len(toks) == 3 and str(toks[0]).strip() == "->":
            return ("->", toks[1], toks[2])
        return text  # not an arrow pattern; leave unchanged

    # String case
    if isinstance(text, str):
        s = text.strip()
        if not s:
            return s
        s = s.replace("IMPLIES", "->").replace("⇒", "->").replace("→", "->")
        return s

    # Anything else: unchanged
    return text
