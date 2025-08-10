from __future__ import annotations
from typing import Any, Callable, Dict, Optional

class HookRegistry:
    """
    Simple registry you can extend without touching Evaluator:
      hooks.register("quantifier_rewrite", fn)
      hooks.try_call("quantifier_rewrite", expr=..., state=...)
    """
    def __init__(self):
        self._hooks: Dict[str, Callable[..., Any]] = {}

    def register(self, name: str, fn: Callable[..., Any]) -> None:
        self._hooks[name] = fn

    def try_call(self, name: str, **kwargs) -> Optional[Any]:
        fn = self._hooks.get(name)
        if not fn:
            return None
        try:
            return fn(**kwargs)
        except Exception:
            # keep the evaluator robust even if a hook blows up
            return None
