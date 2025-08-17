from __future__ import annotations
from typing import List, Dict, Any

# Canonical Basis5 angles (deg)
ANGLES = {"ALIVE": 0, "JAM": 90, "MEM": 180}

def rotation_delta_deg(a: str, b: str) -> int:
    return (ANGLES[b] - ANGLES[a]) % 360

def build_winding(phases: List[str]) -> Dict[str, Any]:
    deltas = []
    total = 0
    for i in range(1, len(phases)):
        d = rotation_delta_deg(phases[i-1], phases[i])
        deltas.append(d)
        total += d
    return {
        "rotation_deltas_deg": deltas,
        "total_winding_deg": total,
    }

def jam_ratio_from_trace(phases: List[str]) -> float:
    if not phases:
        return 0.0
    jam_count = sum(1 for p in phases if p == "JAM")
    return jam_count / len(phases)

def resistance_from_deltas(deltas: List[int], phases: List[str]) -> float:
    if not deltas:
        return 0.0
    mean_delta = sum(deltas) / len(deltas)
    loop_penalty = 1.0 if len(set(phases)) < len(phases) else 0.0
    return (mean_delta / 180.0) * (0.5 + 0.5 * loop_penalty)

def compute_stress_metrics(phases: List[str]) -> Dict[str, Any]:
    w = build_winding(phases)
    jam_ratio = jam_ratio_from_trace(phases)
    resistance = resistance_from_deltas(w["rotation_deltas_deg"], phases)
    stress_index = (w["total_winding_deg"] / 360.0) * jam_ratio
    return {
        "phases": phases,
        "rotation_deltas_deg": w["rotation_deltas_deg"],
        "total_winding_deg": w["total_winding_deg"],
        "jam_ratio": round(jam_ratio, 6),
        "resistance": round(resistance, 6),
        "stress_index": round(stress_index, 6),
        "notes": "Jam ratio derived from phase-trace distribution; upgrade to time-weighted when durations are available."
    }
