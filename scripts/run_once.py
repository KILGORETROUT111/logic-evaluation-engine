from __future__ import annotations
import argparse, json, sys
from pathlib import Path

# Ensure repo root on sys.path so `from src...` works when run as a script
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.engine import Pipeline  # now resolves

def _last_detect_enrichment(log_json: str):
    try:
        prov = Path(log_json).with_suffix(".prov.jsonl")
        if not prov.exists():
            return None
        last = None
        with prov.open("r", encoding="utf-8") as f:
            for line in f:
                try:
                    obj = json.loads(line)
                except Exception:
                    continue
                if obj.get("kind") == "detect":
                    last = obj
        if last:
            return last.get("details", {}).get("enrichment")
    except Exception:
        return None
    return None

def main():
    ap = argparse.ArgumentParser(description="Run one LEE evaluation")
    ap.add_argument("--expr", required=True, help='Expression, e.g. "1 -> 0"')
    ap.add_argument("--domain", choices=["legal","medical"], required=True)
    ap.add_argument("--log", default="cli_run", help="Log name prefix")
    ap.add_argument("--session", default="cli", help="Session tag")
    ap.add_argument("--no-prov", action="store_true", help="Disable provenance")
    args = ap.parse_args()

    p = Pipeline(
        log_name=args.log,
        domain=args.domain,
        enable_provenance=not args.no_prov,
        session=args.session,
    )
    res = p.run(args.expr)

    print(json.dumps({
        "phase": res["state"]["phase"],
        "history": res.get("history"),
        "log_json": res.get("log_json"),
        "log_svg": res.get("log_svg"),
        "enrichment(last_detect)": _last_detect_enrichment(res.get("log_json", "")),
    }, indent=2))

if __name__ == "__main__":
    main()
