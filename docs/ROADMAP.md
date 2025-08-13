# Logic Evaluation Engine (LEE) 3.0 — Basis5 Roadmap + Docs Routine

> LEE **is** the phase geometry. All engine behavior is projected from **Basis5** (ALIVE → JAM → MEM), material implication, and the witness algebra.  
> **If Basis5 can’t project it, we don’t code it.** This file captures scope, contracts, tests, and the full MkDocs + Mike versioned-docs routine.

---

## TL;DR (What’s true after this doc lands)

- Single source of truth for geometry: `src/core/basis5.py`.
- Engine writes Basis5 geometry into **JSON results**, **provenance lines**, and **memdb history**.
- Existing suite remains green (24/24) and **new Basis5 tests** pass.
- Versioned docs published at `https://kilgoretrout111.github.io/logic-evaluation-engine/<version>/` via **MkDocs + Mike**.

---

## Principles (Non-Negotiable)

- **Single source of truth:** Only `src/core/basis5.py` may export geometry helpers.
- **Conservative design:** No features beyond Basis5 projection.
- **Invariants:** Sum of step rotations ≡ total winding (mod 360). Witness integers drive JAM/MEM dynamics.
- **Artifacts:** Every run includes Basis5 fields in JSON, provenance, and memdb.

---

## Repository Map (key surfaces)

```
src/
  core/
    basis5.py            # ← Basis5 geometry & witness (single source of truth)
  engine/
    pipeline.py          # ← phase transitions; result assembly; calls Basis5
    provenance.py        # ← recorder events; include Basis5 in transitions/detect
    ...                  # other engine modules
docs/
  index.md               # landing page
  getting-started.md     # quickstart
  phase-geometry.md      # Basis5 spec (phases, winding, witness, invariants)
  api.md                 # public APIs that matter
  adapter-hooks.md       # legal/medical shims and hook contracts
  contributing.md        # dev workflow, tests, style
.github/workflows/
  ci.yaml                # tests + mkdocs build check
```

> One `.md` per indexed item. Keep pages focused and short.

---

## Basis5 Contracts (APIs **everyone** must use)

**Module:** `src/core/basis5.py`

```python
def project_phase(phase: str) -> dict: ...
def rotation_delta_deg(a: str, b: str) -> int: ...
def transition_basis(a: str, b: str) -> dict: ...
def build_winding(phases: list[str]) -> dict: ...  # {steps, total_deg, phases}
def witness_basis(pattern: str) -> dict: ...       # {implication, contradiction, detachment, ...}
```

**Engine integration (additive, non-breaking)**

```python
# pipeline.py — when transitioning phases:
basis5_t = transition_basis(phase_before, phase_after)
recorder.transition(phase_before, phase_after, details={"basis5": basis5_t})
history["phases"].append(phase_after)

# before returning:
result["basis5"] = {
  "phases": history["phases"],
  "winding": build_winding(history["phases"]),
  "witness": witness_basis(pattern),   # normalized form, e.g. "1 -> 0"
}
```

```python
# provenance.py — on detect/enrichment:
enrichment = {
  "domain": self.domain,
  "pattern": pattern,            # normalized canonical form
  "score": 0.5,
  "tags": ["implication","boolean"],
  "basis5_witness": witness_basis(pattern),
}
```

**MemDB history lines include:**

```jsonc
{
  "run_id": "...",
  "final_phase": "MEM",
  "basis5": { "total_deg": 180, "phases": ["ALIVE", "JAM", "MEM"] }
}
```

---

## Tests to Add (keep legacy tests untouched)

- `tests/engine/test_basis5_geometry.py`
  - JAM sample (`1 -> 0`): phases contain `ALIVE→JAM→MEM` (head or tail); `witness.implication == 1`.
  - Invariant: `sum(Δθ) % 360 == winding.total_deg`.
- `tests/engine/test_provenance_basis5.py`
  - Every `transition` line has `details.basis5.delta_deg`.
  - `detect.details.enrichment.basis5_witness` present.
- `tests/engine/test_memdb_basis5.py`
  - Patient/case last history line has `final_phase`, `basis5.total_deg`, `basis5.phases`.

> All tests **read** Basis5 from engine outputs; none recompute geometry elsewhere.

---

## 9-Day Milestone Plan (Scope + Man-Hours)

> Total ~5–6 focused days of coding spread over 9 calendar days.

### Day 1 — Phase 7 Kickoff (≈ 0.5–1d)
- Memory store finalization; event logging (phase transitions, contradictions).

### Day 2 — Evaluator Integration (≈ 0.5–1d)
- Link memory store + tensor archive → evaluator; ensure phase loops (no deadlocks).

### Day 3 — Logic Hooks (≈ 0.5d)
- Math/NLP/sim hooks; safe state mutation without forcing JAM.

### Day 4 — Vertical Demos (≈ 0.5d)
- Legal + Medical reproducible demos; SVG traces.

