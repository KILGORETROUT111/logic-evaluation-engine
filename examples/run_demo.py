import sys
import os

CURRENT = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.abspath(os.path.join(CURRENT, ".."))
sys.path.insert(0, PARENT)

from core.expressions import Functor, Value, Var
from core.evaluation import evaluate_full


context = {"x": 1, "z": 2}
expr = Functor("Root", [
    Functor("EX", [Var("x"), Functor("JAM")]),
    Functor("Node", [Value(3), Functor("MEM"), Var("z")])
])

state, trace = evaluate_full(expr, context)

print("Final state:", state)
for k, v in trace.items():
    print(f"{k} → {v}")

    import json

# Export trace to a JSON file
output = {k: [str(vv) for vv in v] for k, v in trace.items()}
with open("trace_output.json", "w") as f:
    json.dump(output, f, indent=2)

print("Trace exported to trace_output.json ✅")
