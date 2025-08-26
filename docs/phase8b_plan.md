# Phase 8b Plan — Minimal Proof-Theoretic Hooks (CF + Conjugate/Covariant), Non-Invasive

> Scope: add the smallest “proof-theoretic semantics” surface to LEE’s evaluator (without touching existing green tests), plus two acceptance tests that can be enabled/disabled via flags. Everything here is parser-agnostic and tuple-AST friendly.

---

## 0) Status & Safety

* **Non-invasive default:** all new behavior is **off** unless explicitly enabled.
* **Toggles (suggested):**

  * `cf.enable: bool = False` — enable counterfactual rules (Region-A, A→A).
  * `covariant.enable: bool = False` — enable conjugate transport checks/logging for MEM↔ALIVE.
* **Conservativity:** with both toggles `False`, the evaluator must behave exactly as Phase-8.

---

## 1) What counts as “in-core”

Formal criterion we’ll use going forward:

$$
X \in \text{core} \;\;\Longleftrightarrow\;\; \left(\frac{\partial\,\textsf{Eval}}{\partial X} \neq 0\right)\;\;\lor\;\;\bigl(X \text{ is necessary to prove } I_1\text{–}I_6 \text{ about }\textsf{Eval}\bigr)
$$

* “$\partial\textsf{Eval}/\partial X \neq 0$” = turning $X$ on/off changes observable eval behavior (phase history/events/outputs).
* $I_1$–$I_6$ are your Phase-8 invariants (monotonicity, determinism, archive completeness, etc.). If $X$ is required to prove any, then $X$ is in-core even if it has no visible effect in a given run.

---

## 2) Counterfactual (CF) Hooks — Minimal Operational Semantics

### 2.1 CF introduction/elimination (Region A only)

We introduce a neutral CF constructor and elimination pattern over tuple-AST:

* **Intro (A→A):**

  * From a factual or assumed antecedent $P$ in Region A, allow constructing a CF pair $(\text{CF}, P, Q)$ as a *hypothetical branch* tagged **Region A**.
* **Elim (A→A):**

  * If CF branch $(\text{CF}, P, Q)$ carries a witness that $P \vdash Q$ **within Region A**, we may discharge it to a factual commitment **only** if a promotion rule is enabled (by default, we **do not** promote; we merely log).

**Conservativity (default):** with `cf.enable=False`, CF nodes are treated as **opaque terms** (no rewriting). With `cf.enable=True`, they are **evaluated but not promoted** (A→A only). This guarantees no change to factual outcomes unless promotion is explicitly allowed later.

### 2.2 Evaluator skeleton (drop-in)

Add a private handler called from your dispatcher (names can track your codebase):

```python
# core/evaluation.py  (sketch)
def _handle_cf(expr, ctx, trace):
    """
    expr = ("CF", antecedent, consequent)
    Region-A only: explore the A-branch under antecedent; do not promote.
    """
    if not ctx.get("cf.enable", False):
        return expr, "ALIVE"  # opaque by default

    antecedent, consequent = expr[1], expr[2]

    # 1) Explore antecedent under Region A (constraint-only, JAM allowed)
    #    (reuse your existing stepping function with a region_a flag)
    a_out, a_phase = _eval_region_a(antecedent, ctx, trace)

    # 2) If antecedent yields JAM with a contradiction witness,
    #    the CF cannot be discharged; we keep it and log evidence.
    if a_phase == "JAM":
        trace.log("JAM", {"mode": "cf-antecedent-jam", "expr": expr})
        return expr, "MEM"  # archive CF intent, no promotion

    # 3) Explore consequent under the same A-branch *as hypothetical*
    q_out, q_phase = _eval_region_a(consequent, ctx, trace)

    # 4) Log the hypothetical entailment P ⊢ Q (A→A), but do not promote.
    trace.log("ALIVE", {
        "mode": "cf-a2a",
        "antecedent": a_out,
        "consequent": q_out,
        "note": "A→A hypothetical; promotion disabled"
    })
    return ("CF", a_out, q_out), "ALIVE"
```

> The only **required** addition for 8b is this guarded branch. It never promotes A→B by default, keeping LEE conservative.

---

## 3) Conjugate Quantities & Covariant Transport (MEM ↔ ALIVE)

### 3.1 Invariant (logging-first)

> **Invariant (Covariant recall):** Items persisted to MEM and later recalled to ALIVE must preserve their **logical form up to a covariant re-indexing** $R$:

$$
\mathrm{structure}(\text{ALIVE}_{\text{recalled}})\;=\;R\bigl(\mathrm{structure}(\text{MEM}_{\text{stored}})\bigr)
$$

For 8b we set $R$ to **identity**, i.e., byte-for-byte structure equality of the tuple-AST. Later you can generalize $R$.

### 3.2 Minimal implementation

* When you store to MEM (you already do on JAM→MEM), also log:

  * `mem.artifact_id`
  * `mem.payload_ast` (normalized)
* On MEM→ALIVE recall (your existing reactivation path), log:

  * `alive.recalled_ast`
  * `covariant.check = (alive.recalled_ast == mem.payload_ast)`
* If the check fails, emit a **JAM** with mode `"covariance-fail"` and archive the pair.

No behavioral change otherwise; this is **observability only** unless `covariant.enable=True` and `covariant.enforce=True`, which we *don’t* turn on in 8b.

---

## 4) Acceptance Tests (ready to drop later)

