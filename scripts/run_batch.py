from __future__ import annotations
import argparse, csv, json, sys, time
from pathlib import Path

# ensure repo root on path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.engine import Pipeline  # noqa: E402

def last_detect_enrichment(log_json: str) -> dict | None:
    p = Path(log_json).with_suffix(".prov.jsonl")
    if not p.exists():
        return None
    last = None
    with p.open("r", encoding="utf-8") as f:
        for line in f:
            try:
                obj = json.loads(line)
            except Exception:
                continue
            if obj.get("kind") == "detect":
                last = obj
    return (last or {}).get("details", {}).get("enrichment")

def run_batch(exprs: list[str], domain: str, session: str, log_prefix: str, provenance: bool) -> list[dict]:
    out: list[dict] = []
    for i, expr in enumerate(exprs, 1):
        name = f"{log_prefix}_{i:04d}"
        p = Pipeline(
            log_name=name,
            domain=domain,
            enable_provenance=provenance,
            session=session,
        )
        res = p.run(expr)
        enrich = last_detect_enrichment(res.get("log_json", "")) if provenance else None
        out.append({
            "idx": i,
            "expr": expr,
            "domain": domain,
            "phase": res["state"]["phase"],
            "elapsed_ms": res.get("elapsed_ms"),
            "log_json": res.get("log_json"),
            "log_svg": res.get("log_svg"),
            "enrichment": enrich,
        })
    return out

def main():
    ap = argparse.ArgumentParser(description="LEE batch runner")
    ap.add_argument("--file", required=True, help="Text file with one expression per line")
    ap.add_argument("--domain", choices=["legal","medical"], required=True)
    ap.add_argument("--session", default="batch")
    ap.add_argument("--log-prefix", default="batch")
    ap.add_argument("--no-prov", action="store_true", help="Disable provenance")
    ap.add_argument("--out", default="", help="Optional CSV output path (default under data/logs)")
    args = ap.parse_args()

    src = Path(args.file)
    exprs = [ln.strip() for ln in src.read_text(encoding="utf-8").splitlines() if ln.strip()]
    ts = time.strftime("%Y%m%d_%H%M%S")
    out_csv = Path(args.out) if args.out else Path(f"data/logs/{args.log_prefix}_{ts}.csv")
    out_csv.parent.mkdir(parents=True, exist_ok=True)

    rows = run_batch(exprs, args.domain, args.session, args.log_prefix, provenance=not args.no_prov)

    with out_csv.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else ["idx","expr","domain","phase"])
        w.writeheader()
        for r in rows:
            w.writerow(r)

    print(f"Wrote {len(rows)} rows → {out_csv}")

if __name__ == "__main__":
    main()
