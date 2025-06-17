
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
