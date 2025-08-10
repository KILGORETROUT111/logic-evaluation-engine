from __future__ import annotations

from .pipeline import Pipeline

try:
    from .evaluator import evaluate_expression  # type: ignore
except Exception:
    evaluate_expression = None  # type: ignore

try:
    from .evaluator import evaluate_full  # type: ignore
except Exception:
    evaluate_full = None  # type: ignore

__all__ = ["Pipeline", "evaluate_expression", "evaluate_full"]
