# unifier.py

def unify(expr1, expr2):
    if expr1.functor != expr2.functor or len(expr1.args) != len(expr2.args):
        return None
    substitution = {}
    for a, b in zip(expr1.args, expr2.args):
        # Variable detection: assume lowercase are variables
        if isinstance(a, str) and a.islower():
            substitution[a] = b
        elif a != b:
            return None
    return substitution
