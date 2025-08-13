# Contributing to LEE 3.0

Welcome—keep it lean, exact, and **projected from Basis5**. If the math doesn’t project it, we don’t code it.

---

## Repo setup

```powershell
git clone https://github.com/KILGORETROUT111/logic-evaluation-engine.git
cd logic-evaluation-engine
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
pytest -q  # should be green
```

MkDocs/Mike (docs):

```powershell
pip install mkdocs mkdocs-material mike
mkdocs serve -a 127.0.0.1:8000
```

---

## Branches & releases

- **main**: frozen snapshot.
- **v3.0** (or next `v3.x`): active development.
- Prefer feature branches off v3.0: `feat/<slug>`, `fix/<slug>`; PR back into v3.0.

Tagging docs with Mike (example after merge):
```powershell
mike deploy 3.0
mike set-default 3.0
```

---

## Tests (must pass)

Run everything:
```powershell
pytest -q
```

Targeted:
```powershell
pytest -q tests/engine/test_phase13_adapters.py -q
pytest -q tests/core/test_contradiction.py -q
```

Smoke with scripts:
```powershell
python .\scriptsun_once.py --expr "1 -> 0" --domain legal --log quick
python .\scriptsun_batch.py --file .\scripts\inputs.txt --domain legal --log-prefix smoke
```

**Do not** add probabilistic checks. Everything is deterministic, integer-based.

---

## Basis5 contract (contributor rules)

- Phases are **ALIVE → JAM → MEM** on the discrete circle (0°, 90°, 180°).
- Rotations are multiples of 90°. Composition is modular.
- Witness flags are integers `{0,1}` from syntax; not scores.
- New behavior must be **derived from Basis5** and recorded in provenance:
  - Add **transition** events with `details.basis5` (tensor).
  - Add **detect/enrich** with `basis5_witness` when applicable.

If you can’t express it as a Basis5 rotation/witness, it’s outside scope.

---

## Adapters (legal/medical)

Adapters live in `src/engine/adapters/`. They **annotate** only:
- `legal.cf_analyze(expr) -> dict|None`
- `medical.dm_classify(expr) -> str|None`
- `medical.ner_extract(expr) -> list[dict]|None`

Pipeline merges adapter output into `enrichment` but **does not** let adapters change phases.

---

## Coding style

- Small, explicit modules. No magic.
- Keep public surface minimal; prefer internal helpers.
- Stick to standard library unless there is a *Basis5-projected* need.
- Type hints on new/changed code.
- Logging/provenance: never omit—emit structured events.

Commit messages: conventional-ish
```
feat: basis5 witness for refutation
fix: ensure MEM recorded in patient summary
docs: add adapter-hooks page
ci: add 3.13 job
```

---

## CI expectations

- Linting kept light; tests are the contract.
- Workflows live in `.github/workflows/`. CI runs tests (3.12/3.13) and builds docs.
- Red CI = no merge.

---

## Docs

Single-file pages per topic in `docs/`:
- `index.md` – concise overview
- `phase-geometry.md` – Basis5 geometry
- `adapter-hooks.md` – domain shims
- `api.md` – public surface
- `contributing.md` – this page

Add to `mkdocs.yaml` `nav` as needed. Keep each page focused.

---

## Artifacts & data

- Runtime outputs in `data/logs/` and `data/memdb/`. These are ignored by Git.
- Do not commit large binaries. If needed, link externally and document reproducibility.

---

## Security & disclosure

No network calls from the engine. If you find a security issue, open a private channel (GitHub Security Advisories) or email the maintainer.

---

## PR checklist

- [ ] Tests pass locally (`pytest -q`)
- [ ] Provenance includes Basis5 transitions/enrichment where relevant
- [ ] Docs updated (if API/behavior surfaces)
- [ ] No stray artifacts (`data/logs/*`, `*.pyc`, `__pycache__`)
- [ ] Commit message captures intent

---

## Quick FAQ

**Q: Can adapters flip phases?**  
A: No. They annotate, the engine’s Basis5 geometry governs phases.

**Q: Why no probabilities?**  
A: The math is discrete. Witnesses are integer flags—auditable and stable.

**Q: Where to add a new domain?**  
A: Create a thin adapter in `src/engine/adapters/<domain>.py` and write tests that verify enrichment; phases remain Basis5-driven.

Thanks for keeping it crisp.
