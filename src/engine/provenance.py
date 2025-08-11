from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional


class ProvenanceRecorder:
    """
    Minimal provenance writer: one JSONL per run (sidecar of the primary log JSON).
    Kinds: start, prenorm, enrich, detect, transition
    """

    def __init__(self, json_path: str | Path) -> None:
        self.json_path = Path(json_path)
        self.prov_path = self.json_path.with_suffix(".prov.jsonl")
        self.prov_path.parent.mkdir(parents=True, exist_ok=True)

    def _ts(self) -> str:
        return datetime.now().isoformat(timespec="milliseconds")

    def _write(self, payload: Dict[str, Any]) -> None:
        # append one JSON object per line
        with self.prov_path.open("a", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False)
            f.write("\n")

    # --- event helpers ---

    def start(self, *, session: str, domain: Optional[str], expr: str) -> None:
        self._write(
            {
                "kind": "start",
                "session": session,
                "domain": domain,
                "expr": expr,
                "ts": self._ts(),
            }
        )

    def prenorm(self, *, raw: str, normalized: str) -> None:
        self._write(
            {
                "kind": "prenorm",
                "raw": raw,
                "normalized": normalized,
                "ts": self._ts(),
            }
        )

    def enrich(self, *, details: Dict[str, Any]) -> None:
        self._write({"kind": "enrich", "details": details, "ts": self._ts()})

    def detect(self, *, phase_after: str, details: Dict[str, Any]) -> None:
        self._write(
            {
                "kind": "detect",
                "phase_after": phase_after,
                "details": details,
                "ts": self._ts(),
            }
        )

    def transition(
        self,
        phase_before: Optional[str],
        phase_after: str,
        *,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        self._write(
            {
                "kind": "transition",
                "phase_before": phase_before,
                "phase_after": phase_after,
                "details": details or {},
                "ts": self._ts(),
            }
        )

    # --- simple timeline helpers ---

    def write_timeline_md(self) -> Path:
        md = self.json_path.with_suffix(".timeline.md")
        self._render_markdown_timeline(md)
        return md

    def write_timeline_dot(self) -> Path:
        dot = self.json_path.with_suffix(".timeline.dot")
        self._render_dot_timeline(dot)
        return dot

    # internal renderers

    def _render_markdown_timeline(self, path: Path) -> None:
        lines = []
        if self.prov_path.exists():
            for line in self.prov_path.read_text(encoding="utf-8").splitlines():
                try:
                    ev = json.loads(line)
                except Exception:
                    continue
                k = ev.get("kind")
                ts = ev.get("ts", "")
                if k == "transition":
                    lines.append(f"- {ts} transition: {ev.get('phase_before')} → {ev.get('phase_after')}")
                elif k in ("start", "prenorm", "enrich", "detect"):
                    lines.append(f"- {ts} {k}")
        if not lines:
            lines = ["- timeline: no events captured"]
        path.write_text("# Run Timeline\n\n" + "\n".join(lines) + "\n", encoding="utf-8")

    def _render_dot_timeline(self, path: Path) -> None:
        # very small DOT—good enough for a quick preview; not used by tests
        nodes = set()
        edges = []
        if self.prov_path.exists():
            for line in self.prov_path.read_text(encoding="utf-8").splitlines():
                try:
                    ev = json.loads(line)
                except Exception:
                    continue
                if ev.get("kind") == "transition":
                    a = ev.get("phase_before") or "ALIVE"
                    b = ev.get("phase_after")
                    nodes.add(a)
                    nodes.add(b)
                    edges.append((a, b))
        if not nodes:
            path.write_text("digraph G { ALIVE; }\n", encoding="utf-8")
            return
        body = ["digraph G {"]
        for n in nodes:
            body.append(f'  "{n}";')
        for a, b in edges:
            body.append(f'  "{a}" -> "{b}";')
        body.append("}\n")
        path.write_text("\n".join(body), encoding="utf-8")
