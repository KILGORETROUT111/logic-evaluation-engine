from src.analytic.substitution import Var, Const, Fun, Subst, unify, UnifyError

def test_unify_simple():
    x, a = Var("x"), Const("a")
    σ = unify(x, a)
    assert σ.apply(x) == a

def test_unify_structure():
    x, y = Var("x"), Var("y")
    fxy = Fun("f", (x, y))
    faa = Fun("f", (Const("a"), Const("a")))
    σ = unify(fxy, faa)
    assert σ.apply(fxy) == faa
    assert σ.apply(x) == Const("a") and σ.apply(y) == Const("a")

def test_unify_occurs_check():
    x = Var("x")
    fx = Fun("f", (x,))
    try:
        unify(x, fx)
        assert False, "expected occurs-check failure"
    except UnifyError:
        pass

def test_compose_and_apply():
    x, y, a, b = Var("x"), Var("y"), Const("a"), Const("b")
    σ1 = unify(x, a)
    σ2 = unify(y, b)
    σ = σ1.compose(σ2)
    t = Fun("g", (x, y))
    assert σ.apply(t) == Fun("g", (a, b))
