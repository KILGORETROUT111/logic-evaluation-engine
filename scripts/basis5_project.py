from __future__ import annotations

import argparse
import json
import sys
from glob import glob
from pathlib import Path
from typing import List

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.core.basis5 import build_winding  # type: ignore


def newest_json() -> Path | None:
    files = sorted(
        (Path(p) for p in glob(str(ROOT / "data/logs/*.json"))),
        key=lambda p: p.stat().st_mtime if p.exists() else 0.0,
        reverse=True,
    )
    return files[0] if files else None


def extract_phases(prov_path: Path) -> List[str]:
    phases: List[str] = []
    if not prov_path.exists():
        return phases
    for line in prov_path.read_text(encoding="utf-8").splitlines():
        try:
            ev = json.loads(line)
        except Exception:
            continue
        if ev.get("kind") == "transition":
            phases.append(ev.get("phase_after"))
    return phases


def main() -> None:
    ap = argparse.ArgumentParser(description="Project latest run phases into basis5 winding history")
    ap.add_argument("--log", default="", help="Optional explicit log JSON path; defaults to newest under data/logs")
    args = ap.parse_args()

    log = Path(args.log) if args.log else newest_json()
    if not log or not log.exists():
        print("No log json found.")
        return

    phases = extract_phases(log.with_suffix(".prov.jsonl"))
    # include final phase from summary if not already present
    try:
        summary = json.loads(log.read_text(encoding="utf-8"))
        final = summary.get("final_phase") or summary.get("state", {}).get("phase")
        if final and (not phases or phases[-1] != final):
            phases.append(final)
    except Exception:
        pass

    if not phases:
        print("No phases found in provenance or summary.")
        return

    proj = build_winding(phases)
    out = log.with_suffix(".basis5.json")
    out.write_text(json.dumps(proj, indent=2), encoding="utf-8")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
