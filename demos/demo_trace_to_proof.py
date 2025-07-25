from core.expressions import Variable, Literal, Lambda, Application
from core.evaluation import evaluate_full
from core.states import State
from trace_to_proof import trace_to_proof

# Sample: ((λx.λy.x)(1))(2)
inner = Lambda("y", Variable("x"))
outer = Lambda("x", inner)
expr = Application(Application(outer, Literal(1)), Literal(2))

result, trace = evaluate_full(expr)

# Convert to readable proof
proof_output = trace_to_proof(trace, result.name if hasattr(result, "name") else str(result))
print(proof_output)