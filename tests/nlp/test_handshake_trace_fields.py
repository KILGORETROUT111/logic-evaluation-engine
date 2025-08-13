import importlib

def test_trace_keeps_nl_and_lambda_nf(monkeypatch, tmp_path):
    pl = importlib.import_module("src.engine.pipeline")
    from src.nlp.handshake import evaluate_text

    monkeypatch.setattr(pl, "LOG_DIR", tmp_path / "logs", raising=False)
    captured = {}
    monkeypatch.setattr(pl, "store_entry", lambda **k: captured.update(k), raising=False)

    pipe = pl.Pipeline("nlp_trace2", domain="nlp", enable_provenance=True, session="s2")
    res = evaluate_text("if A then B", pipe)

    # memdb payload
    assert captured["jam"]["pattern"] == "A -> B"
    assert captured["jam"]["nl"] == "if A then B"
    assert "Imp" in captured["jam"]["lambda_nf"]

    # JAM transition details
    jam = next(t for t in res["history"]["transitions"] if t["to"] == "JAM")
    assert jam["details"]["pattern"] == "A -> B"
    assert jam["details"]["nl"] == "if A then B"
    assert "Imp" in jam["details"]["lambda_nf"]
