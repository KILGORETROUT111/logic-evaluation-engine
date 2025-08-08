# src/nlp/named_entities.py
# LEE v3.0 — Phase 6
# Simple surface → Variable mapping with hygiene & canonicalization.

import re
from typing import Dict, Iterable, List, Tuple
from core.expressions import Variable

# Basic normalization: lowercase, spaces→_, strip punctuation, collapse repeats
_PUNCT = re.compile(r"[^\w\s-]", flags=re.UNICODE)
_WS = re.compile(r"\s+")

def normalize_token(s: str) -> str:
    s = s.strip()
    s = _PUNCT.sub(" ", s)
    s = _WS.sub(" ", s)
    s = s.lower().replace(" ", "_")
    # ensure it starts with a letter to be a valid variable in most printers
    if not s or not s[0].isalpha():
        s = f"v_{s}" if s else "v"
    return s

def to_variable(s: str) -> Variable:
    return Variable(normalize_token(s))

def extract_entities_from_text(text: str) -> List[str]:
    """
    Very simple extractor:
      - sequences of letters/digits/underscores that start with a letter
      - also respects dashed compounds (e.g., 'covid-19')
    For production, plug a proper NER; this is intentionally minimal.
    """
    # Keep words and dashed compounds; drop obvious stop tokens
    candidates = re.findall(r"[A-Za-z][A-Za-z0-9_-]*", text)
    # De-duplicate while preserving order
    seen, out = set(), []
    for c in candidates:
        key = c.lower()
        if key not in seen:
            seen.add(key)
            out.append(c)
    return out

def map_entities(entities: Iterable[str]) -> Dict[str, Variable]:
    """
    Map surface strings → hygienic Variables.
    """
    mapping: Dict[str, Variable] = {}
    used: set = set()
    for ent in entities:
        base = normalize_token(ent)
        name = base
        # ensure uniqueness
        k = 1
        while name in used:
            k += 1
            name = f"{base}_{k}"
        used.add(name)
        mapping[ent] = Variable(name)
    return mapping

def entities_from_text(text: str) -> Dict[str, Variable]:
    """Convenience: extract entities then map to Variables."""
    ents = extract_entities_from_text(text)
    return map_entities(ents)
