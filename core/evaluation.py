#This file is part of The Logic Evaluation Engine.
#Logic Evaluation Engine is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
#Logic Evaluation Engine is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#You should have received a copy of the GNU General Public License along with Logic Evaluation Engine.
#If not, see <https://www.gnu.org/licenses/>.

from core.expressions import Functor, Value, Var, State

def evaluate_full(expr, context=None):
    trace = {}
    context = context or {}
    try:
        final_state = evaluate(expr, context, trace)
    except Exception as e:
        print("❌ Evaluation error:", e)
        final_state = None
    if final_state is None:
        print("⚠️ Evaluation returned None")
    return final_state, trace

def evaluate(expr, context, trace):
    def go(node):
        if isinstance(node, Functor):
            name = node.name
            args = node.args
            trace.setdefault(str(name), []).append(node)

            if name == "EX" and len(args) == 2:
                left = go(args[0])
                right = go(args[1])
                if isinstance(left, Value) and left.val == 0:
                    return State.VAC
                return State.ALIVE

            elif name == "EEX" and len(args) == 2:
                left = go(args[0])
                right = go(args[1])
                return State.VAC if left == State.ALIVE else State.ALIVE

            elif name == "SUB" and len(args) == 2:
                var, val = args
                if isinstance(var, Var):
                    context[var.name] = val
                    trace.setdefault("BIND", []).append(f"{var.name}→{val}")
                    return val
                return State.JAM

            elif name == "MEM" and len(args) == 1:
                key = args[0]
                if isinstance(key, Var) and key.name in context:
                    return context[key.name]
                trace.setdefault("UNBOUND", []).append(key)
                return State.VAC

            elif name == "APP" and len(args) == 2:
                func = go(args[0])
                arg = go(args[1])
                if isinstance(func, Functor) and func.name == "LAM":
                    param = func.args[0]
                    body = func.args[1]
                    if isinstance(param, Var):
                        substituted = substitute(body, param.name, arg)
                        return go(substituted)
                    else:
                        raise ValueError("LAM must bind a Var")
                else:
                    raise ValueError("APP expects first argument to be a LAM")

            elif name == "LAM" and len(args) == 2:
                return Functor("LAM", args)

            elif name == "ROOT":
                results = [go(arg) for arg in args]
                return results[-1] if results else None

            elif name == "NODE" and len(args) >= 3:
                return go(args[0])

        elif isinstance(node, Value):
            return node

        elif isinstance(node, Var):
            trace.setdefault("VAR", []).append(node)
            return context.get(node.name, State.VAC)

        elif isinstance(node, State):
            return node

        else:
            raise ValueError(f"Unknown node type: {node}")

    return go(expr)

def substitute(expr, var_name, replacement):
    if isinstance(expr, Var):
        return replacement if expr.name == var_name else expr
    elif isinstance(expr, Functor):
        return Functor(expr.name, [substitute(arg, var_name, replacement) for arg in expr.args])
    return expr
