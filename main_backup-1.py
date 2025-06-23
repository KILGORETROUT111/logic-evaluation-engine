import sys
import json
from core.parser import parse_expression
from core.evaluation import evaluate_full

if len(sys.argv) < 2:
    print('Usage: python main.py \'["EX", "x", "JAM"]\'')
    sys.exit(1)

expr_str = sys.argv[1]
parsed_json = json.loads(expr_str)
expr = parse_expression(parsed_json)

context = {"x": 1, "z": 2}  # You can modify this as needed

state, trace = evaluate_full(expr, context)

print("Final state:", state)
print("Trace:")
for k, v in trace.items():
    print(f"{k} → {[str(e) for e in v]}")