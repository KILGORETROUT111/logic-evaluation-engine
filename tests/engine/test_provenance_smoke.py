import importlib

def test_provenance_two_transitions_and_basis5(monkeypatch, tmp_path):
    pl = importlib.import_module("src.engine.pipeline")
    monkeypatch.setattr(pl, "LOG_DIR", tmp_path / "logs", raising=False)
    monkeypatch.setattr(pl, "store_entry", lambda **k: None, raising=False)

    pipe = pl.Pipeline("prov_smoke", domain="test", enable_provenance=True, session="s3")
    res = pipe.run("A->B")

    # transitions: ALIVE -> JAM -> MEM
    tos = [t["to"] for t in res["history"]["transitions"]]
    assert tos == ["JAM", "MEM"]

    # basis5 present in final result
    b5 = res["result"]["basis5"]
    assert b5["winding"] is not None
    # witness may be None if not wired in your basis5; accept either
    assert "witness" in b5
