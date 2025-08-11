# Phase Geometry

LEE models evaluation as a compact phase machine:

- **ALIVE** — active evaluation
- **JAM** — contradiction / blocking condition detected
- **MEM** — archived / conserved state
- **VAC** — quiescent (rare in the v3.0 pipeline)

## Allowed transitions (v3.0)

- `VAC → ALIVE`
- `ALIVE → { MEM, JAM, VAC }`
- `JAM → MEM`
- `MEM → ALIVE`

In practice for contradiction-like inputs we emit **ALIVE → JAM → MEM** in history, while the **final phase** remains **MEM**.

## Provenance events

Per run we record:
- **start** — domain/session context
- **prenorm** — input normalization (e.g., `IMPLIES → ->`)
- **enrich** — domain enrichment (adapters)
- **detect** — contradiction detection (`phase_after="JAM"`)

Artifacts live next to the JSON log:
- `*.prov.jsonl`, `*.timeline.md`, `*.timeline.dot`, `*.svg`
