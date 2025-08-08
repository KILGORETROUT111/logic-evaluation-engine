# ✅ Phase 2 Patch — LEE v3.0 Reboot
# Target: core/state.py and core/contradiction.py
# Purpose: Upgrade to phase-aware dynamics, VAC state, contradiction logging

# ------------------------------
# PATCH: core/state.py
# ------------------------------

from enum import Enum, auto
from typing import Any, Dict, List, Optional

class Phase(Enum):
    MEM = auto()
    ALIVE = auto()
    JAM = auto()
    VAC = auto()  # New: vacuum / null-state phase

class State:
    def __init__(self, 
                 phase: Phase = Phase.MEM, 
                 environment: Optional[Dict[str, Any]] = None,
                 trace: Optional[List[str]] = None,
                 entropy: float = 0.0,
                 contradiction: Optional[Dict] = None):
        self.phase = phase
        self.environment = environment if environment is not None else {}
        self.trace = trace if trace is not None else []
        self.entropy = entropy
        self.contradiction = contradiction

    def transition(self, new_phase: Phase):
        self.trace.append(f"{self.phase.name} → {new_phase.name}")
        self.phase = new_phase

    def jam(self, reason: str):
        self.transition(Phase.JAM)
        self.contradiction = {
            "reason": reason,
            "environment": self.environment.copy(),
            "entropy": self.entropy,
            "trace": self.trace[:],
        }

    def vac(self):
        self.transition(Phase.VAC)
        self.environment.clear()
        self.entropy = 0.0
        self.trace.append("State reset to VAC")

    def is_terminal(self) -> bool:
        return self.phase in {Phase.JAM, Phase.VAC}

    def __repr__(self):
        return (f"<State phase={self.phase.name} env={list(self.environment.keys())} "
                f"entropy={self.entropy:.2f} trace_len={len(self.trace)}>")


# ------------------------------
# PATCH: core/contradiction.py
# ------------------------------

from typing import Tuple
from core.state import State, Phase


def detect_contradiction(lhs: Any, rhs: Any) -> bool:
    """Basic equality check for contradiction."""
    return lhs != rhs


def handle_contradiction(state: State, lhs: Any, rhs: Any, context: str = "") -> State:
    if detect_contradiction(lhs, rhs):
        reason = f"Contradiction detected: {lhs} ≠ {rhs}"
        if context:
            reason += f" in {context}"
        state.jam(reason)
    return state


def contradiction_summary(state: State) -> str:
    if not state.contradiction:
        return "No contradiction recorded."
    return (f"CONTRADICTION: {state.contradiction['reason']}\n"
            f"Entropy: {state.contradiction['entropy']:.2f}\n"
            f"Trace: {state.contradiction['trace']}")
