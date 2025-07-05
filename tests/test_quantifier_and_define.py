from core.expressions import Variable, Literal, Lambda, Application, Substitution, Define, Quantifier
from core.evaluation import evaluate_full
from core.state import State

def test_substitution_alpha_renaming():
    expr = Lambda("x", Variable("x"))
    sub = Substitution("x", expr, Variable("x"))
    result, trace = evaluate_full(sub)
    assert result == State.ALIVE
    assert any("SUB" in step["phase"] for step in trace)

def test_define_evaluation():
    expr = Define("f", Lambda("x", Variable("x")))
    env = {}
    result, trace = evaluate_full(expr, env)
    assert result == State.ALIVE
    assert "f" in env
    assert isinstance(env["f"], Lambda)

def test_quantifier_universal_success():
    body = Literal(1)  # Always ALIVE
    expr = Quantifier("x", body, universal=True)
    result, trace = evaluate_full(expr)
    assert result == State.ALIVE

def test_quantifier_universal_failure():
    # ∀x ∈ [1, 2, 3]: (EQ x == 2) → fails for 1 and 3 → should JAM
    class EqualityExpr(Literal):
        def __init__(self, varname):
            self.varname = varname
            self.value = varname  # just for compatibility

        def __repr__(self):
            return f"(EQ {self.varname})"

    def evaluate_custom_quantifier(expr, env=None, trace=None):
        if env is None:
            env = {}
        if trace is None:
            trace = []

        results = []
        for val in [1, 2, 3]:
            local_env = env.copy()
            local_env[expr.var] = Literal(val)
            sub_result, _ = evaluate_expr(expr.body, local_env)
            results.append(sub_result)

        if expr.universal:
            return (State.ALIVE if all(r == State.ALIVE for r in results) else State.JAM), trace
        else:
            return (State.ALIVE if any(r == State.ALIVE for r in results) else State.JAM), trace

    def evaluate_expr(expr, env=None):
        if isinstance(expr, EqualityExpr):
            x_val = env.get(expr.varname)
            return (State.ALIVE if x_val and x_val.value == 2 else State.JAM), []
        return evaluate_full(expr, env)

    body = EqualityExpr("x")
    expr = Quantifier("x", body, universal=True)
    result, trace = evaluate_custom_quantifier(expr)
    assert result == State.JAM