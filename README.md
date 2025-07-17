# Logic Evaluation Engine (LEE) – v1.1

## 🧠 What Is the Logic Evaluation Engine?

LEE is a lightweight symbolic engine for logical reasoning across phase-variant, fork-sensitive domains. It tracks logical transformations as phase-consistent rotations—preserving structural coherence even in ambiguous or contradictory input states.

---

## 🚀 What It Does

- Resolves complex symbolic chains using Functor-based logic
- Handles partial, ambiguous, or contradictory propositions
- Supports traceable inference, substitution, and lambda-logic
- Diagnostic use-case: derives likely condition + probe recommendation
- Enables geometric phase-state mapping of logical behavior

---

## 🎯 Who It’s For

- Logicians, symbolic AI researchers
- Diagnostic system designers
- Developers of explainable reasoning engines
- Anyone building logic-based tools with causal, temporal, or incomplete data

---

## 🔧 Highlights of v1.1

- ✅ Diagnostic Phase Engine (CLI demo included)
- ✅ Phase-state geometric mapping across Region A / Region B
- ✅ Traceable inference logging per run
- ✅ JSON + .txt output formats for all diagnostic runs
- 🧪 Prebuilt test runners (text + structured)
- 🌀 Foundation for REST/CLI and proof-chain modules

---

## 🛠️ Getting Started

```bash
git clone https://github.com/KILGORETROUT111/logic-evaluation-engine.git
cd logic-evaluation-engine
python run_diagnostic.py --input "fever,cough"
```

---

## 📁 Directory Structure

```
logic-evaluation-engine/
├── run_diagnostic.py                # CLI interface for LEE
├── diagnostic_phase_engine.py       # Phase-state logic engine
├── test_diagnostic_runs.py          # Batch .txt output test runner
├── test_diagnostic_runs_json.py     # Batch .json output test runner
├── evaluation/                      # Core logic modules (Functors, etc.)
├── tests/                           # Internal validation
├── diagnostic_test_logs/            # Output from test scripts
└── README.md
```

---

## 🔗 Optional Applications in SAP Environments

LEE can be integrated into SAP landscapes (e.g., S/4HANA, BTP) for advanced diagnostics, pricing logic debugging, and AI/ML-enhanced configuration validation pipelines.  
Its symbolic trace and fork-resolution capabilities make it ideal for auditing complex flows like SD condition logic, SLT sync behavior, or multi-source platform integrations.

---

## 🗺️ Roadmap

- [ ] Quantifier logic + axiomatic proof support
- [ ] REST API + CLI shim interface
- [ ] Visualizer for phase-resolution and fork-logic
- [ ] Logic export to external systems or proof viewers
- [ ] Additional use cases: medical, legal, general logic assistants

---

## 🌀 Why Phase-State Logic Matters

LEE introduces **phase-state geometry** as a model of logical conservation. In this view:

- Logical relations are **covariant under rotation**
- Contradictory inputs are **not rejected**, but routed
- Geometric zones (Region A, Region B) define diagnostic or logical *flow*

The engine remains stable and coherent through contradiction, using internal trace semantics to resolve forks.

---
