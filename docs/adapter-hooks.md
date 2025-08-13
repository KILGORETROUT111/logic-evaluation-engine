# Adapter Hooks (Legal / Medical)

**Goal:** keep domain logic thin and explicit. Adapters may enrich signals, but the **Basis5 geometry remains the source of phase dynamics**.

## Locations

```
src/engine/adapters/
  base.py      # shared types/helpers (already present)
  legal.py     # thin legal shim
  medical.py   # thin medical shim
```

## Interfaces

Each adapter can expose some/all of the following optional callables. The pipeline probes them with `raising=False` and proceeds if missing.

```python
# legal.py
def cf_analyze(expr: str) -> dict | None:
    """Optional. Counterfactual analysis (used as an enrichment field)."""

# medical.py
def dm_classify(expr: str) -> str | None:
    """Optional. Divergence/clinical risk classification: e.g. 'low' | 'hi-risk'. """

def ner_extract(expr: str) -> list[dict] | None:
    """Optional. Simple NER results: [{"text": "1"}, ...]."""
```

## Example stubs (safe defaults)

```python
# src/engine/adapters/legal.py
def cf_analyze(expr: str):
    if "->" in expr or "IMPLIES" in expr:
        return {"counterfactual": True}
    return None
```

```python
# src/engine/adapters/medical.py
def dm_classify(expr: str):
    return "low"

def ner_extract(expr: str):
    return []
```

## How the pipeline uses them

- After prenorm and before detect, the pipeline builds `enrichment` and includes any adapter outputs under stable keys:
  - Legal: enrichment['counterfactual'] = {...} when present
  - Medical: enrichment['risk'] = 'low'|'hi-risk', enrichment['ner'] = [...]
- Additionally, enrichment carries basis5_witness projected from the normalized expression.

Resulting provenance detect event (excerpt):

```json
{
  "kind": "detect",
  "phase_after": "JAM",
  "details": {
    "enrichment": {
      "domain": "legal",
      "pattern": "1 -> 0",
      "tags": ["implication","boolean"],
      "basis5_witness": {"jam":1,"detach":1,"mp":1},
      "counterfactual": {"flag": "cf-ok"}
    }
  }
}
```

Adapters remain non-authoritative: they annotate, they do not steer phases.
