
from core.expressions import Lambda, Variable

def alpha_rename(expr, bound_vars=None, counter=None):
    if bound_vars is None:
        bound_vars = set()
    if counter is None:
        counter = {"count": 0}

    if isinstance(expr, Variable):
        return Variable(expr.name)

    elif isinstance(expr, Lambda):
        original_var = expr.var
        if original_var in bound_vars:
            new_var = f"{original_var}_r{counter['count']}"
            counter["count"] += 1
        else:
            new_var = f"{original_var}_r"

        renamed_body = alpha_rename(
            substitute(expr.body, original_var, new_var),
            bound_vars | {new_var},
            counter
        )
        return Lambda(new_var, renamed_body)

    else:
        return expr

def substitute(expr, old_name, new_name):
    if isinstance(expr, Variable):
        return Variable(new_name) if expr.name == old_name else expr

    elif isinstance(expr, Lambda):
        if expr.var == old_name:
            return Lambda(expr.var, expr.body)  # shadowed, no substitution
        else:
            return Lambda(expr.var, substitute(expr.body, old_name, new_name))

    return expr
