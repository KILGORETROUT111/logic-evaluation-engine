# Logic Evaluation Engine (LEE) · v3.0

**LEE** is a phase-aware logic engine with a tiny AST, deterministic phase flow, and provenance trails.

- **Phase geometry**: `ALIVE → JAM → MEM` (final phase **MEM**), with a small allowed transition matrix.
- **Adapters / enrichment**: domain hooks (legal/medical), divergence classification, NER, counterfactual passthrough.
- **Provenance**: per-run JSON log + JSONL provenance + phase timeline (`.md` + `.dot`).

## Quick links
- [Getting Started](getting-started.md)
- [Phase Geometry](phase-geometry.md)
- [API Overview](api.md)
- [Adapter Hooks](adapter-hooks.md)
- [Contributing](contributing.md)

> These docs are versioned with MkDocs Material + **mike**. Use the version selector in the footer when published.
