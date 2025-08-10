# tests/engine/test_phase12_memdb.py
from pathlib import Path
from src.engine import Pipeline

def test_patient_history_and_summary(tmp_path: Path):
    # Run with a patient_id tag
    p = Pipeline(
        log_name="phase12_patient",
        enable_provenance=True,
        enable_temporal_analytics=True,  # benign
        session="test",
        patient_id="P001",
        domain="medical",
    )
    res = p.run("1 -> 0")  # JAM→MEM path

    # Files should exist
    hist = Path("data/memdb/P001.history.jsonl")
    summ = Path("data/memdb/P001.summary.md")
    assert hist.exists(), "patient history jsonl missing"
    assert summ.exists(), "patient summary md missing"

    # Last line should mention this run_id and final phase MEM
    lines = hist.read_text(encoding="utf-8").strip().splitlines()
    assert lines, "history should have at least one line"
    import json as _json
    last = _json.loads(lines[-1])
    assert last.get("run_id") == res["history"]["run_id"] if "run_id" in res.get("history", {}) else p.run_id
    assert last.get("final_phase") == res["state"]["phase"]
    assert last.get("domain") == "medical"


def test_case_history_and_summary(tmp_path: Path):
    # Run with a case_id tag
    p = Pipeline(
        log_name="phase12_case",
        enable_provenance=True,
        enable_temporal_analytics=True,
        session="test",
        case_id="C-TEST-001",
        domain="legal",
    )
    res = p.run("1 -> 0")

    hist = Path("data/memdb/C-TEST-001.history.jsonl")
    summ = Path("data/memdb/C-TEST-001.summary.md")
    assert hist.exists(), "case history jsonl missing"
    assert summ.exists(), "case summary md missing"

    # Parse and assert
    lines = hist.read_text(encoding="utf-8").strip().splitlines()
    assert lines
    import json as _json
    last = _json.loads(lines[-1])
    assert last.get("final_phase") == res["state"]["phase"]
    assert last.get("domain") == "legal"
