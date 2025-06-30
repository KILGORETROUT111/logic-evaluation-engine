from core.expressions import Functor, Var, Value
import json
from enum import Enum


class State(Enum):
    ALIVE = 1
    JAM = 2
    MEM = 3
    VAC = 4


def substitute(expr, var_name, value):
    if isinstance(expr, Var) and expr.name == var_name:
        return value
    elif isinstance(expr, Functor):
        return Functor(
            expr.name, [substitute(arg, var_name, value) for arg in expr.args]
        )
    else:
        return expr


def evaluate(expr, context, trace):
    def go(node):
        if isinstance(node, Functor):
            name = node.name
            args = node.args

            key = str(name) if not isinstance(name, list) else json.dumps(name)
            trace.setdefault(key, []).append(node)

            if name == "EX" and len(args) == 2:
                return State.ALIVE

            elif name == "EEX" and len(args) == 2:
                return State.VAC

            elif name == "SUB" and len(args) == 2:
                var, val = args
                trace.setdefault("BIND", []).append(f"{var}→{val}")
                context[str(var)] = val
                return State.ALIVE

            elif name == "MEM" and len(args) == 1:
                var = args[0]
                key = str(var)
                resolved = context.get(key)
                if resolved:
                    trace.setdefault("RESOLVE", []).append(f"{key}→{resolved}")
                    return go(resolved)
                else:
                    trace.setdefault("UNBOUND", []).append(str(var))
                    return State.VAC

            elif name == "LAM" and len(args) == 2:
                return node  # pass as value

            elif name == "APP" and len(args) == 2:
                fn = go(args[0])
                arg = go(args[1])

                if isinstance(fn, Functor) and fn.name == "LAM":
                    param = fn.args[0]
                    body = fn.args[1]
                    substituted = substitute(body, param.name, arg)
                    return go(substituted)
                else:
                    raise ValueError("APP expects first argument to be a LAM")

            elif name == "ROOT" or name == "NODE":
                result = None
                for arg in args:
                    result = go(arg)
                return result

            else:
                for arg in args:
                    go(arg)
                return State.VAC

        elif isinstance(node, Var):
            trace.setdefault("VAR", []).append(str(node))
            trace.setdefault("UNBOUND", []).append(str(node))
            return State.VAC

        elif isinstance(node, Value):
            trace.setdefault("VAL", []).append(str(node))
            return State.ALIVE

        else:
            raise ValueError(f"Unknown node type: {node}")

    final_state = go(expr)
    return final_state, trace


def evaluate_full(expr, context=None):
    if context is None:
        context = {}
    trace = {}
    final_state, trace = evaluate(expr, context, trace)
    return final_state, trace
