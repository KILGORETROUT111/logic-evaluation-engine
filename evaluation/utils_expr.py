
def substitute_expr(expr, substitution):
    """
    Recursively apply substitution to all args of the expression.
    """
    substituted_args = []
    for arg in expr.args:
        if isinstance(arg, str) and arg in substitution:
            substituted_args.append(substitution[arg])
        else:
            substituted_args.append(arg)
    return expr.__class__(expr.functor, substituted_args)
