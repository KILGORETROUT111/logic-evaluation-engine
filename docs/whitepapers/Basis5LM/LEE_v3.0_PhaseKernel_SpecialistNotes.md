
# LEE v3.0 — Phase Kernel Specialist Notes

## Axioms (Four-Phase Clock)
Let `ClockVal = {Alive, Jam, Mem, Vac}`. Reinterpret a 2-ary operator’s truth table as a **phase map** χ over rows:

- Row (1,1) → Alive  
- Row (1,0) → Jam  
- Row (0,1) → Mem  
- Row (0,0) → Vac

This is the **Occam-minimal** structure that distinguishes the unique obstruction row and preserves the remaining rows as coherently evaluable states.

## Obstruction Lemma (Sheaf Form)
Fix a small category of contexts `E` and the presheaf `C : E^op → Sets` with local values `{φ0,φ1,φ2,φ3}` mapping to `{Alive,Jam,Mem,Vac}`, and partial restriction `ρ(i) = i+1 (mod 4)` except `ρ(1)=⊥`.

**Lemma (Non-Gluability of Jam).** No global section of `C` contains Jam.  
**Intuition:** Jam blocks restriction; you can’t extend it along morphisms. This is exactly the operational meaning of “cannot proceed with evaluation”.

## Conservation / Representation Theorem (Class B)
Let `B = { O : {0,1}² → {0,1} | O(1,0)=0  and  O(0,q)=1 }`. (Material implication is canonical.)

**Theorem.** For every `O ∈ B` there exists a unique χₒ : `ClockVal → ClockVal` preserving the phase assignment above; conversely, any such χ reconstructs `O`.  
**Consequence:** Within `B`, the four-phase kernel is **representation-complete** for the operator’s structure: no extra logical machinery is needed beyond `{Alive,Jam,Mem,Vac}`.

---

## Witness Principle (What the Engine Proves)

### Definitions
- **Local Refutation Witness.** A pair of subterms `(X, ¬X)` under a conjunctive node exhibits immediate Jam.  
- **Implication Jam Witness.** A subterm `(p → q)` with `p ≡ 1` and `q ≡ 0` (the canonical jam row) exhibits Jam.

### Witness Theorem (Operational)
Given an AST `t`, `core.contradiction.analyze(t)` returns:
- `is_contradiction = True`,
- `mode ∈ {local-refutation, implication-jam}`,
- a **witness** `w` that is a compact serialization of the *exact substructure* causing Jam.

**Soundness (engine-level).** If `analyze(t)` returns a witness, then the pipeline must log Jam and either:
- stop, or
- archive and transition `Jam → Mem` (our Phase-7 behavior).

**Completeness (within B + refutation schema).** If `t` contains an instance of `(1→0)` or `X ∧ ¬X` in any representation covered by our AST adapters (tuple/dict/operator or the tokenized lambda-`Application` form), `analyze(t)` will produce a witness.

---

## From Math to Code: Contracts You Can Enforce

### Evaluator Contract
- On input AST/text, `evaluate_full` must:
  1. transition `MEM → ALIVE` (wake),  
  2. run contradiction detection,  
  3. if witness exists → transition `ALIVE → JAM` and emit `{mode, witness}` to the event log.

**Invariant I₁ (Phase Monotonicity).** In a single run: `ALIVE` precedes `JAM` precedes `MEM` if and only if a Jam witness exists.

### Pipeline Contract
- If `state.phase == JAM`:  
  a) persist `{mode, witness}`,  
  b) **optionally** call `divergence_map.resolve` and `tensor_archive.store` to produce an artifact id,  
  c) transition `JAM → MEM` and log.

**Invariant I₂ (Archive Completeness).** Every JAM event must have a corresponding archive record in memory/log including `{mode, witness.pattern}` and `{artifact_id}` if analytics are present.

### Parser Canonicalization Contract (Phase 8 task)
- A prepass maps tokenized `Application(Variable('1'), '-', '>', '0')` to a canonical `Imp(1,0)` node.  
- After canonicalization, `analyze(ast)` succeeds **without** string heuristics.

**Testable Claim C₁.** For all strings in the grammar of `->, &, ~`, canonicalization yields operator nodes recognized by `core.contradiction`.

---

## Why This Is Not “Just Another Logic Engine”

1. **Obstruction is structural, not exceptional.**
2. **Sheaf semantics ≠ slogan.**
3. **Occam-minimality is formal.**
4. **Witness makes it operational.**

---

## Phase 8: Proof Obligations

1. **Kernel Soundness (KS)**
2. **Class-B Completeness (BC)**
3. **Resolution Correctness (RC)**
4. **Deterministic Phase History (DPH)**

---

## Experiments the Skeptics Can’t Hand-Wave

- **E₁ (Witness/Log Linking)**
- **E₂ (Operator-Class Test)**
- **E₃ (Sheaf Obstruction Simulation)**
- **E₄ (Canon vs Fallback)**

---

## What to Ship in Phase 8

- Canonicalization pass
- Real archive bridge
- Tiny WHNF β-reducer + pre-normalization hook
- Log+SVG of `ALIVE → JAM(witness.pattern) → MEM(artifact_id)`

**Exit criteria:**
- 100% passing unit tests
- Fallback never used in canonicalized parse tests
- Archive true for any detected Jam
