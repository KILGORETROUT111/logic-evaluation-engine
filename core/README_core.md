
# 🧠 Core Module Overview – Logic Evaluation Engine (LEE)

The `core/` directory defines the symbolic and structural model that underlies LEE's logical inference system. It provides:

- Expression definitions
- State handling for memory, phase, and contradiction tracking
- Evaluation scaffolding and closure-aware reasoning
- Event-modeling architecture for tracing logical transitions

---

## 📘 Modules

| File                            | Description |
|---------------------------------|-------------|
| `evaluate_full_closure_aware.py` | Logical evaluation with closure tracking across forks |
| `evaluation.py`                 | Central inference orchestrator (connects expressions, states, events) |
| `events.py`                     | Generic event modeling framework |
| `lee_event.py`                  | LEE-specific event lifecycle (for phase rotation, contradictions) |
| `expressions.py`                | Symbol and expression container models |
| `parser.py`                     | Parses logical input (facts, axioms) into expression trees |
| `states.py`                     | Tracks phase state (e.g. `ϕ₀`, `ϕ₁`) and contradiction flags |
| `phase.py`                      | Logic phase transformations (possible vs actual) |
| `visualize.py`                  | Renders inference flow and proof trace visuals |
| `patch_notes_final_eval.txt`   | Internal documentation of model changes |
| `__init__.py`                   | Declares `core` as a package |
