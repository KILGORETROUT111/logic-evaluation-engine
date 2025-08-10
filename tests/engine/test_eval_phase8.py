from src.engine import Pipeline
from src.engine.evaluator import evaluate_expression

def test_beta_reduction_whnf():
    # minimal WHNF smoke: (λx.x) y -> WHNF(y)
    from src.engine.reducer import Var, Lam, App
    y = Var("y")
    expr = App(Lam(Var("x"), Var("x")), y)
    s = evaluate_expression(expr)
    assert s.phase.name == "ALIVE"

def test_canonicalization_feeds_contradiction():
    pipe = Pipeline(log_name="phase8_canon")
    res = pipe.run("1 -> 0")
    assert res["history"]["phases"][:3] == ["ALIVE","JAM","MEM"] or res["history"]["phases"][-3:] == ["ALIVE","JAM","MEM"]
