import pytest
from scripts.stress_toolkit import compute_stress_index

def test_basic_stress_index():
    summary = {"phase_count": 10, "contradictions": 2}
    prov_events = [
        {"time": 0, "phase": "start", "contradiction": False},
        {"time": 1, "phase": "contradict", "contradiction": True},
        {"time": 2, "phase": "resolve", "contradiction": False},
    ]
    stress = compute_stress_index(summary, prov_events)
    assert 0 <= stress <= 1, "StressIndex should be normalized between 0 and 1"
