from pathlib import Path
from src.engine import Pipeline

def test_provenance_files_written():
    # Enable Phase-10 provenance; use a JAM-y input so we get a richer timeline
    p = Pipeline(log_name="phase10_test", enable_provenance=True)
    res = p.run("1 -> 0")

    json_path = Path(res["log_json"])
    assert json_path.exists()

    # Audit artifacts written next to the JSON log
    assert json_path.with_suffix(".prov.jsonl").exists()
    assert json_path.with_suffix(".timeline.md").exists()
    assert json_path.with_suffix(".timeline.dot").exists()
