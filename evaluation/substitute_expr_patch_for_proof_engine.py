# Add this to proof_engine.py if not present

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
    return Expr(expr.functor, substituted_args)
