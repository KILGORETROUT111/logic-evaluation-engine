from src.analytic.lambda_calc import LVar, Lam, App, beta_step, beta_normal_form, free_vars

def test_identity_application():
    I = Lam("x", LVar("x"))
    a = LVar("a")
    t, ch = beta_step(App(I, a))
    assert ch and t == a

def test_const_function():
    K = Lam("x", Lam("y", LVar("x")))
    a, b = LVar("a"), LVar("b")
    # ((K a) b) -> a
    nf = beta_normal_form(App(App(K, a), b))
    assert nf == a

def test_capture_avoidance():
    # (λx. λy. x) y  ⇒  λy_1. y   (free y stays free, bound y renamed)
    t = App(Lam("x", Lam("y", LVar("x"))), LVar("y"))
    nf = beta_normal_form(t)
    # result is a lambda whose body is free 'y'
    assert isinstance(nf, Lam)
    assert free_vars(nf.body) == {"y"}
    assert nf.param != "y"  # due to α-renaming

def test_church_numerals_succ_once():
    # ONE := λf.λx. f x
    ONE = Lam("f", Lam("x", App(LVar("f"), LVar("x"))))
    # INC := λn.λf.λx. f (n f x)
    INC = Lam("n", Lam("f", Lam("x", App(LVar("f"), App(App(LVar("n"), LVar("f")), LVar("x"))))))
    nf = beta_normal_form(App(INC, ONE), max_steps=1000)
    # normal form is λf.λx. f (f x)
    def church_two(t):
        # quick predicate: λf.λx.(f (f x))
        return (
            isinstance(t, Lam) and
            isinstance(t.body, Lam) and
            isinstance(t.body.body, App) and
            isinstance(t.body.body.fn, LVar) and t.body.body.fn.name == "f"
        )
    assert church_two(nf)