### Day 5 — NLP Vertical + Traces (≈ 0.5–1d)
- Parser → λ-logic → evaluator handshake; keep NLP tests green.

### Day 6 — CLI (≈ 0.5d)
- `lee run ...` smoke CLI; `--trace`, `--export` flags.

### Day 7 — Packaging (≈ 0.5d)
- README sections, notebook walkthrough, CI config, Dockerfile.

### Day 8 — Stress (≈ 0.5–1d)
- Full-suite runs on clean env; performance checks; loop edges.

### Day 9 — Delivery Pack (≈ 0.5d)
- One-take demos; zip pack; publish `v3.0-demo` branch.

---

## Local Dev (Windows PowerShell quickstart)

```powershell
# From repo root
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
pip install -r requirements-dev.txt  # if present

pytest -q     # expect 24/24 green
```

Scripts you already have:

```powershell
python scripts\run_once.py  --expr "1 -> 0" --domain legal --log quick
python scripts\run_batch.py --file scripts\inputs.txt --domain legal --log-prefix smoke
python scripts\print_last_run.py
python scripts\print_timeline_md.py
```

---

## MkDocs + Mike — Versioned Documentation Routine

We publish docs to `gh-pages` using **Mike** (versioned), surfaced at:
`https://kilgoretrout111.github.io/logic-evaluation-engine/<version>/`

### 0) One-time install

```powershell
.\.venv\Scripts\Activate.ps1
pip install mkdocs mkdocs-material mike ghp-import
```

Make sure you have `mkdocs.yml` at repo root (you do), and pages in `docs/`.

### 1) Local preview

```powershell
mkdocs serve -a 127.0.0.1:8000
# open http://127.0.0.1:8000/
```

### 2) First-time gh-pages initialization (safe path)

If you’ve never pushed docs before **or** you see “unrelated histories” errors:

```powershell
# Ensure remote tracking is fresh
git fetch origin

# Initialize gh-pages if missing or broken (empty tree is fine)
git checkout --orphan gh-pages
git reset --hard
git commit --allow-empty -m "init gh-pages"
git push -u origin gh-pages

# Return to your work branch
git switch v3.0
```

> If `gh-pages` exists but is incompatible, back it up then recreate:
```powershell
git fetch origin
git checkout gh-pages
git branch backup/gh-pages-<YYYYMMDD-HHMM>
git push origin backup/gh-pages-<YYYYMMDD-HHMM>
git switch v3.0
git push origin --delete gh-pages
# Now re-run the init above
```

(Alternative: use Mike with `--ignore-remote-status` if you’re sure; the recreate path above is cleaner.)

### 3) Deploy version **3.0** and set default

```powershell
# From your source branch (v3.0)
mike deploy --push 3.0
mike set-default --push 3.0

# Optional alias "latest"
mike deploy --push --update-aliases 3.0 latest
mike set-default --push latest
```

You should now see:
- Latest: `https://kilgoretrout111.github.io/logic-evaluation-engine/latest/`
- v3.0:   `https://kilgoretrout111.github.io/logic-evaluation-engine/3.0/`

### 4) Update docs after edits

```powershell
# Edit docs/*.md or mkdocs.yml
mkdocs build   # sanity check locally

# Publish to the same version
mike deploy --push --update-aliases 3.0 latest
mike list      # see what’s published
```

### 5) GitHub Pages setting (repo → Settings → Pages)

- **Source:** `Deploy from a branch`  
- **Branch:** `gh-pages` (root)

> Once set, Pages should update on each Mike deploy.

### Troubleshooting

- **“gh-pages is unrelated to origin/gh-pages”**  
  Use the backup+recreate flow above, then deploy again.  
  As a last resort: `mike deploy --push --ignore-remote-status 3.0` then `mike set-default --push latest`.

- **“GET /versions.json 404” locally**  
  That’s expected for local serve; Mike writes versions.json on deploy to `gh-pages`.

---

## CI (already present)

`.github/workflows/ci.yaml` runs:
- Python 3.12/3.13 test matrix: `pytest -q`
- MkDocs **build** (sanity).  
Publishing still happens explicitly with `mike` commands above.

---

## Definition of Done (Go/No-Go)

- [ ] Existing tests green (24/24).  
- [ ] Basis5 tests green (geometry, provenance, memdb).  
- [ ] JSON result includes `basis5.{phases,winding,witness}`.  
- [ ] Provenance transitions carry `details.basis5.*`; detect carries `basis5_witness`.  
- [ ] Patient/case lines include Basis5 totals.  
- [ ] Docs published to `gh-pages` for `3.0` and `latest`.

---

## Handover Notes (fill at each handoff)

- **Branch:** v3.0  
- **Commit:** `<hash>`  
- **Tests:** legacy 24/24; Basis5 X/Y  
- **Pages:** latest ✅  3.0 ✅  
- **Next action:** `<owner → task → date>`  
- **Known gaps:** `<short list>`

---

### Credits
- Basis5 inference and phase geometry by design. LEE simply projects it—no more, no less.
