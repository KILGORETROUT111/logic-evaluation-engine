
# src/engine/audit.py
from __future__ import annotations
import json
from typing import Any, Dict, List
from pathlib import Path

def load_event_log(json_path: str | Path) -> List[Dict[str, Any]]:
    """Load the EventLog JSON list (as written by EventLog)."""
    data = json.loads(Path(json_path).read_text(encoding="utf-8"))
    assert isinstance(data, list), "EventLog JSON should be a list of events"
    return data

def to_jsonl(events: List[Dict[str, Any]]) -> str:
    """Flatten EventLog events to JSONL for audit/replay pipelines."""
    return "\n".join(json.dumps(e, ensure_ascii=False) for e in events)

def to_markdown_timeline(events: List[Dict[str, Any]]) -> str:
    lines = ["# LEE Audit Timeline", ""]
    for ev in events:
        ts = ev.get("ts","")
        typ = ev.get("type","")
        phase = ev.get("data",{}).get("phase","")
        det = ev.get("data",{}).get("details",{})
        mode = det.get("mode") or ev.get("data",{}).get("mode","")
        pat = (det.get("witness") or {}).get("pattern","")
        lines.append(f"- **{ts}** · `{typ}` · phase=`{phase}`" + (f" · mode=`{mode}` · witness=`{pat}`" if pat or mode else ""))
    return "\n".join(lines)

def to_graphviz_dot(events: List[Dict[str, Any]]) -> str:
    """Produce a simple DOT graph of the phase sequence with JAM annotations."""
    nodes = []
    edges = []
    prev = None
    idx = 0
    for ev in events:
        idx += 1
        label = ev.get("type","")
        phase = ev.get("data",{}).get("phase","")
        pat = (ev.get("data",{}).get("details",{}) or {}).get("witness",{}).get("pattern","")
        node_name = f"n{idx}"
        node_label = f"{label}\n{phase}" + (f"\n[{pat}]" if pat else "")
        nodes.append(f'{node_name} [shape=circle, label="{node_label}"];')
        if prev:
            edges.append(f"{prev} -> {node_name};")
        prev = node_name
    dot = ["digraph LEE {", 'rankdir=LR;']
    dot.extend(nodes)
    dot.extend(edges)
    dot.append("}")
    return "\n".join(dot)
