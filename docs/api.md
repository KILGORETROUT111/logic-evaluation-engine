# API (Single-File Reference)

This page lists the small surface LEE exposes in v3.0.

---

## Engine

### `src.engine.Pipeline`

```python
Pipeline(
    log_name: str,
    domain: str,                         # 'legal' | 'medical' | ...
    enable_provenance: bool = True,
    session: str = "default",
    patient_id: str | None = None,
    case_id: str | None = None,
)
```

**Method**

```python
run(expr: str) -> dict
# -> {
#   "state": {"phase": "MEM"},
#   "history": {"phases": ["ALIVE","JAM","MEM"], "run_id": "..."},
#   "elapsed_ms": 0.0,
#   "log_json": "data/logs/<name>_<ts>.json",
#   "log_svg":  "data/logs/<name>_<ts>.svg"
# }
```

**Behavior**
- Emits provenance start → prenorm → enrich → detect → transition…
- Writes artifacts next to log_json: .prov.jsonl, .timeline.md, .svg.

---

## Basis5 (Geometry)

Module: `src.core.basis5`

```python
project_phase(phase: str) -> dict         # {'phase','angle_deg','vec':{'x','y'}}
rotation_delta_deg(a: str, b: str) -> int # 0|90|180|270
transition_basis(a: str, b: str) -> dict  # tensor for a→b
build_winding(phases: list[str]) -> dict  # cumulative rotation + summary
witness_basis(expr: str) -> dict          # integer flags
```

---

## Evaluator helpers

Module: `src.engine.evaluator` (kept minimal)

```python
evaluate_expression(text_or_ast, logger=None) -> dict
evaluate_full(text_or_ast, logger=None) -> dict
# Internally calls canonicalizer/parser as needed and logs JAM on contradictions.
```

---

## Scripts

From repo root:

```powershell
# One expression → run artifacts
python .\scripts\run_once.py --expr "1 -> 0" --domain legal --log quick

# Many expressions → CSV
python .\scripts\run_batch.py --file .\scripts\inputs.txt --domain legal --log-prefix smoke

# Build Basis5 winding for latest run
python .\scripts\basis5_project.py
```

CSV columns (batch): idx, expr, domain, phase, elapsed_ms, log_json

---

## Artifacts on disk

```
data/logs/<name>_<ts>.json
data/logs/<name>_<ts>.prov.jsonl
data/logs/<name>_<ts>.svg
data/logs/<name>_<ts>.timeline.md
```

Provenance events (JSONL): start, prenorm, enrich, detect, transition, …

---

## Stability

- All APIs here are conservative and already exercised by tests.
- New features must be projected from Basis5 before they appear here.
