import json
from datetime import datetime
from pathlib import Path

# Directory and file setup
out_dir = Path("out")
timestamp = datetime.now().strftime("%Y%m%d_%H%M")
filename = out_dir / f"evaluation_debug_patched_{timestamp}.py"

# Debug-patched evaluate.py content

from core.expressions import Functor, Var, Value
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
    return expr


def evaluate(expr, context, trace):
    def go(node):
        if isinstance(node, Functor):
            name = node.name
            args = node.args
            trace.setdefault(str(name), []).append(node)

            if name == "EX":
                return State.ALIVE
                trace.setdefault(str(name), []).append(node)

            elif name == "EEX":
                return State.VAC
                trace.setdefault(str(name), []).append(node)

            elif name == "SUB" and len(args) == 2:
                var, value = args
                context[var.name] = value
                key = str(name) if not isinstance(name, list) else json.dumps(name)
                trace.setdefault(key, []).append(node)

            elif name == "MEM" and len(args) == 1:
                var = args[0]
                val = context.get(var.name)
                if val is not None:
                    key = str(name) if not isinstance(name, list) else json.dumps(name)
                    trace.setdefault(key, []).append(node)

                else:
                    key = str(name) if not isinstance(name, list) else json.dumps(name)
                    trace.setdefault(key, []).append(node)

            elif name == "LAM" and len(args) == 2:
                key = str(name) if not isinstance(name, list) else json.dumps(name)
                trace.setdefault(key, []).append(node)

            elif name == "APP" and len(args) == 2:
                func = go(args[0])
                arg = go(args[1])
                trace.setdefault(str(name), []).append(node)

                if isinstance(func, Functor) and func.name == "LAM":
                    param = func.args[0]
                    body = func.args[1]
                    substituted = substitute(body, param.name, arg)
                    return go(substituted)
                else:
                    raise ValueError("APP expects a LAM as its first argument")

        elif isinstance(node, Var):
            key = str(name) if not isinstance(name, list) else json.dumps(name)
            trace.setdefault(key, []).append(node)

        elif isinstance(node, Value):
            return State.ALIVE

        return State.VAC

    final_state = go(expr)
    return final_state, trace


def evaluate_full(expr, context=None):
    if context is None:
        context = {}
    trace = {}
    final_state, trace = evaluate(expr, context, trace)
    return final_state, trace
