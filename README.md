# Logic Evaluation Engine (LEE) – v0.9.3

The **Logic Evaluation Engine (LEE)** is a symbolic inference framework designed for introspective logic processing, real-time event tracing, and composable expression evaluation. Built to support reproducibility and formal inspection, LEE serves as a clean-room logic substrate that bridges expressive symbolic rules with concrete memory and substitution semantics.

---

## 🔍 Key Features

- **Event-Driven Execution**  
  All evaluation steps emit structured `LEEEvent`s, enabling real-time introspection, cycle detection, anti-pattern recognition, and symbolic trace capture.

- **JSON Trace Export**  
  Every evaluation run can be exported as a structured JSON file. Ideal for use in reproducibility contexts, symbolic debugging, or GUI diagnostics.

- **Y Combinator Demonstration**  
  Includes example evaluation of a non-trivial fixed-point recursive combinator via lambda-calculus construction.

- **State Phase Control**  
  Expression state transitions follow phase-logical lifecycle: `VAC → ALIVE → MEM` (with `JAM` for contradiction detection and halt conditions).

- **Modular API Interface (O---O)**  
  Clean API segmentation for expression handling, substitution control, evaluation, export, and phase-state inspection.  
  The `O---O API` is LEE’s external face: symbolic, inspectable, and migratable.

---

## 🧠 Why LEE Matters

LEE is built for symbolic transparency and reproducibility. It enables logic processing systems that can:
- Expose their own inference trace in real time,
- Integrate phase-state lifecycle semantics,
- Support downstream tools that visualize, annotate, or diagnose logical computation.

Whether you're a logician, a symbolic AI developer, or a systems researcher, LEE offers a core substrate to **build or test introspective symbolic logic**—without reliance on opaque LLMs or probabilistic black-boxes.

---

## 📂 Project Structure

```plaintext
logic-evaluation-engine/
├── core/                # Core logic: expressions, evaluation, state, event types
├── utils/               # Utilities: safe_print, JSON trace export
├── demos/               # Demonstration scripts incl. Y combinator, trace inspection
├── tests/               # Formal verification test cases
├── out/                 # Output directory for runtime JSON traces
├── README.md
└── main.py              # Example runtime entry point
```

---

## 🚀 Try It

Run `main.py` to see the engine evaluate a small expression and emit a JSON trace:

```bash
python main.py
```

Check the generated trace in:

```bash
out/trace_output.json
```

---

## 🧪 Tests and Demos

- Run all tests:

```bash
pytest tests/
```

- Explore demos:

```bash
python demos/demo_y_combinator.py
python demos/demo_trace_to_proof.py
```

---

## 🔗 Related Papers & Foundations

LEE is grounded in formal logic research. This research informs its deep structure and is integral to its philosophical and architectural design.  
**DOI #s are forthcoming.**

---

## 🔧 License

**GPL v3.0**  
Open, transparent, and reusable. All logic artifacts, demos, and trace exports are subject to this license.

---

## 🔭 Future Directions

- GUI inspection (e.g. Streamlit or Qt for visualizing traces and phases)
- Graph-based pattern detection and cycle mapping
- RESTful or CLI interface for `O---O API` exposure
- Full symbolic-to-proof compiler path (β reduction with trace)
- Phase audit hooks for forensic logic and runtime introspection

---

## 🧬 Design Notes

- JAM and MEM phases follow strict logic rules:
  - `JAM → MEM` (awaiting contradiction resolution)
  - `MEM → ALIVE` (triggered by valid substitution)
  - No `MEM → JAM`, no `MEM → VAC`, unless reset or forcibly overwritten.
- All events are exported in `LEEEvent` form for downstream use.
- Engine is deliberately self-contained: no internet calls, no dependencies outside `Python 3.9+`.

---

## 🛠️ Development Status

Actively maintained. Contributions welcome via fork + PR.  
Contact: [dianoetic@tuta.com](mailto:dianoetic@tuta.com)
Contact CC: [kilgoretrout@berkeley.edu](mailto:kilgoretrout@berkeley.edu)