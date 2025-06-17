import sys
from core.expressions import Functor, Value, Var
from core.evaluation import evaluate_full

def parse_expr(expr_str):
    expr_str = expr_str.strip().replace(" ", "").upper()
    if expr_str == "EX(X,JAM())":
        return Functor("EX", [Var("x"), Functor("JAM")])
    elif expr_str == "MEM":
        return Functor("MEM")
    else:
        raise ValueError(f"Unsupported expression: {expr_str}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py \"EX(x, JAM())\"")
        sys.exit(1)

    try:
        expr = parse_expr(sys.argv[1])
        context = {"x": 1, "z": 2}
        state, trace = evaluate_full(expr, context)

        print("Final state:", state)
        for k, v in trace.items():
            print(f"{k} → {v}")
    except Exception as e:
        print("Error:", e)
        sys.exit(2)