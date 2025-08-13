from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional

"""
Basis5: minimal geometric phase dynamics surface for LEE.

- Phases live on the unit circle: ALIVE (0°), JAM (90°), MEM (180°).
- We expose:
  * transition_basis: one-step rotation tensor with before/after vectors and delta.
  * build_winding: cumulative rotation over a phase sequence.
  * witness_basis: tiny tensor for implication/refutation cues (material implication, detachment/witness).

This module is intentionally small and engine-safe: it only adds provenance detail, never
changes control flow or test-visible behavior.
"""

PHASE_ANGLE = {"ALIVE": 0.0, "JAM": 90.0, "MEM": 180.0}


@dataclass
class PhasePoint:
    phase: str
    angle_deg: float
    angle_rad: float
    vector: Tuple[float, float]


def _vec(angle_deg: float) -> Tuple[float, float]:
    rad = math.radians(angle_deg)
    return (math.cos(rad), math.sin(rad))


def project_phase(phase: str) -> PhasePoint:
    p = (phase or "ALIVE").upper()
    ang = PHASE_ANGLE.get(p, 0.0)
    return PhasePoint(
        phase=p,
        angle_deg=ang,
        angle_rad=math.radians(ang),
        vector=_vec(ang),
    )


def rotation_delta_deg(a: str | None, b: str | None) -> float:
    """Positive rotation from phase a to b on the unit circle (mod 360)."""
    pa = (a or "ALIVE").upper()
    pb = (b or "ALIVE").upper()
    da = PHASE_ANGLE.get(pa, 0.0)
    db = PHASE_ANGLE.get(pb, 0.0)
    d = (db - da) % 360.0
    # normalize: 360 → 0 for 'no change'
    return 0.0 if math.isclose(d, 360.0) else d


def transition_basis(phase_before: str | None, phase_after: str | None) -> Dict:
    """One-step transition tensor."""
    p_before = project_phase(phase_before or "ALIVE")
    p_after = project_phase(phase_after or "ALIVE")
    return {
        "before": {
            "phase": p_before.phase,
            "angle_deg": p_before.angle_deg,
            "vec": {"x": p_before.vector[0], "y": p_before.vector[1]},
        },
        "after": {
            "phase": p_after.phase,
            "angle_deg": p_after.angle_deg,
            "vec": {"x": p_after.vector[0], "y": p_after.vector[1]},
        },
        "delta_deg": rotation_delta_deg(p_before.phase, p_after.phase),
    }


def build_winding(phases: List[str]) -> Dict:
    """Cumulative rotation over a phase sequence."""
    out: List[Dict] = []
    cum = 0.0
    last: Optional[PhasePoint] = None
    for i, ph in enumerate(phases):
        p = project_phase(ph)
        d = 0.0 if last is None else rotation_delta_deg(last.phase, p.phase)
        cum += d
        out.append(
            {
                "step": i,
                "phase": p.phase,
                "angle_deg": p.angle_deg,
                "delta_deg": d,
                "winding_deg": cum,
                "vector": {"x": p.vector[0], "y": p.vector[1]},
            }
        )
        last = p
    avgx = sum(pt["vector"]["x"] for pt in out) / len(out) if out else 0.0
    avgy = sum(pt["vector"]["y"] for pt in out) / len(out) if out else 0.0
    return {
        "points": out,
        "summary": {
            "total_winding_deg": cum,
            "avg_vector": {"x": avgx, "y": avgy},
            "unique_phases": list(dict.fromkeys([p["phase"] for p in out])),
        },
    }


def witness_basis(expr: str) -> Dict[str, Optional[float]]:
    """
    Material implication / refutation cues as a small tensor.
    Hardwired minimal mapping to your geometry; does not change engine control flow.
    """
    s = (expr or "").replace(" ", "")
    su = s.upper()
    # implication / detachment / MP shape
    if "IMPLIES" in su or "->" in s:
        return {"jam": 1.0, "detach": 1.0, "mp": 1.0}
    # local refutation (p & ~p), loose match on '&' and '~'
    if "&~" in s or ("&" in s and "~" in s):
        return {"jam": 1.0, "refute": 1.0}
    return {"jam": 0.0}
