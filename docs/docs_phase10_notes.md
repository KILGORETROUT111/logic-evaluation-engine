
# LEE v3.0 — Phase 10 Scaffold

## Goal
Make the engine **introspective and self-auditing** without breaking the green test suite.

## New modules
- `src/engine/provenance.py` — in-memory provenance recorder (attach later to Pipeline).
- `src/engine/audit.py` — convert EventLog JSON to JSONL / Markdown / Graphviz DOT.
- `src/engine/replay.py` — rebuild timeline (phases, last JAM witness) from EventLog JSON.

## Integration (optional, safe)
- Construct `ProvenanceRecorder(run_id)` inside `Pipeline.__init__` (behind a flag).
- At key points (parse, canon, reduce, detect, archive, transition), call `prov.record(...)`.
- On run end, dump `provenance.to_jsonl()` next to the EventLog files.

## Why this order
1) **No behavior change** — the scaffold is passive utilities.
2) **Audit-first** — we can ship human-readable timelines immediately.
3) **Replay-ready** — testing and BI can work off logs without re-running the engine.

## Next (Phase 10 proper)
- Wire provenance into Pipeline with a feature flag.
- Add unit tests that assert presence/shape of provenance rows (behind an env flag to keep base tests green).
- Extend `resolution` with strategy versions and policy flags for better analytics.
