# nlp/__init__.py
from __future__ import annotations
import importlib, sys

# Proxy the entire 'nlp' package to 'src.nlp' so that imports like
#   from nlp.canonicalize import canonicalize
# resolve to the implementations living under src/nlp/.
_pkg = importlib.import_module('src.nlp')

# expose the underlying package's path so submodule imports work
try:
    __path__ = _pkg.__path__  # type: ignore[attr-defined]
except Exception:
    pass

# re-export everything public from src.nlp (optional convenience)
for _k in dir(_pkg):
    if not _k.startswith('_'):
        globals()[_k] = getattr(_pkg, _k)

# Ensure Python treats 'nlp' as the same module object as 'src.nlp'
sys.modules[__name__] = _pkg