> These tests are **flag-aware**: they will **skip** if your evaluator lacks a `ctx` argument or if toggles cannot be set. Paste each block as a separate file under `tests/phase8b_prooftheory/`.

### 4.1 `test_cf_intro_elim.py`

```python
# tests/phase8b_prooftheory/test_cf_intro_elim.py
import inspect
import pytest

pytestmark = pytest.mark.phase8_core  # stays within Phase-8 scope by toggle

def _enable_cf(evaluate_full):
    import core.evaluation as E
    sig = inspect.signature(evaluate_full)
    if "ctx" in sig.parameters:
        return {"ctx": {"cf.enable": True}}
    # fallback: a module variable toggle if you support it
    try:
        setattr(E, "CF_ENABLE", True)
        return {"ctx": None}
    except Exception:
        pytest.skip("No way to enable CF in evaluator")

def test_cf_a_to_a_holds_without_promotion(evaluate_full):
    extras = _enable_cf(evaluate_full)

    # Build a simple CF: if P then Q, both Region-A hypotheticals.
    P = ("AND", ("VAR","x"), ("CONST", 1))   # benign antecedent
    Q = ("OR",  ("VAR","x"), ("CONST", 1))   # trivially follows under A
    expr = ("CF", P, Q)

    if extras["ctx"] is None:
        t = evaluate_full(expr)
    else:
        t = evaluate_full(expr, **extras)

    # No factual promotion by default; last phase should not be JAM for benign CF.
    phases = [ev.phase for ev in t.events]
    assert "JAM" not in phases, f"benign CF should not JAM; got phases={phases}"
    # Ensure the final expression still contains CF (no promotion A→B).
    assert hasattr(t, "result_expr"), "trace must expose result_expr"
    assert isinstance(t.result_expr, tuple) and t.result_expr[:1] == ("CF",)
```

### 4.2 `test_conjugate_covariance.py`

```python
# tests/phase8b_prooftheory/test_conjugate_covariance.py
import pytest

pytestmark = pytest.mark.phase8_core

def test_mem_alive_covariant_roundtrip(mod_archive, evaluate_full):
    """
    Store a contradiction to MEM, reactivate, and check identity transport.
    """
    reawaken = getattr(mod_archive, "reactivate", None)
    lookup   = getattr(mod_archive, "lookup_archive_record", None)
    if not callable(reawaken) or not callable(lookup):
        pytest.skip("archive API not present")

    expr = ("AND", ("VAR","x"), ("NOT", ("VAR","x")))
    t1 = evaluate_full(expr)

    jams = [ev for ev in t1.events if ev.phase == "JAM"]
    assert jams, "JAM must be logged for x & ~x"
    aid = getattr(jams[0], "archived_id", None)
    assert aid, "archived_id must be set"

    mem_rec = lookup(aid)
    assert mem_rec and "expr" in mem_rec.get("witness", {}), "must archive witness expr"

    # Reactivate (MEM -> ALIVE) with a trivial rules’ tweak
    t2 = reawaken(aid, rules_prime={"note": "identity-transport-check"})
    assert t2.events[0].phase == "ALIVE", "reactivation must wake to ALIVE"

    # Identity transport in 8b (R = id)
    alive_expr = getattr(t2, "result_expr", None)
    stored_expr = mem_rec["witness"]["expr"]
    assert alive_expr == stored_expr, f"Covariant transport failed: {alive_expr} != {stored_expr}"
```

---

## 5) Exit Criteria for Phase-8b

1. **Conservativity:** With both toggles `False`, all Phase-8 tests still green.
2. **CF A→A:** With `cf.enable=True`, benign CF terms neither JAM nor promote; traces show A→A logging.
3. **Covariance logging:** MEM payload equals recalled ALIVE payload (identity transport) and mismatch raises a JAM when `covariant.enforce=True` (optional in 8b).
4. **Docs:** One paragraph in `README.md` + one in the whitepaper appendix describing:

   * the toggles,
   * the A→A limitation,
   * the identity transport check.

---

## 6) Rollout plan (toggle-gated)

* **Step 1 (merge):** Land `_handle_cf` and MEM↔ALIVE logging with toggles **off**.
* **Step 2 (tests):** Add the two tests; mark them with `@pytest.mark.phase8_core`. They should **pass** when toggles are explicitly enabled inside the tests (and **skip** cleanly if not supported).
* **Step 3 (observability):** Keep covariant enforcement off; only log equality. Flip `covariant.enforce=True` later if you want JAM on mismatch.

---

## 7) Notes & Constraints

* **No parser dependency:** All examples use tuple-ASTs you already pass in tests, e.g. `("AND", A, B)`, `("NOT", A)`, `("CF", P, Q)`.
* **Promotion policy:** We intentionally **do not** implement A→B promotion in 8b; that would be a semantics change. When you want it, gate it behind `cf.promote=True` and draft a new acceptance test.
* **DTM integration (future):** DTM becomes “in-core” **iff** the evaluator consults it to bias/choose a legal transition. That is not part of 8b; log a single scalar `tau_at_transition` if you decide to compute it.

---

## 8) One-liner for the README

> **Phase-8b (optional):** Adds guarded counterfactual (CF) A→A evaluation and a MEM↔ALIVE covariant transport check (identity). Off by default; enabling either toggle does not change factual conclusions (no A→B promotion) and preserves Phase-8 invariants.

---
