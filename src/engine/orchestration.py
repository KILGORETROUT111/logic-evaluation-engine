# src/engine/orchestration.py
from __future__ import annotations

import json
import os
import uuid
from pathlib import Path
from typing import Any, Dict, Optional

try:
    import yaml  # optional, only for config file
except Exception:
    yaml = None  # type: ignore


# -------- Config loading --------

DEFAULT_CFG_PATH = Path("data/config/phase13.yaml")


def load_config(path: Optional[str | os.PathLike] = None) -> Dict[str, Any]:
    """
    Load Phase 13 config. If yaml isn't installed or file missing,
    fall back to a sane default (FileDriver).
    """
    cfg_path = Path(path) if path else DEFAULT_CFG_PATH
    if yaml is None or not cfg_path.exists():
        return {
            "driver": "file",
            "file": {
                "dir": "data/outbox",
                "prefix": "lee_evt_",
            },
        }
    with cfg_path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return data


# -------- Drivers --------

class BaseDriver:
    def publish(self, event_type: str, payload: Dict[str, Any]) -> None:  # pragma: no cover (interface)
        raise NotImplementedError


class FileDriver(BaseDriver):
    """
    Writes one JSON line per event into data/outbox/*.jsonl for easy smoke tests.
    """
    def __init__(self, directory: str = "data/outbox", prefix: str = "lee_evt_"):
        self.dir = Path(directory)
        self.dir.mkdir(parents=True, exist_ok=True)
        self.prefix = prefix

    def publish(self, event_type: str, payload: Dict[str, Any]) -> None:
        fname = f"{self.prefix}{event_type}.jsonl"
        path = self.dir / fname
        rec = {"type": event_type, "data": payload}
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")


class WebhookDriver(BaseDriver):
    """
    Simple HTTP POST webhook. Uses 'requests' if present, otherwise urllib.
    Config example:
      driver: webhook
      webhook:
        url: "https://example.com/hook"
        headers:
          Authorization: "Bearer XXX"
    """
    def __init__(self, url: str, headers: Optional[Dict[str, str]] = None):
        self.url = url
        self.headers = headers or {}

        try:
            import requests  # type: ignore
            self._requests = requests
        except Exception:
            self._requests = None

    def publish(self, event_type: str, payload: Dict[str, Any]) -> None:
        body = {"type": event_type, "data": payload}
        if self._requests:
            try:
                self._requests.post(self.url, json=body, headers=self.headers, timeout=5)
            except Exception:
                pass
        else:
            # urllib fallback
            try:
                import urllib.request
                req = urllib.request.Request(self.url, method="POST")
                for k, v in self.headers.items():
                    req.add_header(k, v)
                req.add_header("Content-Type", "application/json")
                data = json.dumps(body).encode("utf-8")
                with urllib.request.urlopen(req, data=data, timeout=5):  # nosec - tooling hook
                    pass
            except Exception:
                pass


# (Placeholder) Kafka driver shape, not wired by default
class KafkaDriver(BaseDriver):  # pragma: no cover (stub)
    def __init__(self, **kwargs):
        # you can fill this later with confluent_kafka or kafka-python
        self.kwargs = kwargs

    def publish(self, event_type: str, payload: Dict[str, Any]) -> None:
        # TODO: send to topic, e.g., kwargs["topic"]
        pass


# -------- Orchestrator --------

class Orchestrator:
    """
    Central facade. Choose a driver from config and expose publish().
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.cfg = config or load_config()
        self.driver = self._build_driver(self.cfg)

    def _build_driver(self, cfg: Dict[str, Any]) -> BaseDriver:
        kind = (cfg.get("driver") or "file").lower()
        if kind == "webhook":
            webhook = cfg.get("webhook") or {}
            return WebhookDriver(url=webhook.get("url", ""), headers=webhook.get("headers") or {})
        elif kind == "kafka":
            return KafkaDriver(**(cfg.get("kafka") or {}))
        else:
            file_cfg = cfg.get("file") or {}
            return FileDriver(directory=file_cfg.get("dir", "data/outbox"),
                              prefix=file_cfg.get("prefix", "lee_evt_"))

    def publish(self, event_type: str, payload: Dict[str, Any]) -> None:
        try:
            payload = dict(payload)
            payload.setdefault("event_id", uuid.uuid4().hex[:16])
            self.driver.publish(event_type, payload)
        except Exception:
            # never crash caller on orchestration errors
            pass
