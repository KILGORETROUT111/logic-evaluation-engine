from __future__ import annotations
import json, sys
from glob import glob
from pathlib import Path

# Optional: add repo root (not strictly needed here, but consistent)
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

def newest_json() -> Path | None:
    files = sorted((Path(p) for p in glob("data/logs/*.json")),
                   key=lambda p: p.stat().st_mtime if p.exists() else 0.0,
                   reverse=True)
    return files[0] if files else None

def _final_phase_from_prov(j: Path) -> str | None:
    prov = j.with_suffix(".prov.jsonl")
    final = None
    if prov.exists():
        with prov.open("r", encoding="utf-8") as f:
            for line in f:
                try:
                    obj = json.loads(line)
                except Exception:
                    continue
                if obj.get("kind") == "transition":
                    final = obj.get("phase_after") or final
    return final

def _last_detect_enrichment(j: Path):
    prov = j.with_suffix(".prov.jsonl")
    last = None
    if prov.exists():
        with prov.open("r", encoding="utf-8") as f:
            for line in f:
                try:
                    obj = json.loads(line)
                except Exception:
                    continue
                if obj.get("kind") == "detect":
                    last = obj
    return (last or {}).get("details", {}).get("enrichment")

def main():
    j = newest_json()
    if not j:
        print("No logs found under data/logs/")
        return
    print(f"Newest: {j}")

    # summary json (may be minimal depending on pipeline snapshot)
    try:
        meta = json.loads(j.read_text(encoding="utf-8"))
    except Exception:
        meta = {}

    enrich = _last_detect_enrichment(j)
    final_phase = meta.get("final_phase") or _final_phase_from_prov(j)
    domain = meta.get("domain") or (enrich or {}).get("domain")

    print("Summary:", {"domain": domain, "final_phase": final_phase})
    print("Enrichment(last_detect):", enrich)

if __name__ == "__main__":
    main()
