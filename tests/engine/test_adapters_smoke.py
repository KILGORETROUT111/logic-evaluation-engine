import importlib

def test_legal_adapter_implies(monkeypatch, tmp_path):
    pl = importlib.import_module("src.engine.pipeline")
    from src.nlp.handshake import evaluate_text

    monkeypatch.setattr(pl, "LOG_DIR", tmp_path / "logs", raising=False)
    captured = {}
    monkeypatch.setattr(pl, "store_entry", lambda **k: captured.update(k), raising=False)

    pipe = pl.Pipeline("adapters", domain="legal", enable_provenance=True, session="sA")
    res = evaluate_text("breach implies liability", pipe)

    # adapter should convert to P -> Q even though λ mini-parser wouldn't
    assert captured["jam"]["pattern"] == "breach -> liability"
    assert res["state"]["phase"] == "MEM"

def test_med_adapter_indicates(monkeypatch, tmp_path):
    pl = importlib.import_module("src.engine.pipeline")
    from src.nlp.handshake import evaluate_text

    monkeypatch.setattr(pl, "LOG_DIR", tmp_path / "logs", raising=False)
    monkeypatch.setattr(pl, "store_entry", lambda **k: None, raising=False)

    pipe = pl.Pipeline("adapters2", domain="medical", enable_provenance=True, session="sB")
    res = evaluate_text("fever indicates infection", pipe)
    jam = next(t for t in res["history"]["transitions"] if t["to"] == "JAM")
    assert jam["details"]["pattern"] == "fever -> infection"
