# counterfactual.py
# LEE v3.0 — Phase 5
# Rewinds memory and simulates alternate paths

from core.state import State
from core.contradiction import ContradictionArchive
from engine.memory_store import memory_lookup

class CounterfactualEngine:
    def __init__(self, archive: ContradictionArchive):
        self.archive = archive

    def rewind_state(self, patient_id, event_index):
        history = memory_lookup(patient_id)
        if history and 0 <= event_index < len(history):
            return history[event_index].clone()
        return None

    def simulate_alternate(self, state: State, alternate_event):
        state.apply_event(alternate_event)
        return state

    def explore_contradiction(self, contradiction_id):
        contradiction = self.archive.retrieve(contradiction_id)
        if not contradiction:
            return None

        patient_id = contradiction.context.get("patient_id")
        origin_index = contradiction.context.get("event_index")
        original_state = self.rewind_state(patient_id, origin_index)

        alternates = contradiction.context.get("alternates", [])
        paths = []
        for alt_event in alternates:
            alt_state = original_state.clone()
            alt_state.apply_event(alt_event)
            paths.append(alt_state)
        return paths
