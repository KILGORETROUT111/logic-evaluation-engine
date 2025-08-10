from __future__ import annotations
import os, json
from datetime import datetime
from typing import Any, Dict, List



LOG_DIR = os.path.join("data", "logs")
os.makedirs(LOG_DIR, exist_ok=True)

class EventLog:
    def __init__(self, name: str = "timeline"):
        stamp = datetime.utcnow().strftime("%Y%m%dT%H%M%S")
        self.json_path = os.path.join(LOG_DIR, f"{name}_{stamp}.json")
        self.svg_path  = os.path.join(LOG_DIR, f"{name}_{stamp}.svg")
        self._events: List[Dict[str, Any]] = []

    def event(self, kind: str, payload: Dict[str, Any]) -> None:
        self._events.append({
            "ts": datetime.utcnow().isoformat(),
            "type": kind,
            "data": payload
        })
        # write-through json for safety
        with open(self.json_path, "w", encoding="utf-8") as f:
            json.dump(self._events, f, indent=2, ensure_ascii=False)

    def snapshot_svg(self) -> None:
        """
        Minimal placeholder: draw phases along a horizontal line.
        You can replace this with graphviz or your preferred renderer later.
        """
        y, x = 50, 40
        lines = [
            '<svg xmlns="http://www.w3.org/2000/svg" width="960" height="120">',
            f'<text x="10" y="20" font-family="monospace" font-size="12">LEE timeline</text>'
        ]
        for ev in self._events:
            label = ev["data"].get("phase", ev["type"])
            lines.append(f'<circle cx="{x}" cy="{y}" r="6" fill="black"/>')
            lines.append(f'<text x="{x+10}" y="{y+4}" font-family="monospace" font-size="10">{label}</text>')
            x += 120
        lines.append("</svg>")
        with open(self.svg_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

# src/engine/event_log.py  (ADD these near top)
import os, glob

MAX_RUNS = 50  # keep last 50 JSON/SVG pairs

def _prune_old_runs(log_dir: str, stem_prefix: str):
    """
    Deletes oldest log pairs beyond MAX_RUNS. Safe: ignores missing mates.
    """
    # Find all json files for this stem
    jsons = sorted(
        glob.glob(os.path.join(log_dir, f"{stem_prefix}_*.json")),
        key=lambda p: os.path.getmtime(p)
    )
    # If we have <= MAX_RUNS, nothing to do
    extra = max(0, len(jsons) - MAX_RUNS)
    for path in jsons[:extra]:
        try:
            os.remove(path)
        except Exception:
            pass
        # try to remove matching svg
        maybe_svg = os.path.splitext(path)[0] + ".svg"
        try:
            if os.path.exists(maybe_svg):
                os.remove(maybe_svg)
        except Exception:
            pass

