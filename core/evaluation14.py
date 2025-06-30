from core.expressions import Functor, Var, Value, State
import json


def substitute(expr, var, replacement):
    if isinstance(expr, Var):
        return replacement if expr.name == var else expr

    if isinstance(expr, Functor):
        if expr.name == "LAM":
            param = expr.args[0].name
            if param == var:
                return expr  # Shadowing: don't substitute
        return Functor(
            expr.name, [substitute(arg, var, replacement) for arg in expr.args]
        )

    return expr


def evaluate(expr, context=None, trace=None):
    if context is None:
        context = {}
    if trace is None:
        trace = {}

    def go(node):
        if isinstance(node, Value):
            return State.ALIVE

        elif isinstance(node, Var):
            val = context.get(node.name)
            if val is not None:
                trace.setdefault("RESOLVE", []).append(f"{node.name}→{val}")
                return val if isinstance(val, State) else State.ALIVE
            trace.setdefault("UNBOUND", []).append(str(node))
            return State.VAC

        elif isinstance(node, Functor):
            name = node.name
            args = node.args

            # Special case: LAM node is a lambda closure
            if name == "LAM":
                trace.setdefault("LAM", []).append(str(node))
                return node

            # Special case: apply lambda to an argument
        elif name == "APP" and len(args) == 2:
            func = go(args[0])  # May resolve to a LAM
            arg = go(args[1])

            if isinstance(func, Var):
                resolved = context.get(func.name)
                if isinstance(resolved, Functor) and resolved.name == "LAM":
                    param, body = resolved.args
                    return go(substitute(body, param.name, arg))
                else:
                    raise ValueError("APP first argument resolves to non-LAM")

            if not (isinstance(func, Functor) and func.name == "LAM"):
                raise ValueError("APP expects first argument to be a LAM or resolvable Var")

            param, body = func.args
            return go(substitute(body, param.name, arg))
   

            # EX(x, JAM) → check x is bound
            if name == "EX" and len(args) == 2:
                trace.setdefault("EX", []).append(str(node))
                return go(args[0])

            # EEX(x, JAM) → x unbound
            if name == "EEX" and len(args) == 2:
                trace.setdefault("EEX", []).append(str(node))
                var = args[0]
                if isinstance(var, Var) and var.name not in context:
                    return State.VAC
                return State.ALIVE

            # SUB(x, φ)
            if name == "SUB" and len(args) == 2:
                trace.setdefault("BIND", []).append(f"{args[0]}→{args[1]}")
                if isinstance(args[0], Var):
                    context[args[0].name] = args[1]
                return State.ALIVE

            # MEM(x) looks up context
            if name == "MEM" and len(args) == 1:
                trace.setdefault("MEM", []).append(str(node))
                val = context.get(args[0].name)
                return (
                    val if isinstance(val, State) else State.ALIVE if val else State.VAC
                )

            # Otherwise: fallback
            trace.setdefault(name, []).append(str(node))
            for arg in args:
                go(arg)
            return State.ALIVE

        else:
            raise ValueError(f"Unknown node type: {node}")

    final_state = go(expr)
    return final_state, trace


def evaluate_full(expr, context=None):
    return evaluate(expr, context or {}, {})