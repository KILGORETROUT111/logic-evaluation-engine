# tests/engine/test_phase13_adapters.py
from __future__ import annotations

import json
from pathlib import Path
from glob import glob

from src.engine import Pipeline


def _resolve_log_json(res: dict, log_name: str) -> Path:
    # Preferred: returned by pipeline
    p = res.get("log_json")
    if p:
        return Path(p)

    # Fallback: newest matching file under data/logs/
    candidates = sorted(
        (Path(x) for x in glob(f"data/logs/{log_name}_*.json")),
        key=lambda p: p.stat().st_mtime if p.exists() else 0.0,
        reverse=True,
    )
    assert candidates, f"No logs found for log_name={log_name}"
    return candidates[0]


def _read_prov_lines(log_json_path: Path) -> list[dict]:
    prov = log_json_path.with_suffix(".prov.jsonl")
    assert prov.exists(), f"Provenance file missing: {prov}"
    lines = []
    with prov.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                lines.append(json.loads(line))
            except Exception:
                pass
    return lines


def test_legal_prenorm_and_enrichment(tmp_path):
    log_name = "phase13_legal_test"
    p = Pipeline(
        log_name=log_name,
        domain="legal",
        enable_provenance=True,
        session="test",
    )
    res = p.run("1 IMPLIES 0")
    assert res["state"]["phase"] == "MEM"

    log_json = _resolve_log_json(res, log_name)
    prov = _read_prov_lines(log_json)
    detects = [d for d in prov if d.get("kind") == "detect" and d.get("phase_after") == "JAM"]
    assert detects, "No JAM detect entries found in provenance"
    assert any(isinstance(d.get("details", {}).get("enrichment"), dict) for d in detects)


def test_medical_enrichment(tmp_path):
    log_name = "phase13_medical_test"
    p = Pipeline(
        log_name=log_name,
        domain="medical",
        enable_provenance=True,
        session="test",
    )
    res = p.run("1 -> 0")
    assert res["state"]["phase"] == "MEM"

    log_json = _resolve_log_json(res, log_name)
    prov = _read_prov_lines(log_json)
    detects = [d for d in prov if d.get("kind") == "detect" and d.get("phase_after") == "JAM"]
    assert detects, "No JAM detect entries found in provenance"
    assert any(d.get("details", {}).get("enrichment", {}).get("domain") == "medical" for d in detects)
