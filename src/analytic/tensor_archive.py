# src/analytic/tensor_archive.py
# ------------------------------
# Phase 4: Contradiction Tensor Archiving
# Archives contradiction events as phase-rotation tensors for replay and analysis

from dataclasses import dataclass
from typing import List, Dict
from core.phase_geometry import Phase
from core.state import State

@dataclass
class ContradictionTensor:
    id: str
    basis: str  # e.g., "identity_violation", "temporal_conflict"
    origin_phase: Phase
    jammed_phase: Phase
    metadata: Dict[str, str]
    snapshot: State  # Frozen snapshot of state at time of JAM

class TensorArchive:
    def __init__(self):
        self._archive: Dict[str, ContradictionTensor] = {}

    def store_tensor(self, tensor: ContradictionTensor):
        """Store a contradiction tensor by its unique ID."""
        self._archive[tensor.id] = tensor
        print(f"[ARCHIVE] Stored tensor: {tensor.id} with basis: {tensor.basis}")

    def retrieve_by_basis(self, basis: str) -> List[ContradictionTensor]:
        """Retrieve all tensors with a given contradiction basis."""
        return [t for t in self._archive.values() if t.basis == basis]

    def retrieve_all(self) -> List[ContradictionTensor]:
        """Return all stored tensors."""
        return list(self._archive.values())

    def replay_tensor(self, tensor_id: str) -> State:
        """Reconstruct the state snapshot from a contradiction tensor."""
        tensor = self._archive.get(tensor_id)
        if tensor:
            print(f"[ARCHIVE] Replaying state from tensor: {tensor_id}")
            return tensor.snapshot
        else:
            raise ValueError(f"Tensor ID '{tensor_id}' not found in archive.")

    def __contains__(self, tensor_id: str) -> bool:
        """Check if a tensor ID exists in the archive."""
        return tensor_id in self._archive
