# LEE v3.0 Reboot Initialization
# File: src/__init__.py
# Purpose: foundational module scaffolding for self-projective logic engine

# Directory structure (proposed and approved):
# src/
#   core/          : Primitive logical structures and phase dynamics
#   analytic/      : Advanced contradiction mapping and energy modeling
#   nlp/           : Language preprocessing (no TMA)
#   engine/        : Execution engine, memory, evaluation loop

# This __init__.py sets up namespace exposure and base imports

# Phase 0: Core logic primitives and system base
from .core.expressions import Variable, Lambda, Application, Quantifier
from .core.combinators import Y_combinator, Z_combinator
from .core.phase_geometry import rotate_phase, PhaseState
from .core.contradiction import detect_contradiction, jam_trace
from .core.state import make_blank_state, transition_state

# Phase 1: Analytic dynamics
from .analytic.tensor_archive import archive_tensor, recall_tensor
from .analytic.energy_dynamics import compute_lioness_energy
from .analytic.counterfactual import rewind_path, replay_path
from .analytic.divergence_map import map_logical_divergence

# Phase 2: NLP substrate (structural only)
from .nlp.parser import parse_expression
from .nlp.rewriter import rewrite_expression
from .nlp.scope_inference import infer_scope
from .nlp.named_entities import extract_logical_atoms

# Phase 3: Evaluation Engine
from .engine.evaluator import evaluate_full
from .engine.memory_store import memory_push, memory_lookup
from .engine.event_log import log_event, render_svg_history
from .engine.logic_hooks import external_callout

# Note: All modules must enforce deterministic phase rotation under contradiction.
# Core principle: Jammed state (JAM) is the only admissible transition failure,
# and must yield reentrant resolution through Phase Geometry.

__all__ = [
    "Variable", "Lambda", "Application", "Quantifier",
    "Y_combinator", "Z_combinator",
    "rotate_phase", "PhaseState",
    "detect_contradiction", "jam_trace",
    "make_blank_state", "transition_state",
    "archive_tensor", "recall_tensor",
    "compute_lioness_energy",
    "rewind_path", "replay_path",
    "map_logical_divergence",
    "parse_expression", "rewrite_expression",
    "infer_scope", "extract_logical_atoms",
    "evaluate_full", "memory_push", "memory_lookup",
    "log_event", "render_svg_history", "external_callout"
]
