# src/nlp/handshake.py
from __future__ import annotations

import re
from typing import Optional, Dict

# Work both in-repo ("src.*") and installed package ("*")
try:
    from src.analytic.lambda_calc import LVar, App, beta_normal_form, LTerm
except Exception:
    from analytic.lambda_calc import LVar, App, beta_normal_form, LTerm

try:
    from src.engine.adapters import get_adapter  # type: ignore
except Exception:
    try:
        from engine.adapters import get_adapter  # type: ignore
    except Exception:
        def get_adapter(_domain: str):
            return None  # type: ignore

# Symbol used to represent implication in λ-terms
_IMP = "Imp"

def _mk_imp(p: str, q: str) -> LTerm:
    """Encode implication as a curried application: ((Imp p) q)."""
    return App(App(LVar(_IMP), LVar(p)), LVar(q))

def parse_text_to_lambda(text: str) -> LTerm:
    """Very small NL→λ parser for implication-like patterns."""
    s = text.strip()

    # 1) "A -> B"
    m = re.fullmatch(r"\s*([A-Za-z][A-Za-z0-9_]*)\s*->\s*([A-Za-z][A-Za-z0-9_]*)\s*", s)
    if m:
        return _mk_imp(m.group(1), m.group(2))

    # 2) "if A then B"
    m = re.fullmatch(
        r"\s*if\s+([A-Za-z][A-Za-z0-9_]*)\s+then\s+([A-Za-z][A-Za-z0-9_]*)\s*",
        s,
        re.IGNORECASE,
    )
    if m:
        return _mk_imp(m.group(1), m.group(2))

    # 3) bare symbol
    m = re.fullmatch(r"\s*([A-Za-z][A-Za-z0-9_]*)\s*", s)
    if m:
        return LVar(m.group(1))

    # 4) fallback: squash to a single safe token
    token = re.sub(r"\W+", "_", s) or "Expr"
    return LVar(token)

def extract_implication_pattern(t: LTerm) -> Optional[str]:
    """Return 'P -> Q' if β-NF has shape Imp P Q; else None."""
    nf = beta_normal_form(t)
    if isinstance(nf, App) and isinstance(nf.fn, App):
        fn = nf.fn.fn
        if isinstance(fn, LVar) and fn.name == _IMP:
            p, q = nf.fn.arg, nf.arg
            if isinstance(p, LVar) and isinstance(q, LVar):
                return f"{p.name} -> {q.name}"
    return None

# ---- domain-agnostic NL implication guesser --------------------------------

_REL_WORDS = r"(implies|results in|entails|causes|indicates|suggests|triggers|provokes)"

def _guess_nl_implication(text: str) -> Optional[str]:
    """Heuristic: extract 'P -> Q' from simple NL like 'breach implies liability'."""
    s = text.strip()
    m = re.search(
        rf"\b([A-Za-z][\w]*)\s+{_REL_WORDS}\s+([A-Za-z][\w]*)\b",
        s,
        re.IGNORECASE,
    )
    if m:
        p, q = m.group(1), m.group(3)  # group(2) is relation word
        return f"{p} -> {q}"
    return None

def _canonical_domain_name(dom: str) -> Optional[str]:
    d = (dom or "").strip().lower()
    if d in ("legal", "law"):
        return "legal"
    if d in ("medical", "med", "health"):
        return "medical"
    if d in ("defense", "def"):
        return "defense"
    return None

# ---------------------------------------------------------------------------

def evaluate_text(text: str, pipeline) -> dict:
    """
    NL text → λ-term → β-NF → Pipeline.run('P -> Q', meta={"nl","lambda_nf","adapter"?}).
    Prefer domain adapter; otherwise λ extraction; otherwise NL heuristic.
    Ensure adapter metadata when domain is known (even if heuristic path).
    """
    term = parse_text_to_lambda(text)
    nf = beta_normal_form(term)

    # normalize domain name
    dom = _canonical_domain_name(getattr(pipeline, "domain", ""))

    pattern: Optional[str] = None
    adapter_meta: Optional[Dict] = None

    # 1) Domain adapter (if present)
    adapter = get_adapter(dom or "")
    if adapter:
        try:
            analysis: Dict = adapter.analyze(text)  # type: ignore[attr-defined]
            if analysis.get("pattern"):
                pattern = analysis["pattern"]
                adapter_meta = {"name": adapter.name, "tags": analysis.get("tags", [])}
        except Exception:
            pattern = None

    # 2) λ-normal form extraction
    if pattern is None:
        pattern = extract_implication_pattern(nf)

    # 3) NL heuristic fallback
    if pattern is None:
        guess = _guess_nl_implication(text)
        if guess:
            pattern = guess
            # attach domain-derived adapter meta if we have a known domain
            if dom and adapter_meta is None:
                adapter_meta = {"name": dom, "tags": ["rel:heuristic"]}

    # 4) Last-resort idempotent pattern
    if pattern is None:
        if isinstance(term, LVar):
            pattern = f"{term.name} -> {term.name}"
        else:
            pattern = "X -> X"

    meta = {"nl": text, "lambda_nf": str(nf)}
    if adapter_meta:
        meta["adapter"] = adapter_meta

    return pipeline.run(pattern, meta=meta)
