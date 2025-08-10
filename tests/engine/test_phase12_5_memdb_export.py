from src.engine import Pipeline
from src.engine import memdb
import os

def test_memdb_export(tmp_path):
    p = Pipeline(
        log_name="phase12_5_test",
        patient_id="P001",
        case_id="C001",
        domain="legal",
        enable_provenance=False
    )
    p.state = {"phase": "MEM"}
    memdb.store_entry("P001", "C001", "legal", "MEM")
    csv_path = memdb.export_csv(tmp_path / "export.csv")
    assert csv_path.exists()
    with open(csv_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    assert "patient_id" in lines[0]
