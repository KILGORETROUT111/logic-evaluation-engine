# -*- coding: utf-8 -*-
from __future__ import annotations
from pathlib import Path
from typing import Dict, Any
import json

MEMDB_DIR = Path("data/memdb")

def append_patient_history(patient_id: str, res: Dict[str, Any], fallback_run_id: str | None = None) -> None:
    MEMDB_DIR.mkdir(parents=True, exist_ok=True)
    path = MEMDB_DIR / f"{patient_id}.history.jsonl"
    hist = res.get("history", {}) or {}
    payload = {
        "run_id": hist.get("run_id") or fallback_run_id,
        "phase": (res.get("state", {}) or {}).get("phase"),
        "final_phase": (res.get("state", {}) or {}).get("phase"),
        "phases": hist.get("phases", []),
        "domain": res.get("domain"),
    }
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False) + "\n")

def write_patient_summary(patient_id: str, res: Dict[str, Any]) -> None:
    MEMDB_DIR.mkdir(parents=True, exist_ok=True)
    path = MEMDB_DIR / f"{patient_id}.summary.md"
    hist = res.get("history", {}) or {}
    phases = " → ".join(hist.get("phases", []))
    final_phase = (res.get("state", {}) or {}).get("phase")
    run_id = hist.get("run_id")
    md = [
        f"# Patient {patient_id} — LEE Summary", "",
        f"- **run_id:** {run_id}",
        f"- **final phase:** {final_phase}",
        f"- **trace:** {phases}", "",
    ]
    path.write_text("\n".join(md), encoding="utf-8")
