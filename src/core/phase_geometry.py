from enum import Enum, auto
from dataclasses import dataclass
from typing import Dict, Tuple, Optional

class Phase(Enum):
    MEM = auto()
    ALIVE = auto()
    JAM = auto()
    VAC = auto()  # Phase of vacuum reset / nullification

@dataclass
class PhaseEdge:
    from_phase: Phase
    to_phase: Phase
    weight: float

# Define default phase rotation graph
PHASE_GRAPH: Dict[Phase, Tuple[Phase, float]] = {
    Phase.MEM:   (Phase.ALIVE, 1.0),
    Phase.ALIVE: (Phase.JAM,   1.0),
    Phase.JAM:   (Phase.VAC,   1.0),
    Phase.VAC:   (Phase.MEM,   1.0),
}

def rotate_phase(phase: Phase) -> Optional[Phase]:
    """Return the next phase in rotation."""
    return PHASE_GRAPH.get(phase, (None,))[0]

def inverse_phase(phase: Phase) -> Optional[Phase]:
    """Return the previous phase in rotation."""
    for prev, (next_, _) in PHASE_GRAPH.items():
        if next_ == phase:
            return prev
    return None
