from core.lee_event import LEEEvent, EventPhase
from core.expressions import IfThenElse, BinaryOp
from core.state import State
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
        trace.append(LEEEvent.from_dict({"phase": "LITERAL", "value": expr.value}))
        return State.ALIVE, trace

    if isinstance(expr, Variable):
        val = env.get(expr.name)
        trace.append(LEEEvent.from_dict({"phase": "VARIABLE", "name": expr.name, "value": val}))
        if val is None:
            return State.JAM, trace
        return evaluate_full(val, env, trace)

    if isinstance(expr, Lambda):
        trace.append(LEEEvent.from_dict({"phase": "LAMBDA", "var": expr.var, "body": repr(expr.body)}))
        return (expr, env.copy()), trace  # Return closure: lambda and its env

    if isinstance(expr, Application):
        trace.append(LEEEvent.from_dict({"phase": "APPLICATION", "func": repr(expr.func), "arg": repr(expr.arg)}))
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
        trace.append(LEEEvent.from_dict({"phase": "DEFINE", "name": expr.name, "value": repr(expr.value)}))
        return State.ALIVE, trace

    if isinstance(expr, Memory):
        val = env.get(expr.var)
        trace.append(LEEEvent.from_dict({"phase": "MEMORY", "var": expr.var, "value": val}))
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
        
# Add to evaluate_full after Quantifier:

    if isinstance(expr, IfThenElse):
        cond_result, trace = evaluate_full(expr.condition, env, trace)
        if cond_result == State.ALIVE:
            return evaluate_full(expr.then_branch, env, trace)
        else:
            return evaluate_full(expr.else_branch, env, trace)

    if isinstance(expr, BinaryOp):
        left_result, trace = evaluate_full(expr.left, env, trace)
        right_result, trace = evaluate_full(expr.right, env, trace)
        if expr.op == "==":
            return (State.ALIVE if left_result == right_result else State.JAM), trace
        if expr.op == "*":
            try:
                result_val = left_result.value * right_result.value
                return Literal(result_val), trace
            except Exception:
                return State.JAM, trace
        return State.JAM, trace

    trace.append(LEEEvent.from_dict({"phase": "UNKNOWN", "expr": repr(expr)}))
    return State.JAM, trace

import json
from typing import List
from core.lee_event import LEEEvent, EventPhase


def emit_trace_to_json(trace: List[LEEEvent], filepath: str = "trace_output.json"):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump([event.to_dict() for event in trace], f, indent=2)
