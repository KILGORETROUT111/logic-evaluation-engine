# Logic Evaluation Engine (LEE) 3.0

**Basis5-driven phase dynamics** for contradiction analysis and evaluation.  
Discrete rotations (**ALIVE → JAM → MEM**) with integer witnesses and auditable provenance.

---

## What is LEE?

LEE is a lean engine that evaluates logical expressions and records a reproducible trail:
- **Phase geometry** on a discrete circle (0°, 90°, 180°).
- **Witness projection** (integers, not probabilities).
- **Deterministic provenance**: JSONL timeline, SVG graph, Markdown summary.
- **Adapters** (legal/medical) enrich signals without steering phases.

---

## Quick start

```powershell
git clone https://github.com/KILGORETROUT111/logic-evaluation-engine.git
cd logic-evaluation-engine
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
pytest -q        # expect green
```

Run a single expression:

```powershell
python .\scripts\run_once.py --expr "1 -> 0" --domain legal --log quick
```

Batch from a file:

```powershell
python .\scripts\run_batch.py --file .\scripts\inputs.txt --domain legal --log-prefix smoke
```

Artifacts land in `data/logs/` with `.json`, `.prov.jsonl`, `.svg`, `.timeline.md` files.

---

## Docs map

- **[Getting started](getting-started.md)**
- **[Phase geometry (Basis5)](phase-geometry.md)**
- **[Adapter hooks](adapter-hooks.md)**
- **[API](api.md)**
- **[Contributing](contributing.md)**

---

## Versioned docs (Mike)

```powershell
mike deploy 3.0
mike set-default latest
# local preview
mike serve -a 127.0.0.1:8000
```

---

## Philosophy

If the math doesn’t project it, we don’t code it.  
Basis5 is the source of truth; everything else annotates.
