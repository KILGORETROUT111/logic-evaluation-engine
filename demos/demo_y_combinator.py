from core.expressions import (
    Variable, Literal, Lambda, Application, BinaryOp, IfThenElse
)
from core.evaluation import evaluate_full
from core.state import State
from trace_to_proof import trace_to_proof

# Define the fixed-point combinator Y = λf.(λx.f(x x))(λx.f(x x))
X = Lambda("x", Application(Variable("f"), Application(Variable("x"), Variable("x"))))
Y = Lambda("f", Application(X, X))

# Define factorial generator:
# fact_gen = λf.λn. if n == 0 then 1 else n * f(n-1)
fact_gen = Lambda("f", Lambda("n",
    IfThenElse(
        BinaryOp("==", Variable("n"), Literal(0)),
        Literal(1),
        BinaryOp("*", Variable("n"), Application(Variable("f"),
                                                 BinaryOp("-", Variable("n"), Literal(1))))
    )
))

# Patch BinaryOp to handle "-" just for demo
def patched_evaluate(expr, env=None, trace=None):
    from core.evaluation import evaluate_full as original_eval
    if isinstance(expr, BinaryOp):
        left_result, trace = patched_evaluate(expr.left, env, trace)
        right_result, trace = patched_evaluate(expr.right, env, trace)
        if expr.op == "-":
            try:
                return Literal(left_result.value - right_result.value), trace
            except:
                return State.JAM, trace
        else:
            return original_eval(expr, env, trace)
    return original_eval(expr, env, trace)

# Build the expression: ((Y fact_gen)(3))
expr = Application(Application(Y, fact_gen), Literal(3))

result, trace = patched_evaluate(expr)

proof_output = trace_to_proof(
    trace,
    result.value if hasattr(result, "value") else result.name if hasattr(result, "name") else str(result)
)

print(proof_output)
