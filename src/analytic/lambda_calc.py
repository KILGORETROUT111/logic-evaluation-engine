from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Set, Tuple, Union

@dataclass(frozen=True)
class LVar:
    name: str
    def __str__(self): return self.name

@dataclass(frozen=True)
class Lam:
    param: str
    body: "LTerm"
    def __str__(self): return f"(λ{self.param}.{self.body})"

@dataclass(frozen=True)
class App:
    fn: "LTerm"
    arg: "LTerm"
    def __str__(self): return f"({self.fn} {self.arg})"

LTerm = Union[LVar, Lam, App]

# --- utilities --------------------------------------------------------------

def free_vars(t: LTerm) -> Set[str]:
    if isinstance(t, LVar): return {t.name}
    if isinstance(t, App):  return free_vars(t.fn) | free_vars(t.arg)
    # Lam
    return free_vars(t.body) - {t.param}

def _gensym(used: Set[str], base: str) -> str:
    i, name = 0, base
    while name in used:
        i += 1
        name = f"{base}_{i}"
    return name

def alpha_convert(t: LTerm, old: str, new: str) -> LTerm:
    """Rename bound variable old -> new (capture-safe if new is fresh)."""
    if isinstance(t, LVar):
        return LVar(new) if t.name == old else t
    if isinstance(t, App):
        return App(alpha_convert(t.fn, old, new), alpha_convert(t.arg, old, new))
    if t.param == old:
        return Lam(new, alpha_convert(t.body, old, new))
    return Lam(t.param, alpha_convert(t.body, old, new))

def substitute(t: LTerm, var: str, repl: LTerm) -> LTerm:
    """Capture-avoiding substitution [var := repl]t."""
    if isinstance(t, LVar):
        return repl if t.name == var else t
    if isinstance(t, App):
        return App(substitute(t.fn, var, repl), substitute(t.arg, var, repl))
    if t.param == var:
        # var is bound here; shadowed
        return t
    # avoid capture: if param occurs free in repl, rename param
    if t.param in free_vars(repl):
        fresh = _gensym(free_vars(t.body) | free_vars(repl) | {var}, t.param)
        t = alpha_convert(t, t.param, fresh)
    return Lam(t.param, substitute(t.body, var, repl))

def beta_step(t: LTerm) -> Tuple[LTerm, bool]:
    """One normal-order β step; returns (term, changed?)."""
    # (λx.M) N → M[x:=N]
    if isinstance(t, App) and isinstance(t.fn, Lam):
        return substitute(t.fn.body, t.fn.param, t.arg), True
    # otherwise, reduce leftmost-outermost
    if isinstance(t, App):
        t1, ch = beta_step(t.fn)
        if ch: return App(t1, t.arg), True
        t2, ch = beta_step(t.arg)
        if ch: return App(t.fn, t2), True
        return t, False
    if isinstance(t, Lam):
        body, ch = beta_step(t.body)
        if ch: return Lam(t.param, body), True
        return t, False
    # LVar
    return t, False

def beta_normal_form(t: LTerm, max_steps: int = 10_000) -> LTerm:
    cur = t
    for _ in range(max_steps):
        cur, changed = beta_step(cur)
        if not changed:
            return cur
    raise RecursionError("β-reduction did not terminate within max_steps")
