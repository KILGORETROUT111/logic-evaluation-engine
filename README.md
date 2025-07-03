# Logic Evaluation Engine

*It started with an acorn. It got planted. Now we’ve got foot-lumber.*  
A metaphor for the LEE's evolution — from conceptual seed to structural reasoning engine.




---

The Logic Evaluation Engine (LEE) is a symbolic logic framework for evaluating structured expressions using functor-based parsing, substitution chains, lambda-calculus inference, and memory-sensitive phase transitions. It’s compact, inspectable, and traceable — built for education, prototyping, and symbolic experimentation.

Whether you're modeling substitution failures, modal conditionals, lambda-applications, or inference structures across memory states, LEE tracks each evaluative **phase**: `ALIVE`, `JAM`, `MEM`, `VAC`, and beyond.

---

## 🚀 Key Features

- **Expression Parser**: Parses symbolic JSON-like or list-based structures into composable expression trees.
- **Evaluator Engine**: Stateful evaluator supporting EX, EEX, SUB, MEM, APP, and LAM logic primitives.
- **Trace System**: Evaluation traces are captured per state (ALIVE, JAM, MEM, etc.) and exportable.
- **Visualization**: Graphviz-rendered .svg and .png output of evaluation traces.
- **Streamlit Interface**: Live interactive web interface for expression evaluation and diagram preview.
- **CLI Interface**: Lightweight terminal-based evaluation with diagram+JSON export.
- **Extensible Architecture**: Add new logical primitives, visualizations, or inference modes.

---

## 🧠 Why Use This Engine

LEE is not a theorem prover or a toy model. It’s a symbolic reasoning core built to:

- Make substitution steps visible.
- Trace how meaning collapses, persists, or mutates across evaluation.
- Explore logic as structure-in-motion — not just result.

Its modular design supports research in modal logic, lambda inference, symbolic cognition, AI interpretability, and dynamic variable binding.

---

## ✅ Expression Examples

```json
["EX", "x", "JAM"]
["EEX", "x", "JAM"]
["SUB", "x", ["EX", "y", "JAM"]]
["MEM", "x"]
["APP", ["LAM", "x", ["EX", "x", "JAM"]], 42]
["Root", ["SUB", "x", 42], ["Node", {"value": 3}, "MEM", "x"]]
```

---

## 🌀 Evaluation Phases

- `ALIVE`: Expression resolved and bound
- `JAM`: Structural obstruction or paradox
- `MEM`: Memory-based lookup or symbolic recall
- `VAC`: Placeholder or null state

Each expression walks through phases tracked in the evaluation trace.

---

## 📂 Folder Structure

```
logic-evaluation-engine/
├── core/         # Logic primitives, parser, evaluator, visualizer
├── webapp/       # Streamlit web UI
├── examples/     # JSON-based logic expression demos
├── tests/        # Pytest-based unit tests
├── out/          # Trace output (.json, .svg, .png)
├── main.py       # CLI entrypoint
├── README.md     # This document
└── LICENSE       # GNU GPLv3
```

---

## 📦 Installation

```bash
pip install -r requirements.txt
python main.py
```

## 🖼️ Web Interface

```bash
streamlit run webapp/app.py
```

---

## 🧪 Run Tests

```bash
pytest tests/
```

---

## 🔗 GitHub Repository

[github.com/KILGORETROUT111/logic-evaluation-engine](https://github.com/KILGORETROUT111/logic-evaluation-engine)

---

© 2025 William A. Patterson. Licensed under GNU GPLv3.
For collaboration inquiries, contact: dianoetic@tuta.com
CC: kilgoretrout@berkeley.edu
