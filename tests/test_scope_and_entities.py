import os
os.environ.setdefault(
    "PYTHONPATH",
    os.path.join(os.path.dirname(__file__), "..", "..", "src")
)

from nlp.parser import parse
from nlp.scope_inference import analyze_scopes, free_vars
from nlp.named_entities import entities_from_text

def test_free_and_scopes():
    e = parse("forall x. (lambda y . (f x) y)")
    assert free_vars(e) == {"f"}
    g = analyze_scopes(e)
    assert len(g.nodes) == 2   # quantifier and lambda scopes
    assert [r.resolved_scope for r in g.references] == [None, 0, 1]

def test_entities_basic():
    m = entities_from_text("Alice met Dr. Bob at New York-Presbyterian.")
    assert "Alice" in m and m["Alice"].name == "alice"
    assert "York-Presbyterian" in m and m["York-Presbyterian"].name == "york-presbyterian"
