# Logic Evaluation Engine (LEE)

**A symbolic reasoning framework for structured substitution, lambda evaluation, and visual logic tracing.**

---

## Overview

The Logic Evaluation Engine (LEE) is a lightweight, expressive system for evaluating symbolic logic expressions through substitutional reasoning and state tracing.

It was built to assist in exploring, teaching, and experimenting with lambda expressions, modal logic, and quantifiers — all while exposing a transparent trace of the logic flow.

Whether you're modeling inference rules, experimenting with recursive expressions, or teaching symbolic logic, LEE makes the process legible, testable, and extendable.

---

## Key Features

- **Lambda Calculus Support**
  - Application, abstraction, and scope tracking
  - Nested applications with substitution
  - Recursive evaluation using combinators (e.g. Y-Combinator)

- **Quantifier Logic**
  - Supports ∀ (universal) and ∃ (existential) structures
  - Evaluates over simulated domains of discourse

- **Substitutional Evaluation**
  - `Variable`, `Literal`, `Define`, `Substitution`, `Application`, and `Lambda` types
  - Traceable and expressive step-by-step computation

- **Trace Visualization**
  - Outputs inference paths as PNG, SVG, and proof-style logs
  - CLI and Streamlit UI options for interactive or scripted use

- **Stateful Outcome Modeling**
  - Expressions resolve to symbolic states: `ALIVE`, `JAM`, or `VOID`
  - Useful for modal, epistemic, or logical condition tracking

- **Extensible Expression System**
  - Plug in custom expression types (e.g. If-Then, BinaryOp)
  - Compose hybrid logic models

---

## Use Cases

### 🧠 Academic & Pedagogical

- Teaching lambda calculus and substitution
- Demonstrating quantifier scoping and binding
- Visualizing logical inference flow
- First-year logic instruction (formal reasoning, functional programming)
- Coursework demos for CS, Philosophy, and Math departments

### 🧪 Logic Research & Experimentation

- Custom modal or substitution logics
- Exploratory logic modeling for AI inference
- Trace validation for symbolic computation pipelines

---

## Example

```python
from core.expressions import Variable, Literal, Lambda, Application
from core.evaluation import evaluate_full

# Define λx.λy.x
inner = Lambda("y", Variable("x"))
outer = Lambda("x", inner)

# Apply: ((λx.λy.x) 1) 2
expr = Application(Application(outer, Literal(1)), Literal(2))

result, trace = evaluate_full(expr)

for step in trace:
    print(step)
```

This yields a full trace of variable binding, lambda scope, and evaluation steps — all visibly structured.

---

## Visualization Example

Evaluate and render substitution logic as SVG/PNG for teaching or analysis:

```bash
python main.py --expr "(LAM x (LAM y x))" --apply "1" "2" --output "trace.svg"
```

---

## Repository Structure

- `core/expressions.py` — all expression types (Variable, Literal, Lambda, etc.)
- `core/evaluation.py` — recursive trace-evaluator
- `core/state.py` — symbolic end-state tracking
- `core/visualize.py` — DOT/SVG/PNG renderers
- `trace_to_proof.py` — readable output logs for logic proofs
- `main.py` — CLI interface
- `demo_*.py` — example test and demonstration files

---

## Status

**Alpha release v0.9.2.3** — actively iterating.

We welcome academic collaborators, feedback from instructors, and early experimental use.

---

## License

GNU General Public License v3.0.

---
Wiki: https://github.com/KILGORETROUT111/logic-evaluation-engine/wiki/wiki-Phase-Evaluation
---

## Contact

William A. Patterson  
Email: [dianoetic@tuta.com](mailto:dianoetic@tuta.com)  
CC: [kilgoretrout@berkeley.edu](mailto:kilgoretrout@berkeley.edu)
