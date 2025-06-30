from core.expressions import Functor, Var, Value
from enum import Enum, auto

class State(Enum):
    ALIVE = auto()
    JAM = auto()
    MEM = auto()
    VAC = auto()

def substitute(expr, var_name, replacement):
    if isinstance(expr, Var):
        return replacement if expr.name == var_name else expr
    elif isinstance(expr, Functor):
        return Functor(expr.name, [substitute(arg, var_name, replacement) for arg in expr.args])
    else:
        return expr

def evaluate(expr, context, trace):
    def go(node):
        if isinstance(node, Functor):
            name = node.name
            if not isinstance(name, str):
                raise ValueError(f"⚠️ Functor name is not a string: {name}")
            trace.setdefault(name, []).append(node)

            if name == "SUB" and len(args) == 2:
                var = args[0]
                val = args[1]
                if isinstance(var, Var):
                    context[var.name] = val
                    trace.setdefault("BIND", []).append(f"{var.name}→{val}")
                    return State.ALIVE
                else:
                    raise ValueError("SUB expects a variable as first argument")

            elif name == "MEM" and len(args) == 1:
                var = args[0]
                trace.setdefault("RESOLVE", []).append(f"{var.name}→{context.get(var.name)}")
                resolved = context.get(var.name)
                if resolved is not None:
                    return go(resolved)
                else:
                    trace.setdefault("UNBOUND", []).append(var)
                    return State.VAC

            elif name == "EX" and len(args) == 2:
                return State.ALIVE

            elif name == "EEX" and len(args) == 2:
                return State.VAC

            elif name == "APP" and len(args) == 2:
                lam_expr = go(args[0])
                applied_arg = go(args[1])
                if isinstance(args[0], Functor) and args[0].name == "LAM":
                    param = args[0].args[0]
                    body = args[0].args[1]
                    if isinstance(param, Var):
                        substituted = substitute(body, param.name, applied_arg)
                        return go(substituted)
                    else:
                        raise ValueError("LAM first argument must be a variable")
                else:
                    raise ValueError("APP expects first argument to be a LAM")

            elif name == "LAM" and len(args) == 2:
                return State.ALIVE

            else:
                return State.VAC

        elif isinstance(node, Var):
            trace.setdefault("VAR", []).append(node)
            trace.setdefault("UNBOUND", []).append(node)
            return State.ALIVE

        elif isinstance(node, Value):
            trace.setdefault("VAL", []).append(node)
            return State.ALIVE

        else:
            raise ValueError(f"Unknown node type: {node}")

    final_state = go(expr)
    return final_state, trace

def evaluate_full(expr, context=None):
    if context is None:
        context = {}
    trace = {}
    return evaluate(expr, context, trace)