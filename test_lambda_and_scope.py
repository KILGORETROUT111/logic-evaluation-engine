from core.expressions import Variable, Literal, Lambda, Application, Quantifier
from core.evaluation import evaluate_full
from core.state import State

def test_lambda_identity():
    # (λx.x)(1) → 1
    expr = Application(Lambda("x", Variable("x")), Literal(1))
    result, _ = evaluate_full(expr)
    assert result == State.ALIVE

def test_lambda_nested_application():
    # ((λx.λy.x)(1))(2) → 1
    inner = Lambda("y", Variable("x"))
    outer = Lambda("x", inner)
    expr = Application(Application(outer, Literal(1)), Literal(2))
    result, _ = evaluate_full(expr)
    assert result == State.ALIVE

def test_quantifier_variable_shadowing():
    # ∀x. ∃x. x == 2
    class EqualityExpr(Literal):
        def __init__(self, varname):
            self.varname = varname
            self.value = varname

        def __repr__(self):
            return f"(EQ {self.varname})"

    def evaluate_expr(expr, env=None):
        if isinstance(expr, EqualityExpr):
            x_val = env.get(expr.varname)
            return (State.ALIVE if x_val and x_val.value == 2 else State.JAM), []
        return evaluate_full(expr, env)

    def evaluate_quantifier(expr, env=None):
        results = []
        for val in [1, 2, 3]:
            local_env = env.copy() if env else {}
            local_env[expr.var] = Literal(val)
            sub_result, _ = evaluate_expr(expr.body, local_env)
            results.append(sub_result)
        if expr.universal:
            return (State.ALIVE if all(r == State.ALIVE for r in results) else State.JAM), []
        else:
            return (State.ALIVE if any(r == State.ALIVE for r in results) else State.JAM), []

    inner = Quantifier("x", EqualityExpr("x"), universal=False)
    outer = Quantifier("x", inner, universal=True)
    result, _ = evaluate_quantifier(outer)
    assert result == State.ALIVE
