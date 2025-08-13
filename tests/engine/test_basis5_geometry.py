# tests/engine/test_basis5_geometry.py
import math
from src.core.basis5 import (
    PHASE_ANGLE,
    project_phase,
    rotation_delta_deg,
    build_winding,
    witness_basis,
)

def _approx(a, b, eps=1e-9):
    return abs(a - b) <= eps

def test_angles_and_vectors():
    assert set(PHASE_ANGLE.keys()) == {"ALIVE", "JAM", "MEM"}
    p_alive = project_phase("ALIVE")
    p_jam   = project_phase("JAM")
    p_mem   = project_phase("MEM")
    assert _approx(p_alive.angle_deg, 0.0)
    assert _approx(p_jam.angle_deg, 90.0)
    assert _approx(p_mem.angle_deg, 180.0)
    # Unit circle directions
    ax, ay = p_alive.vector
    jx, jy = p_jam.vector
    mx, my = p_mem.vector
    assert _approx(ax, 1.0) and _approx(ay, 0.0)
    assert _approx(jx, 0.0) and _approx(jy, 1.0)
    assert _approx(mx, -1.0) and _approx(my, 0.0)

def test_rotation_and_winding():
    assert _approx(rotation_delta_deg("ALIVE", "JAM"), 90.0)
    assert _approx(rotation_delta_deg("JAM", "MEM"), 90.0)
    w = build_winding(["ALIVE", "JAM", "MEM"])
    assert _approx(w["summary"]["total_winding_deg"], 180.0)
    # First step has zero delta by construction
    assert _approx(w["points"][0]["delta_deg"], 0.0)
    assert _approx(w["points"][1]["delta_deg"], 90.0)
    assert _approx(w["points"][2]["delta_deg"], 90.0)

def test_witness_basis_behavior():
    # Current minimal witness: implication-like patterns mark jam/detach/mp
    w1 = witness_basis("1 -> 0")
    assert w1.get("jam") == 1.0 and w1.get("detach") == 1.0 and w1.get("mp") == 1.0
    w2 = witness_basis("P & ~P")
    assert w2.get("jam") == 1.0 and w2.get("refute") == 1.0
    w3 = witness_basis("P")
    assert w3.get("jam") == 0.0
