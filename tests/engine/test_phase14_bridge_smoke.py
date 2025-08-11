from __future__ import annotations
import json
from pathlib import Path
from glob import glob
from src.engine import Pipeline

def _resolve_log_json(res: dict, log_name: str) -> Path:
    p = res.get("log_json")
    if p:
        return Path(p)
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

def _detects(prov: list[dict]) -> list[dict]:
    return [d for d in prov if d.get("kind") == "detect" and d.get("phase_after") == "JAM"]

def test_bridge_legal_smoke(tmp_path):
    log_name = "p14_legal_smoke"
    p = Pipeline(log_name=log_name, domain="legal", enable_provenance=True, session="t")
    res = p.run("1 IMPLIES 0")
    assert res["state"]["phase"] == "MEM"
    prov = _read_prov_lines(_resolve_log_json(res, log_name))
    detects = _detects(prov)
    assert detects, "No JAM detect entries"
    # any dict is fine for legal
    assert isinstance(detects[-1].get("details", {}).get("enrichment"), dict)

def test_bridge_medical_smoke(tmp_path):
    log_name = "p14_med_smoke"
    p = Pipeline(log_name=log_name, domain="medical", enable_provenance=True, session="t")
    res = p.run("1 -> 0")
    assert res["state"]["phase"] == "MEM"
    prov = _read_prov_lines(_resolve_log_json(res, log_name))
    detects = _detects(prov)
    assert detects, "No JAM detect entries"
    assert detects[-1].get("details", {}).get("enrichment", {}).get("domain") == "medical"
