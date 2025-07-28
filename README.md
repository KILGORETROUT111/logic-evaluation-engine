### **Logic Evaluation Engine (LEE).**

### **Covariant Phase-State Dynamics for Symbolic Inference.**

LEE (Logic Evaluation Engine) is a logic-first inference engine designed to handle symbolic contradiction, diagnostic reasoning, and counterfactual inference under phase-consistent transformation rules. It treats symbolic logic as a conserved, covariant field and supports rotational logic state handling through custom primitives.

The **Logic Evaluation Engine (LEE)** is a symbolic reasoning engine built for phase-resolved inference, contradiction handling, and diagnostic logic across domains like **law**, **medicine**, and **autonomous systems**. It resolves symbolic contradictions not by discarding them, but by rotating their phase-state — traversing through **memory (mem)**, **testability (alive)**, **contradiction (jam)**, and **back to memory** — thereby preserving coherence in uncertain or incomplete environments.

LEE v1.2 is the first logic engine to introduce a rotational phase-state geometry for logical primitives. This allows for inference under misalignment — where memory, contradiction, or uncertainty are not obstacles, but coherent states in a structured dynamic. The model does not guess; it rotates. LEE’s architecture supports traceable evaluation, modal diagnostics, and counterfactual inference — and v1.2 introduces stable diagnostic pipelines that show phase resolution in action. This is not a claim of completeness. It is a quiet submission of structural novelty.

> *“LEE is not just logic. It is rotational inference under contradiction.”*

LEE creates a new frontier in formal logic computation:  

---

### 🌀 Key Capabilities

- Forked phase-state logic for contradictory or underdetermined inputs  
- Diagnostic engine with memory rotation and probe suggestion  
- CLI and REST API interfaces for embedding or operational testing  
- SVG / JSON / TXT outputs for analysis, audits, and traceability  
- Conjugate primitive architecture (mem > alive > jam > mem)  
- Tensor-style contradiction trace and semantic rotation  
- Medical and legal demos: LEE can both *diagnose* and *disqualify* by logic

  ---

  ## 🔁 Diagnostic Logic Engine: System Overview

### 1. Live Observation Stream

- Incoming symptom or event observations (e.g., `{"patient_id": "P003", "symptom": "fever", "phase": "initial"}`) are timestamped and assigned a confidence level.
- These are routed through a `symptom_feed.py` parser or CLI ingestion into the evaluation pipeline.

### 2. Memory Model

- Each patient has a unique record (`/jam_store/memdb/P003.json`), storing past observations in a chronological memory stack.
- Observations are written using `memory_push()` and retrieved with `memory_lookup()`.
- This enables stateful diagnostic evaluation — context-sensitive to prior events.

### 3. Evaluation Logic

- Core logic resides in `diagnostic_phase_engine.py` and its logic module.
- It resolves the new input against memory using symbolic reasoning.
- Outcomes:
  - `{"status": "resolved", "diagnosis": "Likely measles"}`
  - `{"status": "jammed", "trace": {"contradiction": True, "conflict": ("fever", "hypothermia")}}`

### 4. JAM Detection and Archive

- Contradictory logic states (e.g., hypothermia after fever in same phase vector) are JAMMED.
- JAMs are stored as JSON files with rich metadata in `/jam_store/jam_dump/`.
- Each JAM has a unique file ID (e.g., `JAM_P003_hypothermia_2025-07-28T16-32-01.840375.json`).
- Archive includes:
  ```json
  {
    "patient_id": "P003",
    "symptom": "hypothermia",
    "phase": "recall",
    "result": {
      "contradiction": true,
      "conflict": ["fever", "hypothermia"]
    },
    "timestamp": "2025-07-28T16:32:01.840375"
  }
  ```

### 5. SVG Rendering

- The JAM is visually rendered using `visualize_archive.py` and `render_patient_phase_flow.py`.
- Diagrams include directional arrows, color-coded regions (MEM → ALIVE → JAM), and patient flows.
- Phase lattices are saved as SVGs into `/evaluation/jam_store/svg_out/`.
- CLI-trigger or hybrid modes supported.

### 6. Upcoming: Timeline Replay + Re-evaluation

- We are now wiring the ability to:
  - Reconstruct a patient’s timeline from memory.
  - Replay it step-by-step into the diagnostic engine.
  - Trigger reevaluation for future hypothetical/retrospective analysis.

This capability will enable advanced use in medical, legal, and defense verticals.

---

## 🧭 LEE’s Position in the Landscape of Theoretical Logic and Physics

**LEE is not a critique. It is a constructive logic that makes collapse unnecessary.**

Where theoretical physicists and philosophers of logic have debated realism, observer dependence, and quantum collapse, LEE simply builds its own frame:

- No observer required.
- No stochastic collapse invoked.
- No untraceable inference.

Instead:
- Logical contradiction becomes a tensor field.
- Phase is operationally real, complex-valued, and spatially conserved.
- JAM → MEM → ALIVE replaces collapse with a dynamic resolution cycle.

LEE’s innovation is not just in the claim — it’s in the code.

> https://github.com/KILGORETROUT111/logic-evaluation-engine/wiki/7.1-Geometric-Inference-vs-Observational-Collapse

> “Where others debated realism, LEE builds it.”  — o---o


---

### 🔐 License & Disclosure

This software is released under the  
**Logic Evaluation Engine – Limited Demonstration and Diagnostic License (LEE-LDDL v1.0)**.

Logic Evaluation Engine (LEE) is a symbolic inference system for contradiction-aware reasoning under uncertainty. It rotates through logical phase states — memory, testability, contradiction, and resolution — to expose hidden inconsistencies and generate structured diagnostic traces.

See full text here:  

📜 [Zenodo DOI: 10.5281/zenodo.16410790](https://doi.org/10.5281/zenodo.16410790)  

🧠 [WAPIV TrustChain Community](https://zenodo.org/communities/wapiv/about)

📖 [Wiki Overview](https://github.com/KILGORETROUT111/logic-evaluation-engine/wiki)

🔧 [Try the REST API (locally)] (http://127.0.0.1:8000/docs)


> © 2025 William Alexander Patterson.  
> For **personal or academic non-commercial use** only.  
> Commercial use or redistribution requires written consent.  
> No rights transferred. All rights reserved.

---

### 📦 Included Demos

- `Exhibit C+` – Legal Clause Rotation under Contradiction  
- `Hemingway Fork` – Medical Inference with Confidence Probes  
- `lee_phasetensor_notebook.ipynb` – Tensor trace visualization  
- REST API endpoint via FastAPI: `/diagnose`

---

### 🚀 Quickstart

```bash
python -m evaluation.cli --goal "PenaltyApplies(x)" \
  --facts "ContractBreach(x)" "NoticeGiven(x)" "UnavoidableCircumstances(x)" \
  --axioms "(ContractBreach(x) ∧ ¬NoticeGiven(x)) → PenaltyApplies(x)" \
           "(NoticeGiven(x) ∧ MitigatingCircumstances(x)) → ¬PenaltyApplies(x)" \
           "UnavoidableCircumstances(x) → MitigatingCircumstances(x)"
```

---

### 🔖 Release Notes – v1.2

- Added dual-domain demos (legal and medical)  
- Phase Tensor Notebook and SVG tensor map  
- FastAPI endpoint `POST /diagnose` live for structured evaluation  
- Rotation history and contradiction trace logic extended  
- License now formalized and linked with Zenodo DOI  
- GitHub push validated, LEE now deployable across pipelines

---

> **The Dude Abides.**
