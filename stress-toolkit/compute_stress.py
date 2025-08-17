
#!/usr/bin/env python3
import argparse, pathlib, json
from stress_toolkit import compute_stress, load_phases_from_summary

def main():
    ap = argparse.ArgumentParser(description="Compute StressIndex/Winding/Resistance from a LEE run")
    ap.add_argument("--summary", required=True, help="Path to <log>.json summary file")
    ap.add_argument("--prov", help="Path to <log>.prov.jsonl provenance file", default=None)
    ap.add_argument("--out", help="Output metrics JSON path (default: alongside summary)", default=None)
    args = ap.parse_args()

    summary = pathlib.Path(args.summary)
    prov = pathlib.Path(args.prov) if args.prov else None
    out = pathlib.Path(args.out) if args.out else summary.with_name(summary.stem + "_StressIndex_metrics.json")

    phases = load_phases_from_summary(summary)
    metrics = compute_stress(phases, prov)

    out.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    print(f"[stress] wrote {out}")

if __name__ == "__main__":
    main()
