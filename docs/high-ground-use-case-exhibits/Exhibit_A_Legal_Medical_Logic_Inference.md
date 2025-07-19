# Exhibit A: Legal Logic Meets Medical Inference

## Objective

To demonstrate the real-world applicability of LEE's symbolic engine using a combined **legal-medical inference scenario**.  
This example draws from counterfactuals, scoped quantifiers, and logical resolution of consequence using axioms and patient data.

---

## Scenario: Presumptive Diagnosis under Legal Framework

> **Legal Clause**:  
> "If a patient presents with Symptom X and does not test negative for Condition Y, it shall be presumed that Condition Y is present."

This clause has the structure of a **counterfactual entailment** with legal force. We'll represent this as an axiom.

> **Medical Data**:  
> A patient exhibits **Symptom X**. No test for **Condition Y** has returned negative.

---

## Symbolic Encoding

### Known Facts:
- `SymptomX(patient1)`
- `¬NegativeTestY(patient1)`

### Axiom (Legal Logic as Conditional Inference):
- `∀x. (SymptomX(x) ∧ ¬NegativeTestY(x)) → ConditionY(x)`

---

## Goal:
- Prove: `ConditionY(patient1)`

---

## CLI Invocation

```bash
python -m evaluation.cli `
  --goal "ConditionY(patient1)" `
  --facts "SymptomX(patient1),¬NegativeTestY(patient1)" `
  --axioms "∀x. (SymptomX(x) ∧ ¬NegativeTestY(x)) → ConditionY(x)" `
  --export-json "proof_conditionY.json" `
  --export-md "proof_conditionY.md"
```

---

## Sample Output (Markdown Trace)

```markdown
Proof result: True
Trace:
- Given facts: SymptomX(patient1), ¬NegativeTestY(patient1)
- Axiom A1: ∀x. (SymptomX(x) ∧ ¬NegativeTestY(x)) → ConditionY(x)
- Substitution: {'x': 'patient1'}
- Instantiated: (SymptomX(patient1) ∧ ¬NegativeTestY(patient1)) → ConditionY(patient1)
- Evaluation: Premise is true; consequence derived
→ Derived ConditionY(patient1) via legal-medical axiom
```

---

## Commentary

This example shows how **LEE** can:
- Handle medical rules with embedded legal logic
- Evaluate scoped inference over patient-specific data
- Export traceable proof logs suitable for regulatory or diagnostic review

LEE demonstrates **transparent, symbolic reasoning** from codified policy to actionable medical consequence.


---

## 🔗 Proof Tether: Real Engine Implementation

This symbolic example isn't hypothetical — it's anchored in LEE's actual diagnostic logic engine.

🧠 See implementation details, engine design, and real use-case logic at:  
👉 [Medical Use Case – v1.1 Diagnostic Logic Engine (GitHub Wiki)](https://github.com/KILGORETROUT111/logic-evaluation-engine/wiki/Medical-Use-Case-%E2%80%93-v1.1-Diagnostic-Logic-Engine)

This proves the legal-medical inference logic showcased here is fully reproducible using the LEE runtime.
