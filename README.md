
# Logic Evaluation Engine – Phase-State Inference with Symbolic Substitution

**Author:** William A. Patterson  
**Status:** Active Research Prototype  
**Last Updated:** June 17, 2025

# logic-evaluation-engine
Symbolic phase-state logic engine with functor evaluation, trace export, and Streamlit UI.


🧠 License & Intent
This repository is part of ongoing research in symbolic logic and epistemic computation. Licensing is under review.
For inquiries or collaboration: please contact the author directly.


---

## 🎯 Project Summary

This is a logic engine built for symbolic reasoning, evaluation tracing, and logic-state transitions over structured expressions. It models inferential phases such as `JAM`, `MEM`, `ALIVE`, and `VAC`, and supports:

- Substitutional inference
- Functor-based evaluation
- Trace output for structural logic
- JSON exports for integration
- Web UI for hands-on experimentation

The project bridges formal logic, modal grammar, and symbolic execution models into a single operational environment.

---

## 💻 Folder Structure

logic_engine/
├── core/ # Logic engine modules (expressions, evaluation, state)
├── examples/ # Demo: CLI + JSON export
├── tests/ # Pytest-based unit tests
├── webapp/ # Streamlit web UI
├── main.py # CLI entrypoint
├── README.md # This document


## ✅ Features

- ✅ Phase-aware logic evaluation
- ✅ Traceable substitutions & failure states
- ✅ JSON trace output
- ✅ Command-line interface
- ✅ Web-based interactive logic evaluation (Streamlit)
- ✅ Full test suite with `pytest`


Logic Evaluation Engine Progress Report
Last updated: 2025-06-27

Overview
This document outlines the development progress of the Logic Evaluation Engine — a symbolic reasoning framework designed to support nested logical expressions, traceable state transitions, and interactive evaluation through CLI and Streamlit interfaces.

It is intended for an audience ranging from academic researchers and developers to technical stakeholders and investors.

System Architecture
The engine is structured as a modular Python project with the following core components:

expressions.py: Defines the abstract syntax tree primitives — Functor, Var, and Value.

parser.py: Recursively parses nested JSON-like lists into expression trees.

evaluation.py: Interprets expressions and generates state-based traces.

visualize.py: Outputs .png, .svg, and JSON manifest trace diagrams via Graphviz.

main.py: CLI interface for testing and generating visual outputs.

webapp/app.py: Streamlit interface for live evaluation, expression input, and graph preview.

Each expression is evaluated stepwise to generate a trace with symbolic interpretation.

Features Implemented
✅ Core Primitives
EX(x, JAM): Existential binding
EEX(x, JAM): Counterfactual exploration
SUB(x, φ): Symbolic substitution
MEM: Anaphoric trace recall
LAM(x, φ): Lambda abstraction
APP(f, x): Function application (with substitution)

✅ Expression Parser
Nested JSON parsing for symbolic expressions
Supports primitives, lists, and dictionaries ({"value": 3} becomes Value(3))

✅ Evaluation Tracer
Evaluation engine produces state transitions (ALIVE, JAM, VAC, etc.)
Automatically logs expression phases
Prevents circular evaluation and hash errors

✅ CLI Interface
CLI prompt with contextual input
Expression-to-trace output with terminal preview
Graphviz-based .svg/.png/JSON output

✅ Streamlit App
Rich UI with example input box
Success + error feedback for parsing/evaluation
Downloadable trace diagram with timestamp and versioning

Known Issues / Limitations
CLI does not yet support piping or shell arguments without quoting issues
Some deeply nested substitutions or context-aware recursion may not trigger expected symbolic outcomes
Streamlit app lacks auto-diagram preview (though .svg/.png can be generated via CLI)


Next Steps
Expression Inference Layer:

Introduce modal logic: resolve possible vs. actual expression states.
Extend memory (MEM) to conditionally resolve previous SUB or LAM.
Substitution Logic Refinement:

Refactor substitution function for α-renaming safety.
Cache resolved forms where possible.
Streamlit Enhancements:

Auto-embed visual diagram (.svg) on success.
Add session memory and annotation features.
GitHub Packaging + Documentation:

Prepare public README with architecture diagram and example walkthroughs.
Tag v0.9.1 and v1.0.0 milestone.
Paper/Publication:

Write and release accompanying paper explaining symbolic inference engine
Comparison with lambda calculus, modal inference, and anaphora in NLP
© 2025 Logic Evaluation Engine Development Team.
