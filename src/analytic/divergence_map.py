# File: analytic/divergence_map.py
# LEE v3.0 - Phase 5 Module
# Tracks divergence pathways stemming from contradictions (JAM)

from core.phase_geometry import Phase
from core.expressions import Expression

class DivergenceMap:
    def __init__(self):
        self.divergence_paths = {}  # {source_event_id: [alt_event_ids]}

    def register_divergence(self, from_event_id, to_event_id):
        if from_event_id not in self.divergence_paths:
            self.divergence_paths[from_event_id] = []
        self.divergence_paths[from_event_id].append(to_event_id)

    def get_divergent_paths(self, from_event_id):
        return self.divergence_paths.get(from_event_id, [])

    def trace_full_divergence(self, from_event_id):
        """ Recursively walk all divergences spawned from a JAM event """
        visited = set()
        results = []

        def _trace(eid):
            if eid in visited:
                return
            visited.add(eid)
            for diverged in self.get_divergent_paths(eid):
                results.append(diverged)
                _trace(diverged)

        _trace(from_event_id)
        return results


# File: analytic/counterfactual.py
# LEE v3.0 - Phase 5 Module
# Rewind and replay logic from JAM back to ALIVE for alternate resolution

from engine.memory_store import retrieve_memory_events
from engine.event_log import replay_event_sequence
from core.phase_geometry import Phase
from core.state import make_blank_state
from core.expressions import Expression
from analytic.divergence_map import DivergenceMap

class CounterfactualEngine:
    def __init__(self):
        self.divergence_map = DivergenceMap()

    def fork_from_jam(self, jam_event_id, alternate_inputs):
        """Start from a JAM and simulate alternate histories."""
        prior_events = retrieve_memory_events(jam_event_id)
        state = make_blank_state()
        replay_event_sequence(prior_events, state)

        alt_event_ids = []
        for alt_input in alternate_inputs:
            # This can include alternate symptoms, expressions, observations
            new_event_id = state.process_input(alt_input)
            self.divergence_map.register_divergence(jam_event_id, new_event_id)
            alt_event_ids.append(new_event_id)

        return alt_event_ids

    def explore_counterfactuals(self, jam_event_id):
        return self.divergence_map.trace_full_divergence(jam_event_id)
    
# divergence_map.py
# LEE v3.0 — Phase 5
# Tracks divergence trees arising from JAM-state contradictions

from core.state import State
from core.contradiction import ContradictionArchive

class DivergenceNode:
    def __init__(self, state: State, cause: str, parent=None):
        self.state = state
        self.cause = cause
        self.parent = parent
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)

    def trace_path(self):
        path = []
        node = self
        while node:
            path.insert(0, (node.cause, node.state.phase))
            node = node.parent
        return path

class DivergenceMap:
    def __init__(self):
        self.roots = []

    def register_divergence(self, parent_state, jam_cause):
        forked_state = parent_state.clone()
        forked_state.rotate_phase("JAM")
        new_node = DivergenceNode(forked_state, jam_cause, parent=None)
        self.roots.append(new_node)
        return new_node

    def expand_from(self, node, new_cause):
        new_state = node.state.clone()
        new_state.rotate_phase("MEM")
        child_node = DivergenceNode(new_state, new_cause, parent=node)
        node.add_child(child_node)
        return child_node

    def all_paths(self):
        paths = []
        def walk(node, acc):
            acc.append((node.cause, node.state.phase))
            if not node.children:
                paths.append(list(acc))
            for child in node.children:
                walk(child, acc[:])
        for root in self.roots:
            walk(root, [])
        return paths



