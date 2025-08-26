# Tiny README snippet — “Tensor Semantics in LEE”

```md
## Tensor Semantics in LEE (Phase-8b)

LEE’s phase manifold is taken (for core purposes) as a 2-D torus \(M \cong \mathbb{T}^2\).  
We expose **tensor *types*** (not numeric components) to keep the core evaluator geometrically disciplined.

**Field types (meta):**
- `EntropyLoad` (EL): scalar \((0,0)\)
- `PhaseFlow`: vector \((1,0)\)
- `DTM_dir`: covector \((0,1)\)
- `J_contra`: contradiction flux, 2-form \((0,2)\), antisymmetric
- `Stress2Form`: stress diagnostic, 2-form \((0,2)\), antisymmetric

**Invariants (meta-level):**
1. **Type stability under reparametrization**: coordinate changes (e.g., \(\phi \mapsto \phi+\alpha\)) preserve variance \((p,q)\), symmetry, and dimension exponent.
2. **Wedge discipline**: \( (0,1)\wedge(0,1) \to (0,2) \) with antisymmetry.
3. **Dimension bookkeeping**: exponents add under tensor product; core fields use exponent \(0\). (Nonzero exponents are reserved for verticals.)

**DTM policy (core vs vertical):**
`DTM_dir` remains *out of core* unless the evaluator **actually consults it to decide/modify** a legal phase transition (e.g., to damp a high-torsion JAM→MEM). If consulted, DTM becomes “is-in (core)” per the Phase-8b rule.

See `src/core/tensor.py` and `tests/phase8b_tensor_semantics.py`.
```

---

# Full project doc — `docs/tensor_semantics.md`

````md
# Tensor Semantics in LEE (Phase-8b)

**Scope.** This document specifies the meta-level tensor discipline used by LEE’s core evaluator. We model *types* (rank/variance, symmetry, dimension exponents) on the phase manifold \(M \cong \mathbb{T}^2\). Numeric components, metrics, and Hodge duals are deferred to verticals.

---

## Files

- `src/core/tensor.py` — minimal API for tensor *metadata*:
  - `FieldMeta`: `(name, variance=(p,q), symmetry, dimension_exp, chart)`
  - helpers: `tensor_product_meta`, `wedge_meta`, `grad_meta`, `div_meta`,
    `reparam_phi_shift_meta`
  - conveniences: `EL_meta`, `phase_flow_meta`, `DTM_dir_meta`,
    `contradiction_flux_meta`, `stress_2form_meta`
- `tests/phase8b_tensor_semantics.py` — acceptance tests (A–F)

---

## Design goals

1. **Geometric discipline for the core.** Keep the evaluator honest about what objects it produces/consumes across phase transitions.
2. **Separation of concerns.** Core uses only *dimensionless* types (exponent \(0\)); verticals (physics/biomed) may introduce nonzero exponents.
3. **Future-proofing.** The API anticipates adding numeric components, connections, and integrals without breaking core contracts.

---

## Core types

| Name                  | Variance | Symmetry  | Dim. exp. | Meaning                                    |
|-----------------------|----------|-----------|-----------:|--------------------------------------------|
| `EntropyLoad` (EL)    | (0,0)    | none      |        0.0 | scalar load functional on \(M\)            |
| `PhaseFlow`           | (1,0)    | none      |        0.0 | vector field for phase transport           |
| `DTM_dir`             | (0,1)    | none      |        0.0 | diagnostic torsion direction (1-form)      |
| `J_contra`            | (0,2)    | antisym   |        0.0 | contradiction flux 2-form                  |
| `Stress2Form`         | (0,2)    | antisym   |        0.0 | stress diagnostic 2-form                   |

> **Note (DTM policy).** `DTM_dir` is *not* “is-in (core)” unless the evaluator actually consults it to choose/modify a legal phase transition. Once consulted, it becomes core per the formal rule:
>
> \[
> X \in \text{core} \;\;\Longleftrightarrow\;\; \frac{\partial\,\textsf{Eval}}{\partial X}\neq 0 \;\;\lor\;\; X\text{ is needed to prove } I_1\text{–}I_6 \text{ about }\textsf{Eval}.
> \]

---

## API sketch

```python
@dataclass(frozen=True)
class FieldMeta:
    name: str                   # label for diagnostics
    variance: tuple[int,int]    # (p,q) = (# contravariant, # covariant)
    symmetry: "none|sym|antisym"
    dimension_exp: float        # exponent under L -> λL scaling
    chart: str = "theta,phi"    # coordinate tag (purely informational)

# Type algebra
tensor_product_meta(a, b) -> FieldMeta          # (p,q) add; exponents add
wedge_meta(a, b) -> FieldMeta                   # (0,1) ^ (0,1) -> (0,2) antisym

# Flat T^2 differential *meta* (types only)
grad_meta(scalar) -> (0,1)
div_meta(vector)  -> (0,0)

# Coordinate reparametrization invariance (meta-level type preservation)
reparam_phi_shift_meta(meta, shift) -> meta
````

---

## Acceptance tests (A–F)

* **A. Type/dimension algebra.** `grad(EL):(0,1)`, `div(PhaseFlow):(0,0)`, product adds variances and exponents.
* **B. Wedge discipline.** `(0,1) ∧ (0,1) → (0,2)` with antisymmetry.
* **C. Coordinate covariance (meta).** Reparametrization preserves variance, symmetry, exponent.
* **D. Syntactic gauge (α-rename) placeholder.** Meta unaffected by naming.
* **E. Integral well-posedness (meta).** Only 2-forms are integrable over area (e.g., `J_contra`, `Stress2Form`).
* **F. Unit rescale sanity.** Core fields use exponent 0; verticals may set nonzero.

---

## Worked mini-examples

### 1) Contradiction flux as a 2-form

To integrate a contradiction flux over a patch $U \subset M$, its *type* must be $(0,2)$ antisymmetric:

```python
J = contradiction_flux_meta()      # (0,2), antisym
assert J.is_2form()
# Later vertical can attach numeric components and compute ∫_U J.
```

### 2) DTM-gated phase damping (conditional core)

If the evaluator uses `DTM_dir` to damp a high-torsion JAM→MEM step (e.g., threshold on a torsion score), then $ \partial \textsf{Eval}/\partial \text{DTM\_dir}\neq 0$ and DTM becomes “is-in (core)” per Phase-8b.

---

## Running the tests

**Windows (PowerShell):**

```powershell
cd C:\Users\Dell\Documents\logic-evaluation-engine-3.0
$env:PYTHONPATH = "$pwd\src"
pytest -q -rA tests\phase8b_tensor_semantics.py
```

**Unix-like:**

```bash
cd logic-evaluation-engine-3.0
PYTHONPATH=src pytest -q -rA tests/phase8b_tensor_semantics.py
```

Tests will `skip` cleanly if `core/tensor.py` is missing.

---

## Roadmap (post-8b)

* Attach numeric components and simple pullbacks on $\mathbb{T}^2$.
* Optional metric $g$ and Hodge star $\star$ for 1-forms/2-forms.
* Basic Stokes checks for the JAM archive boundary (line integral vs flux).
* Bridge to analytics: log field *types* alongside event traces.

---

## Rationale

* Keeps the core evaluator’s reasoning **coordinate-honest** without dragging in heavy differential-geometric machinery.
* Clean boundary between **pedagogy/research** and **verticals**: academics can reason about types/invariants; engineering pipelines can later add units and numerics without weakening proofs or contracts.

```

Render a micro “API docstring audit” (*.md table generated from `tensor.py` annotations) so the code and this doc never drift.
::contentReference[oaicite:0]{index=0}
```
