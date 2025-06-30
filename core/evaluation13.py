"""
Evaluation logic for symbolic logic engine.
"""

from core.expressions import Functor, Var, Value, State


def substitute(expr, var, replacement):
    if isinstance(expr, Var):
        return replacement if expr.name == var else expr
    elif isinstance(expr, Functor):
        # If lambda shadows the variable, skip substitution
        if expr.name == "LAM" and expr.args[0].name == var:
            return expr
        return Functor(expr.name, [substitute(arg, var, replacement) for arg in expr.args])
    return expr


def evaluate(expr, context=None, trace=None):
    context = context or {}
    trace = trace or {}

    def go(node):
        if isinstance(node, Functor):
            name = node.name
            args = node.args

        try:
            trace.setdefault(str(node.name), []).append(node)
        except Exception as e:
            print("⚠️ Trace error:", e)


            if name == "EX":
                if len(args) != 2:
                    raise ValueError("EX expects two arguments")
                left = go(args[0])
                right = go(args[1])
                if isinstance(left, Value) or isinstance(left, Var):
                    trace.setdefault("ALIVE", []).append(left)
                    return State.ALIVE
                return State.VAC

            elif name == "EEX":
                if len(args) != 2:
                    raise ValueError("EEX expects two arguments")
                go(args[0])
                go(args[1])
                return State.VAC

            elif name == "JAM":
                trace.setdefault("JAM", []).append(node)
                return State.JAM

            elif name == "MEM":
                trace.setdefault("MEM", []).append(node)
                return State.MEM

            elif name == "SUB":
                if len(args) != 2:
                    raise ValueError("SUB expects two arguments")
                var = args[0]
                val = go(args[1])
                if not isinstance(var, Var):
                    raise ValueError("SUB first argument must be a Var")
                context[var.name] = val
                trace.setdefault("BIND", []).append(Functor("→", [var, val]))
                return State.VAC

            elif name == "LAM":
                return node

            elif name == "APP":
                if len(args) != 2:
                    raise ValueError("APP expects two arguments")
                func = go(args[0])
                arg = go(args[1])
                if not isinstance(func, Functor) or func.name != "LAM":
                    raise ValueError("APP expects first argument to be a LAM")
                param = func.args[0]
                body = func.args[1]
                if not isinstance(param, Var):
                    raise ValueError("LAM parameter must be a Var")
                substituted = substitute(body, param.name, arg)
                return go(substituted)

            elif isinstance(node, Var):
                val = context.get(node.name)
                if val is not None:
                    trace.setdefault("RESOLVE", []).append(Functor("→", [node, val]))
                    return val
                trace.setdefault("UNBOUND", []).append(node)
                return node

            elif isinstance(node, Value):
                return node

            elif isinstance(node, State):
                return node

            raise ValueError(f"Unknown node type: {node}")

        final_state = go(expr)
        return final_state, trace


def evaluate_full(expr, context=None):
    return evaluate(expr, context or {}, {})