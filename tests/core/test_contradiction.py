from core import contradiction as C

def mk(op, *args):
    return (op, *args)

def test_witness_local_refutation():
    X = "p"
    r = C.analyze(mk("And", X, mk("Not", X)))
    assert r["is_contradiction"] is True
    assert r["mode"] == "local-refutation"
    assert r["witness"]["pattern"] == "X & ~X"
    assert r["witness"]["X"] == "p"

def test_witness_implication_jam():
    r = C.analyze(mk("->", 1, 0))
    assert r["is_contradiction"] is True
    assert r["mode"] == "implication-jam"
    w = r["witness"]
    assert w["pattern"] == "1 -> 0"
    assert w["antecedent"] == 1 and w["consequent"] == 0

def test_no_contradiction_simple():
    r = C.analyze(mk("->", 1, 1))
    assert r["is_contradiction"] is False
