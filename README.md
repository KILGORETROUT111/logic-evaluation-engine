
[![CI (v3.0)](https://github.com/KILGORETROUT111/logic-evaluation-engine/actions/workflows/ci.yml/badge.svg?branch=v3.0)](https://github.com/KILGORETROUT111/logic-evaluation-engine/actions/workflows/ci.yml)
![Python 3.10–3.13](https://img.shields.io/badge/python-3.10%E2%80%933.13-blue)

# Logic Evaluation Engine (LEE) — v3.0

## Inspiration
![Billy Joel – Live in Uniondale, December 29, 1982](docs/billy-joel-uniondale-1982.png)

**“Happy New Year Long Island. And don’t take any shit from anybody!”**  
— Billy Joel, [Live in Uniondale (December 29, 1982)](https://www.youtube.com/watch?v=wDEvqyiRpzE&t=5596s)

_This project, like Billy said, is about doing the work right — and not taking any crap from broken logic, bad data, or bloated design._

Basis5 rotational phase logic + NL → λ-calculus → evaluator handshake.  
Canonical phase path: **ALIVE → JAM → MEM** with Basis5 winding/witness recorded in traces.

## Quickstart
```bash
# from repo root
pip install -e .
lee "if A then B" -d legal --pretty

# LEE 3.0 — Basis5 Contract (Conservative Spec)

**One rule:** we only code what the math projects.  
Basis5 is the projector; the engine is the print. No heuristics, no ephemera.

This document is the ground truth for LEE 3.0. It spells out the **Basis5 phase geometry**, how the **pipeline** records and respects it, what the **provenance** looks like on disk, and the invariants we conserve (the “logical Bianchi identity” discovered inside Basis5, not borrowed from anywhere else).

---

## 1) Basis5 in one page

- **Discrete phases on an exact lattice (no trig, no floats):**
  - `ALIVE` → angle `0°`, vector `( +1, 0 )`
  - `JAM`   → angle `90°`, vector `(  0, +1 )`
  - `MEM`   → angle `180°`, vector `( -1, 0 )`

- **Rotations are quarter-turns** in the cyclic group **Z/4Z**.  
  The only deltas are `{0, 90, 180, 270}` degrees, computed exactly.

- **Vectors are not amplitudes.** They’re **integer unit vectors** on **ℤ²**; no Feynman-like semantics, no probabilities.

- **Witness/Detachment** are projected from syntax-level operators (material implication, local refutation) and encoded as **integer flags (0/1)**. No scores.

---

## 2) Surfaces we expose in code

File: `src/core/basis5.py` (conservative form)

- `project_phase(phase) -> PhasePoint`  
  Returns the exact integer angle and unit vector for a phase.

- `rotation_delta_deg(a, b) -> int`  
  Returns `{0,90,180,270}`; `360` is normalized to `0`.

- `transition_basis(a, b) -> dict`  
  Small tensor with:
  ```json
  {
    "before": {"phase":"ALIVE","angle_deg":0,"vec":{"x":1,"y":0}},
    "after":  {"phase":"JAM","angle_deg":90,"vec":{"x":0,"y":1}},
    "delta_deg": 90
  }
  ```

- `build_winding(phases: list[str]) -> dict`  
  Cumulative rotation over a run. Returns per-step deltas and a summary with a rational average vector:
  ```json
  {
    "summary": {
      "total_winding_deg": 180,
      "avg_vector": {"x":{"num":0,"den":3}, "y":{"num":1,"den":3}},
      "unique_phases": ["ALIVE","JAM","MEM"]
    }
  }
  ```

- `witness_basis(expr: str) -> dict[str,int]`  
  Integer flags projected from the expression:
  - Implication / Modus Ponens / Detachment shape (`"IMPLIES"` or `"->"`):  
    `{"jam":1,"detach":1,"mp":1}`
  - Local refutation (e.g., `p & ~p`):  
    `{"jam":1,"refute":1}`
  - Otherwise: `{"jam":0}`

These are **conservative projections**: the engine never fabricates behavior that the math didn’t project.

---

## 3) Engine contract

**Behavior unchanged; instrumentation added.**  
LEE still runs `ALIVE → JAM → MEM` for our test scenarios. We now **record** the Basis5 geometry for each hop and the Basis5 witness at detect time.

### Integration points (current v3.0)
- On each phase hop, the pipeline writes a provenance `transition` event with:
  ```json
  "details": { "basis5": transition_basis(before, after) }
  ```
- On detect, the pipeline adds to enrichment:
  ```json
  "basis5_witness": witness_basis(normalized_expr)
  ```

No branching decisions are made from Basis5 yet; this is **aligned instrumentation**. (A v3.x step can make Basis5 the **authoritative planner** for the phase trace—see roadmap.)

---

## 4) Provenance schema (what you’ll find on disk)

Per run we write:
- **Primary summary**: `data/logs/<name>_<ts>.json`
- **Provenance**: `data/logs/<name>_<ts>.prov.jsonl`
- **SVG stub**: `… .svg`
- **Timeline extracts**: `… .timeline.md`, `… .timeline.dot`

### Event kinds
- `start`: session, domain, expr
- `prenorm`: raw → normalized
- `enrich`: domain enrichment, now including `basis5_witness`
- `detect`: phase after detect (usually `JAM`) + enrichment
- `transition`: phase_before → phase_after + `details.basis5` tensor

**Example (snippets):**
```json
{"kind":"transition","phase_before":"ALIVE","phase_after":"JAM",
 "details":{"basis5":{"before":{"phase":"ALIVE","angle_deg":0,"vec":{"x":1,"y":0}},
                      "after":{"phase":"JAM","angle_deg":90,"vec":{"x":0,"y":1}},
                      "delta_deg":90}}}

{"kind":"detect","phase_after":"JAM",
 "details":{"enrichment":{"domain":"legal","pattern":"1 -> 0",
                          "tags":["implication","boolean"],
                          "basis5_witness":{"jam":1,"detach":1,"mp":1}}}}
```

---

## 5) Invariants (logical “Bianchi-like” conservation)

These are **properties Basis5 guarantees** and that the engine should never violate:

1. **Discrete rotation conservation**  
   Over a closed loop, the **winding sum** is a multiple of `360°`.  
   Over a simple ALIVE→JAM→MEM trace, the total is `180°`, matching the intended closure to memory.

2. **Detachment preservation**  
   If the witness flags imply a detachment/MP structure (`1 -> 0`), the MEM closure **does not erase** that fact; it is recorded in enrichment and can be audited post-hoc.

A small optional checker (`scripts/basis5_project.py` + a future `src/core/basis5_invariants.py`) can assert these in CI without touching run-time flow.

---

## 6) Running it

### Install & test
```powershell
# Windows PowerShell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .            # editable install
pip install -r requirements-dev.txt  # if present
pytest -q                   # should be green
```

### One-shot evaluation (Python REPL)
```python
from src.engine import Pipeline
p = Pipeline(log_name="quick", domain="legal", enable_provenance=True, session="demo")
res = p.run("1 -> 0")
print(res["state"]["phase"])          # MEM
print(res["log_json"])                # data\logs\quick_<ts>.json
```

### Check the geometry in provenance
```python
import json, pathlib
log = pathlib.Path(res["log_json"])
prov = [json.loads(l) for l in log.with_suffix(".prov.jsonl").read_text(encoding="utf-8").splitlines()]
last_transition = [e for e in prov if e["kind"]=="transition"][-1]
print(last_transition["details"]["basis5"]["delta_deg"])  # e.g., 90
```

### Build a winding summary for the latest run
```powershell
python .\scripts\basis5_project.py
# -> writes data\logs\<name>_<ts>.basis5.json
```

### Batch runner (examples file)
```powershell
# from repo root
python .\scripts\run_batch.py --file .\scripts\inputs.txt --domain legal --log-prefix smoke
# -> data\logs\smoke_<ts>.csv with phases & timings
```

---

## 7) File layout (relevant bits)

```
src/
  core/
    basis5.py                # exact integer geometry and witnesses
  engine/
    pipeline.py              # emits transitions + witnesses to provenance
    provenance.py            # JSONL writer + timeline renders
data/
  logs/                      # run artifacts (*.json, *.prov.jsonl, *.svg, *.timeline.*)
  memdb/                     # phase-12 history/summary outputs (patient/case)
scripts/
  basis5_project.py          # builds winding (basis5) JSON from the latest run
  run_once.py                # one expression → one run
  run_batch.py               # many expressions → csv
```

---

## 8) What’s guaranteed right now

- Phases for our scenarios: **ALIVE → JAM → MEM**.  
- **No probabilistic math.** Geometry is exact and discrete.
- Provenance logs include **Basis5 transition tensors** and **Basis5 witness**.
- The existing test suite is **green**.

---

## 9) Roadmap (short)

- **Promote Basis5 to the authoritative planner** (phase plan and tags generated only from Basis5; the pipeline merely executes and records).
- **Invariants checker** (opt-in CI gate; alarms on any conservation breach).
- **Viz**: simple MkDocs page that graphs `*.basis5.json` for each run (no 3D, just cardinal rotations and winding).

---

## 10) Philosophy

LEE is **conservative**: the engine does not “invent.”  
**Basis5 projects → Engine records and executes.**  
The conserved transforms observed (“logical Bianchi identity”) are **emergent from Basis5** and remain conserved by construction.

If a code path can’t be derived from Basis5, it doesn’t ship.

---

**Appendix: Quick mental model**

- Think of phases as **cardinal directions** on a square compass.  
- An evaluation rotates that compass by exact quarter-turns as it moves from `ALIVE` (open) through `JAM` (tension) to `MEM` (closure).  
- Implications and refutations **mark** the presence of those rotations; they don’t “weigh” them.  
- The provenance is the scope note: which turn, when, and why — in integers, not vibes.

That’s LEE 3.0. Conservative, geometric, exact.
459e10ec47c76601a5a978852ca97da9f7e02f6e
