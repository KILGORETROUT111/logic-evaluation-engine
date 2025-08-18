
# Basis5 Taxonomy of MathLog→Code Exhaustibility

This section formalizes three classes that separate *what LEE can build today* from *what LEE can only define*. The taxonomy is designed to align reviewers and engineers on **proof obligations** and **engineering expectations**.

## Class I — Exhaustible (Resource‑Constrained Implementable)
**Definition.** Algorithms and representations exist; implementation is blocked by practical resources (time, memory, parallelism, scale).  
**Theory analogue.** Decidable classes (e.g., P/NP/PSPACE) with high constants.  
**Proof obligations.**
- Complexity bounds (upper/lower) or approximation guarantees.
- Reductions to known tractable/intractable kernels.
- Engineering bill: required compute, accelerators (GPU/TPU/FPGA), time-to-solution.

**LEE examples.**
- Multi-object counterfactual runs that complete on HPC.
- StressIndex with full time-weighting over large case networks.

## Class II — Exhaustible (Translator/Technology‑Lagged Implementable)
**Definition.** Logically implementable, but there is no **media-translator** (language/architecture/semantics) yet to encode the construct. Feasible with new DSLs or hardware.  
**Theory analogue.** Constructive existence without a current Curry–Howard/operational mapping; unconventional computing.  
**Proof obligations.**
- Constructive semantics for a DSL or intermediate representation (IR).
- Compilation strategy to existing or proposed hardware.
- Soundness/completeness relative to the math object.

**LEE examples.**
- Phase‑geometry rotations that require a new “phase‑tensor” IR.
- Counterfactual branching with native provenance algebras.

## Class III — Non‑Exhaustible (Inherent Non‑Implementable)
**Definition.** Inherently non-implementable due to undecidability or non-constructive features; no faithful finite encoding.  
**Theory analogue.** Halting-like undecidability, diagonal arguments, no‑go theorems.  
**Proof obligations.**
- Reduction from a known undecidable problem or impossibility theorem.
- Explicit boundary statement: approximable shadows vs. full object.

**LEE examples.**
- Global closure properties whose computation entails unbounded logical completion.

---

## Decision Checklist (Fast Triage)

| Question | If **Yes** | Class |
|---|---|---|
| Do we have an algorithmic representation today? | but it blows up in cost | I |
| Can we define a constructive mapping with a new DSL/IR/hardware? | plausible & testable | II |
| Does the construct imply undecidability or non‑constructive dependence? | provable | III |

**Reviewer protocol.** Attempt Class I → if blocked by scale, try approximation. If representation is missing, draft a Class II translator sketch. If formal barriers appear, escalate to Class III and publish a boundary result.

---

## Integration Notes

- **Basis5LM (Lower Math):** Use the taxonomy as a user‑facing commitment device (what ships now vs. near‑term vs. theoretical boundary).  
- **Basis5HM (Higher Math):** Attach formal proofs for class placement; include reductions, semantics, and no‑go arguments.  
- **Provenance:** Record class assignment per experiment in `prov.jsonl` (`"exhaustibility_class": "I|II|III"`).
