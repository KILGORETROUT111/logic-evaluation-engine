# src/engine/event_log.py
from __future__ import annotations
import os, json, glob, hashlib
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

LOG_DIR = os.path.join("data", "logs")
os.makedirs(LOG_DIR, exist_ok=True)

# Keep only the most recent N runs (JSON/SVG pairs)
MAX_RUNS = 50

def _prune_old_runs(log_dir: str, stem_prefix: str) -> None:
    jsons = sorted(
        glob.glob(os.path.join(log_dir, f"{stem_prefix}_*.json")),
        key=lambda p: os.path.getmtime(p)
    )
    extra = max(0, len(jsons) - MAX_RUNS)
    for path in jsons[:extra]:
        try: os.remove(path)
        except Exception: pass
        maybe_svg = os.path.splitext(path)[0] + ".svg"
        try:
            if os.path.exists(maybe_svg):
                os.remove(maybe_svg)
        except Exception:
            pass

class EventLog:
    """
    BI-friendly event log:
      - JSON stream (for dev)
      - SVG timeline (for quick glance)
      - OLAP rows (Parquet if pyarrow; else CSV) for BI tools
    """
    def __init__(self, name: str = "timeline", *, run_id: Optional[str] = None, session: Optional[str] = None):
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
        self.log_name = name
        self.run_id = run_id or self._hash16(f"{name}:{stamp}")
        self.session = session or ""
        self.json_path = os.path.join(LOG_DIR, f"{name}_{stamp}.json")
        self.svg_path  = os.path.join(LOG_DIR, f"{name}_{stamp}.svg")
        self.rows_path_parquet = os.path.join(LOG_DIR, f"{name}_{stamp}.parquet")
        self.rows_path_csv = os.path.join(LOG_DIR, f"{name}_{stamp}.csv")

        self._events: List[Dict[str, Any]] = []
        self._olap_rows: List[Dict[str, Any]] = []
        self._event_id = 0

        _prune_old_runs(LOG_DIR, name)

    # ----------------- public -----------------

    def event(self, kind: str, payload: Dict[str, Any]) -> None:
        # enrich payload minimally
        ts = datetime.now(timezone.utc)
        data = {
            "ts": ts.isoformat(),
            "type": kind,
            "data": payload,
        }
        self._events.append(data)
        # write-through json for dev safety
        try:
            with open(self.json_path, "w", encoding="utf-8") as f:
                json.dump(self._events, f, indent=2, ensure_ascii=False)
        except Exception:
            pass

        # build an OLAP row
        try:
            self._event_id += 1
            row = self._row_from_event(kind, ts, payload, self._event_id)
            self._olap_rows.append(row)
        except Exception:
            pass

    def snapshot_svg(self) -> None:
        """
        Minimal SVG timeline (unchanged in spirit), plus we write OLAP rows.
        """
        y, x = 50, 40
        lines = [
            '<svg xmlns="http://www.w3.org/2000/svg" width="960" height="160">',
            '<style>text{font-family:monospace;font-size:11px}</style>',
            f'<text x="10" y="20">LEE timeline · {self.log_name} · {self.run_id}</text>'
        ]
        for ev in self._events:
            label = ev["data"].get("phase", ev["type"])
            extra = ""
            if ev.get("type") == "jam":
                pat = ev["data"].get("details", {}).get("witness", {}).get("pattern")
                if pat:
                    extra = f" [{pat}]"
            lines.append(f'<circle cx="{x}" cy="{y}" r="6" fill="black"/>')
            lines.append(f'<text x="{x+10}" y="{y+4}">{label}{extra}</text>')
            x += 160
        lines.append("</svg>")
        try:
            with open(self.svg_path, "w", encoding="utf-8") as f:
                f.write("\n".join(lines))
        except Exception:
            pass

        # Write OLAP rows: Parquet if possible, else CSV
        self._write_olap_rows()

    # ----------------- internals -----------------

    def _row_from_event(self, kind: str, ts: datetime, payload: Dict[str, Any], eid: int) -> Dict[str, Any]:
        # dimension basics
        phase = payload.get("phase") or ""
        details = payload.get("details") or {}
        mode = details.get("mode") or payload.get("mode") or ""
        witness = details.get("witness") or payload.get("witness") or {}
        witness_pattern = witness.get("pattern") or ""
        witness_hash = self._hash16(json.dumps(witness, sort_keys=True)) if witness else ""

        # extras
        time_to_mem_ms = payload.get("time_to_mem_ms")
        resolution = payload.get("resolution") or {}
        analytic = payload.get("analytic") or {}
        ast_size = details.get("ast_size") or payload.get("ast_size")
        depth = details.get("depth") or payload.get("depth")

        row = {
            "run_id": self.run_id,
            "log_name": self.log_name,
            "session": self.session,
            "event_id": eid,
            "event_type": kind,
            "phase": phase,
            "ts": ts.isoformat(),
            "date": ts.date().isoformat(),
            "hour": ts.hour,

            "mode": mode,
            "witness_pattern": witness_pattern,
            "witness_hash": witness_hash,

            "resolution_strategy": resolution.get("strategy") or "",
            "resolution_applied": 1 if resolution.get("applied") else 0,
            "artifact_created": 1 if analytic.get("artifact") else 0,

            "time_to_mem_ms": time_to_mem_ms if isinstance(time_to_mem_ms, (int, float)) else None,
            "ast_size": ast_size if isinstance(ast_size, int) else None,
            "depth": depth if isinstance(depth, int) else None,
        }
        return row

    def _write_olap_rows(self) -> None:
        rows = self._olap_rows
        if not rows:
            return
        # Parquet preferred
        try:
            import pyarrow as pa  # type: ignore
            import pyarrow.parquet as pq  # type: ignore
            table = pa.Table.from_pylist(rows)
            pq.write_table(table, self.rows_path_parquet)
            return
        except Exception:
            pass
        # CSV fallback
        try:
            import csv
            keys = sorted({k for r in rows for k in r.keys()})
            with open(self.rows_path_csv, "w", newline="", encoding="utf-8") as f:
                w = csv.DictWriter(f, fieldnames=keys)
                w.writeheader()
                for r in rows:
                    w.writerow(r)
        except Exception:
            pass

    @staticmethod
    def _hash16(s: str) -> str:
        return hashlib.md5(s.encode("utf-8")).hexdigest()[:16]