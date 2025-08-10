from __future__ import annotations
from typing import Any, Protocol, Optional, Dict

class AdapterProtocol(Protocol):
    domain: str
    def initialize(self, config: Optional[Dict[str, Any]] = None) -> None: ...
    def enrich(self, normalized_expr: str) -> Dict[str, Any]: ...
    def close(self) -> None: ...

class AdapterRegistry:
    _adapters: dict[str, type[AdapterProtocol]] = {}

    @classmethod
    def register(cls, domain: str):
        def _wrap(adapter_cls: type[AdapterProtocol]):
            cls._adapters[domain] = adapter_cls
            return adapter_cls
        return _wrap

    @classmethod
    def create(cls, domain: str, config: Optional[Dict[str, Any]] = None) -> AdapterProtocol:
        if domain not in cls._adapters:
            raise KeyError(f"No adapter registered for domain '{domain}'")
        inst = cls._adapters[domain]()  # type: ignore[call-arg]
        inst.initialize(config or {})
        return inst
