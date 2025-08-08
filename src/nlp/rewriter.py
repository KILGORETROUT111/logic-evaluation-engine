# src/nlp/rewriter.py
# LEE v3.0 — Phase 6
# Beta-reduction, alpha-rename, safe substitution on core AST

from typing import Set, Dict
from core.expressions import Variable, Lambda, Application, Quantifier, Expression

########################
# Free variables
########################
def free_vars(expr: Expression) -> Set[str]:
    if isinstance(expr, Variable):
        return {expr.name}
    if isinstance(expr, Lambda):
        return free_vars(expr.body) - {expr.param.name}
    if isinstance(expr, Application):
        return free_vars(expr.func) | free_vars(expr.arg)
    if isinstance(expr, Quantifier):
        return free_vars(expr.body) - {expr.var.name}
    return set()

########################
# Alpha-rename
########################
def alpha_rename(expr: Expression, old: str, new: str) -> Expression:
    if isinstance(expr, Variable):
        return Variable(new) if expr.name == old else expr
    if isinstance(expr, Lambda):
        p = expr.param.name
        if p == old:
            # rename binder and its body occurrences bound by this binder
            return Lambda(Variable(new), alpha_rename(expr.body, old, new))
        else:
            return Lambda(expr.param, alpha_rename(expr.body, old, new))
    if isinstance(expr, Application):
        return Application(alpha_rename(expr.func, old, new),
                           alpha_rename(expr.arg, old, new))
    if isinstance(expr, Quantifier):
        v = expr.var.name
        if v == old:
            return Quantifier(expr.kind, Variable(new), alpha_rename(expr.body, old, new))
        else:
            return Quantifier(expr.kind, expr.var, alpha_rename(expr.body, old, new))
    return expr

########################
# Capture-avoiding substitution: [x := value]expr
########################
def substitute(expr: Expression, x: str, value: Expression) -> Expression:
    if isinstance(expr, Variable):
        return value if expr.name == x else expr

    if isinstance(expr, Application):
        return Application(substitute(expr.func, x, value),
                           substitute(expr.arg, x, value))

    if isinstance(expr, Lambda):
        p = expr.param.name
        if p == x:
            # bound shadow, stop
            return expr
        # Avoid capture
        fvs_value = free_vars(value)
        if p in fvs_value:
            fresh = _fresh_name(p, free_vars(expr.body) | fvs_value | {x})
            renamed_body = alpha_rename(expr.body, p, fresh)
            return Lambda(Variable(fresh), substitute(renamed_body, x, value))
        else:
            return Lambda(expr.param, substitute(expr.body, x, value))

    if isinstance(expr, Quantifier):
        v = expr.var.name
        if v == x:
            return expr
        fvs_value = free_vars(value)
        if v in fvs_value:
            fresh = _fresh_name(v, free_vars(expr.body) | fvs_value | {x})
            renamed_body = alpha_rename(expr.body, v, fresh)
            return Quantifier(expr.kind, Variable(fresh), substitute(renamed_body, x, value))
        else:
            return Quantifier(expr.kind, expr.var, substitute(expr.body, x, value))

    return expr

def _fresh_name(base: str, avoid: Set[str]) -> str:
    k = 1
    cand = f"{base}_{k}"
    while cand in avoid:
        k += 1
        cand = f"{base}_{k}"
    return cand

########################
# Beta-reduction (one step)
########################
def beta_reduce_once(expr: Expression) -> Expression:
    if isinstance(expr, Application):
        # (λx. body) arg  →  body[x := arg]
        if isinstance(expr.func, Lambda):
            return substitute(expr.func.body, expr.func.param.name, expr.arg)
        # otherwise try to reduce func or arg
        new_func = beta_reduce_once(expr.func)
        if new_func is not expr.func:
            return Application(new_func, expr.arg)
        new_arg = beta_reduce_once(expr.arg)
        if new_arg is not expr.arg:
            return Application(expr.func, new_arg)
        return expr
    if isinstance(expr, Lambda):
        new_body = beta_reduce_once(expr.body)
        return Lambda(expr.param, new_body)
    if isinstance(expr, Quantifier):
        new_body = beta_reduce_once(expr.body)
        return Quantifier(expr.kind, expr.var, new_body)
    return expr

def normalize(expr: Expression, fuel: int = 128) -> Expression:
    """Repeated beta-reduction until no change or fuel exhausted."""
    cur = expr
    for _ in range(fuel):
        nxt = beta_reduce_once(cur)
        if nxt == cur:
            return cur
        cur = nxt
    return cur
