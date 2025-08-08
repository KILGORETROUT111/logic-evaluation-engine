# src/core/state.py

from typing import Any, Dict, List, Optional
from core.phase_geometry import Phase  # ← single source of truth

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