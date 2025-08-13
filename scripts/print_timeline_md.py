from __future__ import annotations
import json, sys
from glob import glob
from pathlib import Path

# ensure repo root on path (not strictly needed)
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

def newest_json() -> Path | None:
    files = sorted((Path(p) for p in glob("data/logs/*.json")),
                   key=lambda p: p.stat().st_mtime if p.exists() else 0.0,
                   reverse=True)
    return files[0] if files else None

def to_md(log_json: Path) -> str:
    prov = log_json.with_suffix(".prov.jsonl")
    items = []
    if prov.exists():
        with prov.open("r", encoding="utf-8") as f:
            for line in f:
                try:
                    e = json.loads(line)
                except Exception:
                    continue
                kind = e.get("kind")
                if kind == "start":
                    items.append(f"- **start** · domain=`{e.get('domain')}` session=`{e.get('session')}`")
                elif kind == "prenorm":
                    items.append(f"- **prenorm** · text=`{e.get('text')}` → `{e.get('normalized')}`")
                elif kind == "rewrite":
                    items.append(f"- **rewrite** · {e.get('rule')}")
                elif kind == "enrich":
                    items.append(f"- **enrich** · {e.get('adapter')} → `{e.get('what')}`")
                elif kind == "detect":
                    det = e.get("details", {})
                    tags = ",".join(det.get("enrichment", {}).get("tags", []) or [])
                    items.append(f"- **detect** · phase_after=`{e.get('phase_after')}` tags=[{tags}]")
                elif kind == "transition":
                    items.append(f"- **transition** · {e.get('phase_before')} → **{e.get('phase_after')}**")
    header = f"# Timeline for `{log_json.name}`\n\n"
    return header + ("\n".join(items) if items else "_No provenance events found._\n")

def main():
    j = newest_json()
    if not j:
        print("No logs found.")
        return
    md = j.with_suffix(".timeline.md")
    md.write_text(to_md(j), encoding="utf-8")
    print(f"Wrote {md}")

if __name__ == "__main__":
    main()
