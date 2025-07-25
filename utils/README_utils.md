
# 🛠️ Utils Module Overview – Logic Evaluation Engine (LEE)

The `utils/` directory contains foundational infrastructure tools used throughout LEE:

- Safe I/O printing
- Structured logging
- Trace conversion for exports
- Debug-friendly internal hooks

---

## 📘 Modules

| File             | Description |
|------------------|-------------|
| `alpha_rename.py`  | Utility for renaming bound variables during substitution |
| `logging.py`       | Logging infrastructure for proof, diagnostics, and engine activity |
| `safe_print.py`    | Handles clean printing in threaded or subprocess environments |
| `trace_export.py`  | Export trace logs to structured `.json` or `.txt` |
| `trace_logger.py`  | Real-time trace builder |
| `trace_to_proof.py`| Converts trace logs into readable proof chains |
| `__init__.py`      | Declares `utils` as a package |
