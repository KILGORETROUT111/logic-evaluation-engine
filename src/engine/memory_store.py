from __future__ import annotations
import os, json
from typing import Any, List

DATA_DIR = os.path.join("data", "memory")
os.makedirs(DATA_DIR, exist_ok=True)

class MemoryStore:
    def __init__(self, filename: str = "session.jsonl"):
        self.path = os.path.join(DATA_DIR, filename)
        # lazily create file
        if not os.path.exists(self.path):
            open(self.path, "a", encoding="utf-8").close()

    def append(self, record: dict[str, Any]) -> None:
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    def load(self, tail: int | None = None) -> List[dict[str, Any]]:
        out: List[dict[str, Any]] = []
        with open(self.path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    out.append(json.loads(line))
        return out[-tail:] if tail else out
