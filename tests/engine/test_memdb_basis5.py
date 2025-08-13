# tests/engine/test_memdb_basis5.py
import importlib

def test_pipeline_memdb_capture(monkeypatch, tmp_path):
    # Import once so we can patch module-level symbols
    pl = importlib.import_module("src.engine.pipeline")

    # Keep logs local to the test
    monkeypatch.setattr(pl, "LOG_DIR", tmp_path / "logs", raising=False)

    captured = {}
    def fake_store_entry(**kwargs):
        captured.update(kwargs)

    # Patch the *imported* symbol inside pipeline.py
    monkeypatch.setattr(pl, "store_entry", fake_store_entry, raising=False)

    pipe = pl.Pipeline(
        log_name="t_memdb",
        domain="legal",
        enable_provenance=True,
        session="sess-1",
    )
    res = pipe.run("A->B")

    # Basic run invariants
    assert res["state"]["phase"] == "MEM"
    assert "run_id" in res["history"]

    # MemDB payload invariants
    assert captured["run_id"] == res["history"]["run_id"]
    assert captured["session"] == "sess-1"
    assert captured["domain"] == "legal"
    assert captured["final_phase"] == "MEM"
    assert isinstance(captured["time_to_mem_ms"], (int, float))
    # Prenormalization check
    assert captured["jam"]["pattern"] == "A -> B"
