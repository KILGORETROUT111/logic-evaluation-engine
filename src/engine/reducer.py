from __future__ import annotations
from typing import Any, Dict

class Var:
    __slots__=("name",)
    def __init__(self, name:str): self.name=name

class Lam:
    __slots__=("param","body")
    def __init__(self, param:Any, body:Any): self.param, self.body = param, body

class App:
    __slots__=("func","arg")
    def __init__(self, func:Any, arg:Any): self.func, self.arg = func, arg

def whnf(term: Any, env: Dict[str, Any] | None = None, fuel: int = 128) -> Any:
    """Weak-head normal form: small, safe, fuel-limited."""
    env = {} if env is None else env
    t = term
    while fuel > 0:
        fuel -= 1
        # (Lam x. body) v  => body[x:=v]
        if isinstance(t, App) and isinstance(t.func, Lam):
            v = t.arg
            t = subst(t.func.body, t.func.param, v)
            continue
        # head reduction under env
        if isinstance(t, Var) and t.name in env:
            t = env[t.name]
            continue
        # otherwise stop (WHNF)
        break
    return t

def subst(term: Any, name_or_var: Any, value: Any) -> Any:
    name = getattr(name_or_var, "name", name_or_var) if not isinstance(name_or_var,str) else name_or_var
    if isinstance(term, Var):
        return value if term.name == name else term
    if isinstance(term, Lam):
        # naive capture-ignoring (ok for smoke); improve later if needed
        if getattr(term.param, "name", term.param) == name:
            return term
        return Lam(term.param, subst(term.body, name, value))
    if isinstance(term, App):
        return App(subst(term.func, name, value), subst(term.arg, name, value))
    return term
