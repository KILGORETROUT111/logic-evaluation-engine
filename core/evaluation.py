from core.state import State
from core.expressions import Value, Var, Functor

def evaluate_full(expr, context=None, phase=1):
    if context is None:
        context = {}
    trace = {"JAM": [], "MEM": [], "ALIVE": [], "VAC": []}

    def eval_inner(e):
        if isinstance(e, Value):
            trace["ALIVE"].append(e)
            return State.ALIVE
        if isinstance(e, Var):
            if phase == 0:
                trace["VAC"].append(e)
                return State.VAC
            if e.name in context:
                trace["ALIVE"].append(e)
                return State.ALIVE
            else:
                trace["VAC"].append(e)
                return State.VAC
        if isinstance(e, Functor):
            op = e.name.upper()
            if op == "JAM":
                trace["JAM"].append(e)
                return State.JAM
            if op == "MEM":
                trace["MEM"].append(e)
                return State.MEM
            if op == "VAC":
                trace["VAC"].append(e)
                return State.VAC
            if op == "EX":
                states = [eval_inner(c) for c in e.children]
                if any(s == State.JAM for s in states):
                    trace["JAM"].append(e)
                    return State.JAM
                if any(s == State.ALIVE for s in states):
                    trace["ALIVE"].append(e)
                    return State.ALIVE
                if any(s == State.MEM for s in states):
                    trace["MEM"].append(e)
                    return State.MEM
                trace["VAC"].append(e)
                return State.VAC
            if op == "EEX":
                states = [eval_inner(c) for c in e.children]
                if any(s == State.JAM for s in states):
                    trace["JAM"].append(e)
                    return State.JAM
                if any(s == State.MEM for s in states):
                    trace["MEM"].append(e)
                    return State.MEM
                if any(s == State.ALIVE for s in states):
                    trace["ALIVE"].append(e)
                    return State.ALIVE
                trace["VAC"].append(e)
                return State.VAC
            states = [eval_inner(c) for c in e.children]
            if any(s == State.JAM for s in states):
                trace["JAM"].append(e)
                return State.JAM
            if all(s == State.ALIVE for s in states):
                trace["ALIVE"].append(e)
                return State.ALIVE
            if any(s == State.MEM for s in states):
                trace["MEM"].append(e)
                return State.MEM
            if any(s == State.ALIVE for s in states):
                trace["ALIVE"].append(e)
                return State.ALIVE
            trace["VAC"].append(e)
            return State.VAC
        trace["VAC"].append(e)
        return State.VAC

    final_state = eval_inner(expr)
    return final_state, trace
=======
from core.expressions import Functor, Var, Value
from enum import Enum

class State(Enum):
    JAM = 1
    MEM = 2
    ALIVE = 3
    VAC = 4

def evaluate(expr, context, trace):
    def go(node):
        if isinstance(node, Functor):
            name = node.name
            trace.setdefault(name, []).append(node)
            if not hasattr(node, 'args'):
                raise ValueError(f"Functor {name} has no 'args' attribute! {node}")
            for arg in node.args:
                go(arg)
            if name == "JAM":
                return State.JAM
            elif name == "MEM":
                return State.MEM
            elif name == "EX":
                return State.ALIVE
            elif name == "VAC":
                return State.VAC
            return State.VAC
        elif isinstance(node, Var):
            trace["ALIVE"].append(node)
            return State.ALIVE
        elif isinstance(node, Value):
            trace["ALIVE"].append(node)
            return State.ALIVE
        else:
            raise ValueError(f"Unknown node type: {node}")

    final_state = go(expr)
    return final_state, trace

def evaluate_full(expr, context):
    trace = {"JAM": [], "MEM": [], "ALIVE": [], "VAC": []}
    return evaluate(expr, context, trace)
79041d6 (Initial commit with CLI + SUB support)
