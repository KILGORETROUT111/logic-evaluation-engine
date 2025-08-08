# LEE v3.0 - Phase 3: energy_dynamics.py
# Purpose: Track energy deltas from Basis5 shifts to phase rotations. Entropy and conservation logic.

from datetime import datetime
from collections import defaultdict
import math

# ---------------------------------------------
# Energy Unit Model
# ---------------------------------------------

class BasisEnergy:
    def __init__(self):
        self.last_basis = None
        self.total_energy = 0.0
        self.entropy_log = []

    def delta(self, new_basis):
        if self.last_basis is None:
            self.last_basis = new_basis
            return 0.0

        delta = sum(1 for b1, b2 in zip(self.last_basis, new_basis) if b1 != b2)
        energy = delta ** 2
        self.total_energy += energy

        entropy = -math.log2(1 / (delta + 1)) if delta > 0 else 0.0
        self.entropy_log.append((datetime.utcnow(), entropy))

        self.last_basis = new_basis
        return energy

# ---------------------------------------------
# Global Energy Tracker
# ---------------------------------------------

class EnergyRegistry:
    def __init__(self):
        self.registry = defaultdict(BasisEnergy)

    def observe(self, patient_id, current_basis):
        energy = self.registry[patient_id].delta(current_basis)
        return energy

    def total_energy(self, patient_id):
        return self.registry[patient_id].total_energy

    def entropy_timeline(self, patient_id):
        return self.registry[patient_id].entropy_log


# Singleton
energy_tracker = EnergyRegistry()

# LEE v3.0
# Phase 4: Basis Energy Dynamics
# File: src/analytic/energy_dynamics.py

from core.phase_geometry import Phase, rotate_phase_clockwise
from core.state import DiagnosticState

class BasisDelta:
    """Delta in basis-level observations."""
    def __init__(self, from_basis: set, to_basis: set):
        self.from_basis = from_basis
        self.to_basis = to_basis
        self.new_terms = to_basis - from_basis
        self.dropped_terms = from_basis - to_basis

    def entropy(self) -> int:
        """Entropy is defined as the number of changes in the basis."""
        return len(self.new_terms) + len(self.dropped_terms)

    def __repr__(self):
        return f"BasisDelta(+{self.new_terms}, -{self.dropped_terms})"

class EnergyEvaluator:
    """Maps ΔBasis to phase transitions via energy dynamics."""

    @staticmethod
    def delta_to_energy(delta: BasisDelta) -> float:
        """Convert basis delta into energy scalar (simple entropy model)."""
        return delta.entropy()  # Simple model: 1 unit per change

    @staticmethod
    def apply_to_state(state: DiagnosticState, delta: BasisDelta) -> DiagnosticState:
        """Advance state if energy exceeds threshold."""
        energy = EnergyEvaluator.delta_to_energy(delta)
        threshold = 2  # Static threshold for rotation
        if energy >= threshold:
            new_phase = rotate_phase_clockwise(state.phase)
            return DiagnosticState(phase=new_phase, memory=state.memory.copy())
        return state

