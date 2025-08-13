# tests/nlp/test_handshake_smoke.py
import importlib
from src.nlp.handshake import evaluate_text

def test_if_then_to_pipeline(monkeypatch, tmp_path):
    pl = importlib.import_module("src.engine.pipeline")

    # isolate logs and capture memdb sink
    monkeypatch.setattr(pl, "LOG_DIR", tmp_path / "logs", raising=False)
    captured = {}
    def fake_store_entry(**kwargs):
        captured.update(kwargs)
    monkeypatch.setattr(pl, "store_entry", fake_store_entry, raising=False)

    pipe = pl.Pipeline(log_name="nlp_trace", domain="nlp", enable_provenance=True, session="s1")
    res = evaluate_text("if A then B", pipe)

    assert res["state"]["phase"] == "MEM"
    assert res["history"]["run_id"]
    assert captured["jam"]["pattern"] == "A -> B"
