# LEE Gives ALIVE

# Logic Evaluation Engine (LEE)

🚨 **To all you mathy CS types, logicians, and proof jockeys — hear this:**

> **Pushing code isn’t surgery. It’s midwifery.**  
> You're not cutting — you're catching.  
> You're not fixing — you're witnessing.  
> **LEE** doesn't "compile" logic. It **births** it.  

There are no sterile gloves in this repo.  
Only **rotating phase states**, **inference chains**, and the **cry of a valid conclusion.**  

You want formal logic?  
You want symbolic traceability?  
You want reasoning that earns its result?  

**LEE gives ALIVE.**

🧬 [logic-evaluation-engine](https://github.com/KILGORETROUT111/logic-evaluation-engine)  
⚙️ v1.1 — Now Pushed. Now Born.  
📢 Share if you believe code should reason, not just run.
**Status**: Active Development  
**License**: GPL-3.0 

---

## 🧠 What Is LEE?

The **Logic Evaluation Engine (LEE)** is a lightweight, self-contained logic execution environment built for symbolic reasoning, diagnostic inference, and dynamic proof-chain evaluation. It handles contradictory input, reentrant substitution, quantified logic, and truth-phase resolution with traceable precision.

LEE is designed as a **symbolic counterweight to opaque ML systems**, ideal for fields where **transparent inference, step-traceable evaluation**, and **controlled symbolic logic** matter.

---

## 🔍 What Can It Do?

- ✅ **Evaluate symbolic expressions** (lambda, operators, propositional logic)
- ✅ **Trace substitutions, inference chains, contradictions, and recovery**
- ✅ **Run diagnostic logic flows** with memory and error phase-handling
- ✅ **Export proof traces** to JSON or Markdown
- ✅ **Resolve quantified expressions (∀, ∃)** across scoped domains
- ✅ **Run from command line** via `cli_runner.py` with argument support
- ✅ **Log and capture evaluations** to timestamped files
- ✅ **Map to real-world reasoning** (e.g., medical/legal inference, pricing)

---

## 📁 Repo Layout

```
logic-evaluation-engine/
├── core/                       # Core symbolic logic modules
│   ├── evaluation.py
│   ├── parser.py
│   ├── phase.py
│   ├── states.py
│   └── ...
├── evaluation/                 # Diagnostic, quantifier, proof logic
│   ├── context_scope.py
│   ├── quantifier_engine.py
│   ├── proof_engine.py
│   ├── unifier.py
│   └── test_*.py
├── utils/                      # Logging and trace helpers
│   ├── logging.py
│   └── trace_export.py
├── docs/
│   ├── philosophy/
│   │   ├── LEE_Tribute_JulianBoyd.md
│   │   └── LEE_WhitePaper_Fragmented.md
│   └── high-ground-use-case-exhibits/
│       └── LegalLogic_MedicalInference_Model.md
├── logs/
│   └── test_log_template.md
├── main.py                     # Basic starter runner
├── cli_runner.py              # CLI interface for quick eval + proof
├── README.md
└── LICENSE.txt
```

---

## 🧪 Example Capabilities

### ✅ Symbolic Proof Derivation

```bash
python -m evaluation.proof_engine "Q(a)"
```

**Output:**
```txt
Proof result: True
Trace:
   Given fact: P(a)
   Axiom A1: ¬P(x) ∨ Q(x)
   Substitution: {'x': 'a'}
   Instantiated: ¬P(a) ∨ Q(a)
   Disjunction Eval: (¬P(a))=False, (Q(a))=False
   → Derived Q(a) via disjunctive syllogism on A1

# 🌊 Logic Evaluation Engine (LEE) – Ride the Wave of Symbolic Inference

Welcome to LEE — a lightweight, phase-consistent symbolic logic engine that doesn't just evaluate expressions — it **resolves tension**, **rotates truth**, and **derives consequence** like a wave barreling through the reef of ambiguity.

![Surf LEE](https://beachgrit.com/wp-content/uploads/2015/08/Screen-Shot-2015-08-15-at-8.09.21-am-1024x566.png)

---

## 🧠 What LEE Is

- A symbolic logic engine written in Python.
- Capable of evaluating propositional and predicate logic (∧, ∨, ¬, →, ∀, ∃).
- Tracks **quantifier scope**, **axioms**, and **phase-state truth transitions**.
- Proves consequence through substitution, unification, and inference tracing.
- Outputs `.md` and `.json` traces for full auditability.

Built for diagnostics, law, counterfactuals, and AI logic systems.

---

## 📁 Repo Structure

```bash
/evaluation/
  ├── evaluate.py             # Main logic engine
  ├── quantifier_engine.py    # ∀ / ∃ logic
  ├── unifier.py              # Pattern matching
  ├── proof_engine.py         # Axiom-based derivation
  ├── context_scope.py        # Runtime-scoped domains
  └── cli.py                  # Run from command line

/docs/
  ├── philosophy/
  │   ├── LEE_Tribute_JulianBoyd.md
  │   └── LEE_WhitePaper_Fragment.md
  └── high-ground-use-case-exhibits/
      └── Exhibit_A_Legal_Medical_Logic_Inference.md
5c7371b (Release LEE v1.1 — Diagnostic Logic Engine, Proof Mode, CLI)
```

---

### 🩺 Medical Use Case Integration

Use-case and implementation logic are documented in the wiki:  
▶ **[Medical Diagnostic Logic Engine — v1.1](https://github.com/KILGORETROUT111/logic-evaluation-engine/wiki/Medical-Use-Case-–-v1.1-Diagnostic-Logic-Engine)**

---

## 🌐 Real-World Applications

- **Diagnostic Reasoning** (Medical, Fault Tree, Causal Systems)
- **Legal Inference Modeling** (Modality, obligation, violation detection)
- **AI-ML Interface** (Explainability layer for black-box inference)
- **Pricing Rules Validation** (e.g., SAP SD Pricing Debug Tracing)
- **Symbolic Reasoning** in Logic Courses or Research Prototypes

---

## 💡 Why It Matters

**LEE earns its inference.**  
Unlike ML models, every step in LEE is logically traceable, reproducible, and falsifiable.  
It combines **phase-aware evaluation**, **symbolic expressiveness**, and **modular extensibility** in ~1k lines.

---

## 🔗 Related

- 🔬 [Julian Boyd Tribute – Modal & Legal Logic](docs/philosophy/LEE_Tribute_JulianBoyd.md)
- 📎 [High-Ground Use Case: Legal Logic + Medical Inference](docs/high-ground-use-case-exhibits/LegalLogic_MedicalInference_Model.md)
- 🌊 [LEE_WhitePaper_Fragmented.md](docs/philosophy/LEE_WhitePaper_Fragmented.md)
- 🧾 [Proof Traces in Markdown/JSON](proof_Qa.md, proof_trace_Q_a_.json)
- 📓 Wiki: [Medical Use Case Logic](https://github.com/KILGORETROUT111/logic-evaluation-engine/wiki)

---

## 📌 Author / Contact

GitHub: [KILGORETROUT111](https://github.com/KILGORETROUT111)  
Email: [Provided in CV or repo issues]

---

## 🧭 Next Milestones (v1.2+)

- [ ] Axiomatic logic scaffolds (∀ introduction/elimination, → intro, ¬ intro)
- [ ] REST/CLI module cleanup & pipeline packaging
- [ ] Graph export (DOT/PNG) of inference chains
- [ ] SAT-logic integration layer (optional)

---

### 🧠 “LEE is not a black box. It’s the proof inside it.”

## ⚡ Example CLI Run

```bash
python -m evaluation.cli \
  --goal "Q(a)" \
  --facts "P(a)" \
  --axioms "¬P(x) ∨ Q(x)" \
  --export-json output/proof_Qa.json \
  --export-md output/proof_Qa.md
```

---

## 🧪 Showcase Inference

**Legal-Medical Logic Exhibit**  
Real inference from regulation to diagnosis:
📄 [`Exhibit_A_Legal_Medical_Logic_Inference.md`](docs/high-ground-use-case-exhibits/Exhibit_A_Legal_Medical_Logic_Inference.md)

**Full Engine Design + Use Case**  
🧬 [`Medical Use Case – v1.1`](https://github.com/KILGORETROUT111/logic-evaluation-engine/wiki/Medical-Use-Case-%E2%80%93-v1.1-Diagnostic-Logic-Engine)

---

## 🛰️ Whitepaper Fragment

Read how phase-consistent rotation and covariant logic primitives power inference:
📘 [`docs/philosophy/LEE_WhitePaper_Fragment.md`](docs/philosophy/LEE_WhitePaper_Fragment.md)

---

## 🎯 Who LEE Is For

- **Diagnostic Engineers** – trace symptoms to diagnosis
- **Legal Logic Developers** – encode and prove consequence
- **Philosophers of Logic** – explore phase-rotation and symbolic unification
- **Angels & Acies** – you want explainable AI? It lives here.

---

## 🌀 What’s Next

- Inference chaining
- Proof dialect extensions
- REST + CLI symmetry
- Logic as geometry – `∠truth`

---

## 🌊 Ride it

LEE doesn’t simulate logic. It earns it.
When ambiguity crashes in — LEE rides the phase.

5c7371b (Release LEE v1.1 — Diagnostic Logic Engine, Proof Mode, CLI)
