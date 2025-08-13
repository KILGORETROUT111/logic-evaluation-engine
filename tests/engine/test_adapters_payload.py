# tests/engine/test_adapters_payload.py
import importlib

def test_adapter_metadata_in_payload(monkeypatch, tmp_path):
    pl = importlib.import_module("src.engine.pipeline")
    from src.nlp.handshake import evaluate_text

    monkeypatch.setattr(pl, "LOG_DIR", tmp_path / "logs", raising=False)
    captured = {}
    monkeypatch.setattr(pl, "store_entry", lambda **k: captured.update(k), raising=False)

    pipe = pl.Pipeline("adapters_meta", domain="legal", enable_provenance=True, session="sX")
    res = evaluate_text("breach implies liability", pipe)

    # memdb payload has adapter metadata
    assert captured["jam"]["pattern"] == "breach -> liability"
    assert captured["jam"]["adapter"]["name"] in ("legal", "law")

    # history transition details carry adapter too
    jam = next(t for t in res["history"]["transitions"] if t["to"] == "JAM")
    assert jam["details"]["adapter"]["name"] in ("legal", "law")
