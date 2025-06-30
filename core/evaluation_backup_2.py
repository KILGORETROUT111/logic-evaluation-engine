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
        return Functor(expr.name, [substitute(arg, var_name, value) for arg in expr.args])
    return expr

def evaluate(expr, context, trace):
    def go(node):
        if isinstance(node, Functor):
                print("🔎 TRACE KEY DEBUG:", node.name, type(node.name))
                trace.setdefault(str(node.name), []).append(node)

                args = node.args

        if name == "EX":
            if len(args) != 2:
                raise ValueError(f"EX expects 2 args, got {args}")
            return State.ALIVE

        elif name == "EEX":
            return State.VAC

        elif name == "MEM":
            return State.MEM

        elif name == "SUB":
            if len(args) != 2:
                raise ValueError("SUB requires 2 arguments")
            varname = args[0].name if isinstance(args[0], Var) else str(args[0])
            context[varname] = args[1]
            trace.setdefault("BIND", []).append(f"{varname}→{args[1]}")
            return State.ALIVE

        elif name == "LAM":
            return node  # Return the lambda expression for APP

        elif name == "APP":
            if len(args) != 2:
                raise ValueError("APP requires function and argument")
            func = go(args[0])
            if not isinstance(func, Functor) or func.name != "LAM":
                raise ValueError("APP expects first argument to be a LAM")

            param = func.args[0]
            body = func.args[1]
            applied_arg = go(args[1])
            if isinstance(param, Var):
                substituted = substitute(body, param.name, applied_arg)
                return go(substituted)
            else:
                raise ValueError("LAM param must be a Var")

        elif name == "ROOT" or name == "NODE":
            for arg in args:
                go(arg)
            return State.ALIVE

        else:
            for arg in args:
                go(arg)
            return State.VAC

        elif isinstance(node, Var):
            trace.setdefault("VAR", []).append(str(node))
            val = context.get(node.name)
            if val:
                trace.setdefault("RESOLVE", []).append(f"{node.name}→{val}")
                return go(val)
            else:
                trace.setdefault("UNBOUND", []).append(str(node))
                return State.ALIVE

        elif isinstance(node, Value):
            trace.setdefault("VALUE", []).append(str(node))
            return State.ALIVE

        else:
            raise ValueError(f"Unsupported node type: {node}")

    final_state = go(expr)
    return final_state, trace

    def evaluate_full(expr, context=None):
        if context is None:
            context = {}
        trace = {}
        return evaluate(expr, context, trace)