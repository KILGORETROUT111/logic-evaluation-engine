from enum import Enum
from core.expressions import Functor, Var, Value

class State(Enum):
    ALIVE = 1
    JAM = 2
    MEM = 3
    VAC = 4

def substitute(expr, var_name, replacement):
    if isinstance(expr, Var):
        return replacement if expr.name == var_name else expr
    elif isinstance(expr, Functor):
        return Functor(expr.name, [substitute(arg, var_name, replacement) for arg in expr.args])
    return expr  # Value or unknown stays unchanged

def evaluate(expr, context=None, trace=None):
    if context is None:
        context = {}
    if trace is None:
        trace = {}

    def go(node):
        if isinstance(node, State):
            return node

        if isinstance(node, Functor):
            name = node.name
            args = node.args

            key = str(name)
            trace.setdefault(key, []).append(node)

            # Handle known functors
            if name == "EX" and len(args) == 2:
                return State.ALIVE

            elif name == "EEX" and len(args) == 2:
                return State.VAC

            elif name == "JAM":
                return State.JAM

            elif name == "MEM":
                if len(args) == 1 and isinstance(args[0], Var):
                    var_name = args[0].name
                    value = context.get(var_name)
                    if value:
                        trace.setdefault("RESOLVE", []).append(f"{var_name}→{value}")
                        return go(value)
                    else:
                        trace.setdefault("UNBOUND", []).append(args[0])
                        return State.VAC

            elif name == "SUB" and len(args) == 2 and isinstance(args[0], Var):
                var_name = args[0].name
                bound_val = args[1]
                context[var_name] = bound_val
                trace.setdefault("BIND", []).append(f"{var_name}→{bound_val}")
                return State.MEM

            elif name == "ROOT" or name == "NODE":
                for arg in args:
                    go(arg)
                return State.VAC

            elif name == "APP" and len(args) == 2:
                func = go(args[0])
                arg = go(args[1])
                if isinstance(func, Functor) and func.name == "LAM":
                    param = func.args[0]
                    body = func.args[1]
                    substituted = substitute(body, param.name, arg)
                    return go(substituted)
                else:
                    raise ValueError("APP expects first argument to be a LAM")

            elif name == "LAM" and len(args) == 2:
                return node  # Preserve lambda form as-is for APP

        elif isinstance(node, Var):
            trace.setdefault("VAR", []).append(node)
            return context.get(node.name, State.VAC)

        elif isinstance(node, Value):
            trace.setdefault("VAL", []).append(node)
            return State.ALIVE

        raise ValueError(f"Unknown node type: {node}")

    final_state = go(expr)
    return final_state, trace

def evaluate_full(expr, context=None):
    trace = {}
    final_state, trace = evaluate(expr, context, trace)
    return final_state, trace
