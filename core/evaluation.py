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
