# Logic Evaluation Engine (LEE) · v3.0

**LEE** is a phase-aware logic engine with a tiny AST, deterministic phase flow, and provenance trails.

- **Phase geometry**: `ALIVE → JAM → MEM` (final state **MEM**) with allowed transitions defined (see _Phase Geometry_).
- **Adapters / enrichment**: domain-aware hooks (legal, medical), divergence classification, NER, counterfactuals passthrough.
- **Provenance**: JSON log + JSONL provenance + timeline (`.md` + `.dot`) emitted per run.
- **Minimal API**: `Pipeline.run(expr)`, `canonicalize(...)`, `contradiction.analyze(...)`.

> These docs are versioned. Switch versions with the selector in the footer (Material + mike).

## Quick links
- [Getting Started](getting-started.md)
- [Phase Geometry](phase-geometry.md)
- [API Overview](api.md)
- [Adapter Hooks](adapter-hooks.md)
- [Contributing](contributing.md)
