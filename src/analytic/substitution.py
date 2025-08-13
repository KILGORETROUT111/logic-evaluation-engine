from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Iterable, List, Tuple, Union

# --- Term AST ---------------------------------------------------------------

@dataclass(frozen=True)
class Var:
    name: str
    def __str__(self) -> str: return self.name

@dataclass(frozen=True)
class Const:
    name: str
    def __str__(self) -> str: return self.name

@dataclass(frozen=True)
class Fun:
    name: str
    args: Tuple["Term", ...]
    def __str__(self) -> str:
        if not self.args: return self.name
        return f"{self.name}({', '.join(map(str, self.args))})"

Term = Union[Var, Const, Fun]

# --- Substitution -----------------------------------------------------------

class Subst:
    """Immutable-ish substitution mapping Var -> Term with apply/compose."""
    def __init__(self, mapping: Dict[Var, Term] | None = None) -> None:
        self._m: Dict[Var, Term] = {} if mapping is None else dict(mapping)

    def __repr__(self) -> str:
        items = ", ".join(f"{v}↦{t}" for v, t in self._m.items())
        return f"Subst({{{items}}})"

    def get(self, v: Var, default: Term | None = None) -> Term | None:
        return self._m.get(v, default)

    def items(self): return self._m.items()

    def apply(self, t: Term) -> Term:
        if isinstance(t, Var):
            r = self._m.get(t)
            return self.apply(r) if r is not None else t
        if isinstance(t, Const):
            return t
        # Fun
        return Fun(t.name, tuple(self.apply(a) for a in t.args))

    def extend(self, v: Var, t: Term) -> "Subst":
        m = dict((k, self.apply(vv)) for k, vv in self._m.items())
        m[v] = self.apply(t)
        return Subst(m)

    def compose(self, other: "Subst") -> "Subst":
        """self ∘ other: apply self after other."""
        m = {v: self.apply(t) for v, t in other.items()}
        for v, t in self._m.items():
            if v not in m:
                m[v] = t
        return Subst(m)

# --- Unification (occurs-check) --------------------------------------------

class UnifyError(Exception): pass

def occurs(v: Var, t: Term, σ: Subst) -> bool:
    t = σ.apply(t)
    if t == v: return True
    if isinstance(t, Fun):
        return any(occurs(v, a, σ) for a in t.args)
    return False

def unify(t1: Term, t2: Term, σ: Subst | None = None) -> Subst:
    σ = Subst() if σ is None else σ
    t1, t2 = σ.apply(t1), σ.apply(t2)

    if t1 == t2:
        return σ

    # variable cases
    if isinstance(t1, Var):
        if occurs(t1, t2, σ): raise UnifyError(f"occurs: {t1} in {t2}")
        return σ.extend(t1, t2)
    if isinstance(t2, Var):
        if occurs(t2, t1, σ): raise UnifyError(f"occurs: {t2} in {t1}")
        return σ.extend(t2, t1)

    # constants
    if isinstance(t1, Const) and isinstance(t2, Const):
        if t1.name != t2.name: raise UnifyError(f"const clash: {t1} vs {t2}")
        return σ

    # functions
    if isinstance(t1, Fun) and isinstance(t2, Fun):
        if t1.name != t2.name or len(t1.args) != len(t2.args):
            raise UnifyError(f"fun clash: {t1} vs {t2}")
        for a, b in zip(t1.args, t2.args):
            σ = unify(a, b, σ)
        return σ

    raise UnifyError(f"clash: {t1} vs {t2}")
