# Logic Evaluation Engine (LEE)

**LEE v1.0 – A Phase-State Symbolic Logic Engine**

---

## 🔍 What It Is

LEE is a symbolic logic engine designed for introspective computation, dynamic inference, and memory-aware traceability. It avoids static truth-tables and one-pass inference. Instead, LEE resolves logic as a sequence of *phase-state transitions* between primitive states like `ALIVE`, `MEM`, `JAM`, and `VAC`, defined by structural relationships grounded in counterfactual entailment.

## 🚀 What It Does

- 🔁 **Phase-Aware Evaluation:** Logical expressions evolve through state cycles (e.g., `MEM → ALIVE → JAM → ALIVE`).
- 📘 **Four Primitive States:** The states form the core fabric for reversible computation, derived from the decomposition of material implication.
- 🧠 **Y-Combinator & Recursion Support:** Deep lambda evaluation with structural trace tracking.
- 📦 **Trace Export:** Emits evaluation trace in JSON for reproducibility, auditing, or visualization.
- 🧩 **Modular O---O API:** Clean, introspective modules (Expressions, Evaluation, Substitution, Export, PhaseControl).
- ⚖️ **Conservation-Oriented Inference:** Inspired by differential geometry’s Bianchi identity: logic transformations must preserve internal phase-state coherence.

## 🧬 How It’s Different

Most logic engines:
- Are forward-only (truth-table driven)
- Discard memory of evaluation
- Lack introspection or structural traceability

LEE instead:
- Tracks structural transformations across time.
- Ensures phase-consistent reversibility.
- Embraces logical conservation laws: inference must maintain state integrity.

## 🧠 Core Inspiration

- **Counterfactual Entailment**: von Wright’s logic of “if P had occurred, Q would have followed” serves as LEE’s backbone.
- **Material Implication as Phase Dynamics**: (¬P ∨ Q) is not just syntax—it unrolls into phase-rotations with observable state effects.
- **Bianchi Identity Analogy**: Just as geometric curvature obeys conservation rules, LEE's logic operations must preserve internal consistency and evaluative symmetry.

## ⚙️ Use Cases

- 🧪 Diagnostic Inference Engines (medical, technical systems)
- 📚 Logic Education & Symbolic Reasoning Demonstrators
- 🔬 Scientific Hypothesis Testing (counterfactual model evaluation)
- 🧩 DSL Backend for Structured, Explainable AI

## 📖 Example Expression Trace

```python
identity = Lambda("x", Variable("x"))
expr = Application(identity, Literal(42))
result, trace = evaluate_full(expr)
```

Output Trace:
```json
[
  {"type": "EVAL", "expr": "(λx.x)", "env": {}},
  {"type": "EVAL", "expr": "42", "env": {}},
  {"type": "LITERAL", "expr": "42", "env": {}},
  {"type": "APPLY", "param": "x", "arg": "State.ALIVE", "body": "x"},
  {"type": "EVAL", "expr": "x", "env": {"x": "State.ALIVE"}},
  {"type": "EVAL", "expr": "State.ALIVE", "env": {"x": "State.ALIVE"}}
]
```

## 🌐 Repository Links

- [Main Repo](https://github.com/KILGORETROUT111/logic-evaluation-engine)
- [Project Wiki](https://github.com/KILGORETROUT111/logic-evaluation-engine/wiki)
- [White Paper 1 – Conservation Logic](./White_Paper_1_LEE_Conservation_Logic.pdf)

---

*LEE is built for thinkers, educators, and systems with memory. Logic, after all, isn’t a static table—it’s a living evaluation.*
