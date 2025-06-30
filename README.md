# Logic Evaluation Engine

A modular symbolic reasoning system for evaluating logic expressions using Functor-based ASTs and trace-based evaluation. Designed to support modal, counterfactual, and lambda-calculus-style inference in a lightweight, extensible framework.

## 🚀 Key Features

- **Expression Parser**: Parses symbolic JSON-like or list-based structures into composable expression trees.
- **Evaluator Engine**: Stateful evaluator supporting EX, EEX, SUB, MEM, APP, and LAM logic primitives.
- **Trace System**: Evaluation traces are captured per state (ALIVE, VAC, MEM, etc.) and exportable.
- **Visualization**: Graphviz-rendered .svg and .png output of evaluation traces.
- **Streamlit Interface**: Live interactive web interface for expression evaluation and diagram preview.
- **CLI Interface**: Lightweight terminal-based evaluation with diagram+JSON export.
- **Extensible Architecture**: Add new logical primitives, visualizations, or inference modes.

## 📂 Folder Structure


logic-evaluation-engine/
│
├── core/               # Core logic: expressions, parser, evaluation, visualize
├── webapp/             # Streamlit-based web interface (run with `streamlit run webapp/app.py`)
├── examples/           # Expression demos
├── tests/              # Pytest unit tests
├── out/                # Output diagrams (.svg/.png) and trace logs
├── main.py             # CLI evaluator
├── README.md           # This file
└── LICENSE             # GNU GPLv3



## ✅ Expression Examples

json

["EX", "x", "JAM"]
["EEX", "x", "JAM"]
["SUB", "x", ["EX", "y", "JAM"]]
["MEM", "x"]
["APP", ["LAM", "x", ["EX", "x", "JAM"]], 42]
["Root", ["SUB", "x", 42], ["Node", {"value": 3}, "MEM", "x"]]


## 🔍 Evaluation States

- `State.ALIVE`: Expression resolved and bound
- `State.VAC`: Empty or default state
- `State.MEM`: Memory resolved
- `State.JAM`: Failure or paradox state

## 🧠 Research Scope

This project explores symbolic reasoning and inference by composing small primitives, emulating features from:
- Modal logic
- Counterfactual logic
- Lambda calculus
- Anaphora & dynamic binding

Ideal for AI explainability, formal logic prototyping, or educational logic engines.

## 📦 Installation

bash
pip install -r requirements.txt
python main.py


## 🖼️ Web Interface

bash
streamlit run webapp/app.py


## 📁 Output

- `/out`: SVG + PNG diagram visualizations
- `/out/*.json`: Trace manifest logs

## 🧪 Tests

bash
pytest tests/


## 🏷️ Version

**v0.9.0-alpha** — Early alpha, fully working logic core with extensible primitives.



## 🎯 Project Summary

This is a logic engine built for symbolic reasoning, evaluation tracing, and logic-state transitions over structured expressions. It models inferential phases such as `JAM`, `MEM`, `ALIVE`, and `VAC`, and supports:

- Substitutional inference
- Functor-based evaluation
- Trace output for structural logic
- JSON exports for integration
- Web UI for hands-on experimentation

The project bridges formal logic, modal grammar, and symbolic execution models into a single operational environment.



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
Last updated: 2025-06-30

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
Tag v0.9.2 and v0.9.2.1 milestone.
Paper/Publication:

Write and release accompanying paper explaining symbolic inference engine
Comparison with lambda calculus, modal inference, and anaphora in NLP
Copyright 2025 Logic Evaluation Engine Development Team.

Copyright 2025 Logic Evaluation Engine creator and inventor William A. Patterson. For more info, see wiki page or contact maintainer at dianoetic@tuta.com
04af6e0 (✅ Finalize logic engine v0.9.2: lambda + app + substitution inference). 

Logic Evaluation Engine is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version. Logic Evaluation Engine is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details. You should have received a copy of the GNU General Public License along with Logic Evaluation Engine. If not, see <https://www.gnu.org/licenses/>.
