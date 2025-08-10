# Project LEE-3.0 Changelog

## [2025-08-10]
- **Phase 12 MEMDB Integration**
  - Added in-memory + JSONL persistence for phase results.
  - CSV export + CLI commands (`report`, `export`).
  - Unit tests for storage + export pass.
- **Pipeline Patch**
  - Fixed indentation/import scope bugs.
  - Added MEMDB activation checks.
- **Test Cleanup**
  - Removed stale bytecode and `__pycache__`.

## [2025-08-09]
- Patched `Pipeline.run` to eliminate `UnboundLocalError`.
- Began MEMDB integration scaffolding.
