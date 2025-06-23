# core/parser.py

from core.expressions import Functor, Value, Var

def parse_expression(expr):
    if isinstance(expr, list):
        if not expr:
            raise ValueError("Empty list cannot be parsed as a Functor")
        head = expr[0]
        args = expr[1:]
        # Recursively build children
        parsed_args = [parse_expression(arg) for arg in args]
        return Functor(str(head).upper(), parsed_args)
    
    elif isinstance(expr, dict) and "value" in expr:
        return Value(expr["value"])
    
    elif isinstance(expr, (int, float)):  # ✅ ADD THIS
        return Value(expr)
    
    elif isinstance(expr, str):
        upper = expr.upper()
        known = {"EX", "EEX", "MEM", "JAM", "VAC", "SUB", "ROOT", "NODE"}
        if upper in known:
            return Functor(upper, [])
        else:
            return Var(expr)

    else:
        raise ValueError(f"Unsupported expression type: {type(expr)}")