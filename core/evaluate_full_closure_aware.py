from core.states import State
from core.expressions import (
    Literal, Variable, Lambda, Application,
    Substitution, Define, Memory, Quantifier
)

def evaluate_full(expr, env=None, trace=None):
    if env is None:
        env = {}
    if trace is None:
        trace = []

    if isinstance(expr, Literal):
        trace.append({"phase": "LITERAL", "value": expr.value})
        return State.ALIVE, trace

    if isinstance(expr, Variable):
        val = env.get(expr.name)
        trace.append({"phase": "VARIABLE", "name": expr.name, "value": val})
        if val is None:
            return State.JAM, trace
        return evaluate_full(val, env, trace)

    if isinstance(expr, Lambda):
        trace.append({"phase": "LAMBDA", "var": expr.var, "body": repr(expr.body)})
        return (expr, env.copy()), trace  # Return closure: lambda and its env

    if isinstance(expr, Application):
        trace.append({"phase": "APPLICATION", "func": repr(expr.func), "arg": repr(expr.arg)})
        func_result, trace = evaluate_full(expr.func, env, trace)
        if isinstance(func_result, tuple) and isinstance(func_result[0], Lambda):
            func, closure_env = func_result
            local_env = closure_env.copy()
            local_env[func.var] = expr.arg
            return evaluate_full(func.body, local_env, trace)
        else:
            return State.JAM, trace

    if isinstance(expr, Substitution):
        local_env = env.copy()
        local_env[expr.var] = expr.value
        return evaluate_full(expr.body, local_env, trace)

    if isinstance(expr, Define):
        env[expr.name] = expr.value
        trace.append({"phase": "DEFINE", "name": expr.name, "value": repr(expr.value)})
        return State.ALIVE, trace

    if isinstance(expr, Memory):
        val = env.get(expr.var)
        trace.append({"phase": "MEMORY", "var": expr.var, "value": val})
        if val is None:
            return State.JAM, trace
        return evaluate_full(val, env, trace)

    if isinstance(expr, Quantifier):
        results = []
        for val in [1, 2, 3]:
            local_env = env.copy()
            local_env[expr.var] = Literal(val)
            result, _ = evaluate_full(expr.body, local_env)
            results.append(result)

        if expr.universal:
            return (State.ALIVE if all(r == State.ALIVE for r in results) else State.JAM), trace
        else:
            return (State.ALIVE if any(r == State.ALIVE for r in results) else State.JAM), trace

    trace.append({"phase": "UNKNOWN", "expr": repr(expr)})
    return State.JAM, trace
