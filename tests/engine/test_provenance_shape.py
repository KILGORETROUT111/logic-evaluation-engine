from __future__ import annotations
import json
from pathlib import Path
from src.engine import Pipeline

def _read_prov(path: Path) -> list[dict]:
    lines = []
    with path.open("r", encoding="utf-8") as f:
        for raw in f:
            raw = raw.strip()
            if raw:
                lines.append(json.loads(raw))
    return lines

def test_provenance_has_expected_events(tmp_path):
    log_name = "p14_prov_shape"
    p = Pipeline(log_name=log_name, domain="medical", enable_provenance=True, session="t")
    res = p.run("1 IMPLIES 0")
    log_json = Path(res["log_json"])
    prov_path = log_json.with_suffix(".prov.jsonl")
    assert prov_path.exists(), f"Missing {prov_path}"
    prov = _read_prov(prov_path)

    kinds = [e.get("kind") for e in prov]
    # minimal sequence we expect given the pipeline
    for k in ("start", "prenorm", "enrich", "detect"):
        assert k in kinds, f"Missing {k} event"

    steps = [e.get("step") for e in prov]
    assert steps == sorted(steps), "Provenance steps must be monotonic increasing"

    detect = [e for e in prov if e.get("kind") == "detect"][-1]
    assert detect.get("phase_after") == "JAM"
    enr = detect.get("details", {}).get("enrichment", {})
    assert enr.get("domain") in {"medical", "legal"}
