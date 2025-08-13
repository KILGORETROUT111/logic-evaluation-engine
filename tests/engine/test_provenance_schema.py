# tests/engine/test_provenance_schema.py
import importlib

def test_provenance_schema_smoke(monkeypatch, tmp_path):
    pl = importlib.import_module("src.engine.pipeline")
    monkeypatch.setattr(pl, "LOG_DIR", tmp_path / "logs", raising=False)
    monkeypatch.setattr(pl, "store_entry", lambda **k: None, raising=False)

    pipe = pl.Pipeline("prov_schema", domain="test", enable_provenance=True, session="s4")
    res = pipe.run("A->B", meta={"nl": "A implies B", "lambda_nf": "((Imp A) B)"})

    # state & history
    assert res["state"]["phase"] == "MEM"
    hist = res["history"]
    assert isinstance(hist["run_id"], str)
    assert hist["phases"] == ["ALIVE", "JAM", "MEM"]
    assert len(hist["transitions"]) == 2
    for t in hist["transitions"]:
        assert t["from"] in ("ALIVE", "JAM")
        assert t["to"] in ("JAM", "MEM")
        assert "ts" in t
        if t["to"] == "JAM":
            d = t.get("details", {})
            assert d.get("pattern") == "A -> B"
            # nl / lambda_nf may or may not be present depending on call site; here they are
            assert d.get("nl") == "A implies B"
            assert "lambda_nf" in d

    # result basis5 presence (best-effort)
    b5 = res["result"]["basis5"]
    assert "winding" in b5
    assert "witness" in b5  # may be None, but key should exist
