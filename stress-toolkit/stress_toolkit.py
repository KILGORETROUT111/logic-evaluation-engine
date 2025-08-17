
from __future__ import annotations
from typing import List, Dict, Any, Iterable, Tuple
import json, pathlib

ANGLES = {"ALIVE": 0, "JAM": 90, "MEM": 180}

def rotation_delta_deg(a: str, b: str) -> int:
    return (ANGLES[b] - ANGLES[a]) % 360

def build_winding(phases: List[str]) -> Dict[str, Any]:
    total = 0
    deltas = []
    for i in range(1, len(phases)):
        d = rotation_delta_deg(phases[i-1], phases[i])
        deltas.append(d)
        total += d
    return {"rotation_deltas_deg": deltas, "total_winding_deg": total}

def jam_ratio_from_prov_or_trace(prov_iter, phases: List[str]):
    total_steps = 0
    jam_steps = 0
    have_ts = False
    for line in prov_iter:
        line = line.strip()
        if not line:
            continue
        try:
            evt = json.loads(line)
        except Exception:
            continue
        total_steps += 1
        ev = evt.get("event") or evt.get("type")
        details = evt.get("details") or {}
        after = None
        if ev == "transition":
            after = evt.get("after") or details.get("after")
        elif ev == "phase":
            after = evt.get("phase") or details.get("phase")
        if after == "JAM":
            jam_steps += 1
        ts = evt.get("ts") or evt.get("time") or evt.get("@timestamp")
        if isinstance(ts, str):
            have_ts = True
    if total_steps > 0:
        return (jam_steps / total_steps, have_ts)
    if phases:
        return (sum(1 for p in phases if p == "JAM") / len(phases), False)
    return (0.0, False)

def resistance(deltas: List[int], phases: List[str]) -> float:
    if not deltas:
        return 0.0
    mean_delta = sum(deltas) / len(deltas)
    loop_penalty = 1.0 if len(set(phases)) < len(phases) else 0.0
    return (mean_delta/180.0) * (0.5 + 0.5*loop_penalty)

def compute_stress(phases: List[str], prov_path: pathlib.Path | None = None) -> Dict[str, Any]:
    w = build_winding(phases)
    prov_iter = open(prov_path, "r", encoding="utf-8", errors="ignore") if prov_path and pathlib.Path(prov_path).exists() else []
    try:
        jam_ratio, used_ts = jam_ratio_from_prov_or_trace(prov_iter, phases)
    finally:
        try:
            prov_iter.close()
        except Exception:
            pass
    si = (w["total_winding_deg"]/360.0) * jam_ratio
    res = resistance(w["rotation_deltas_deg"], phases)
    return {
        "phases": phases,
        "rotation_deltas_deg": w["rotation_deltas_deg"],
        "total_winding_deg": w["total_winding_deg"],
        "jam_ratio": round(jam_ratio, 6),
        "resistance": round(res, 6),
        "stress_index": round(si, 6),
        "used_timestamps": used_ts,
        "notes": "Jam ratio from provenance step counts when available; otherwise from phase trace."
    }

def load_phases_from_summary(summary_json_path: pathlib.Path) -> list[str]:
    p = pathlib.Path(summary_json_path)
    if not p.exists():
        return []
    data = json.loads(p.read_text(encoding="utf-8"))
    return data.get("history", {}).get("phases", [])
