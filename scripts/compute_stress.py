#!/usr/bin/env python3
import argparse, pathlib, json, os, socket, subprocess, time
from stress_toolkit import compute_stress, load_phases_from_summary

# NOTE: you said the helper is named prov_util.py (singular)
from prov_util import append_prov   # if your file is prov_utils.py, change this import

def _git_rev_or_none():
    try:
        return subprocess.check_output(["git","rev-parse","--short","HEAD"], stderr=subprocess.DEVNULL).decode().strip()
    except Exception:
        return None

def main():
    ap = argparse.ArgumentParser(
        description="Compute StressIndex/Winding/Resistance (and bianchi_residual) from a LEE run and emit provenance."
    )
    ap.add_argument("--summary", required=True, help="Path to <log>.json summary file")
    ap.add_argument("--out", help="Output metrics JSON path (default: alongside summary)", default=None)

    # provenance outputs
    ap.add_argument("--prov-out", help="Path to <log>.prov.jsonl (default: alongside summary)", default=None)

    # exhaustibility metadata (optional)
    ap.add_argument("--exhaustibility-class", choices=["I","II","III"], default=None,
                    help="Override automatic class assignment (I|II|III).")
    ap.add_argument("--evidence", nargs="*", default=None,
                    help="Evidence tags, e.g. complexity_upper_bound approx_algo_v1")
    ap.add_argument("--reviewer", default=None,
                    help='Reviewer tag, e.g. "WAP-IV"')

    args = ap.parse_args()

    summary = pathlib.Path(args.summary).resolve()
    out_path = pathlib.Path(args.out) if args.out else summary.with_name(summary.stem + "_StressIndex_metrics.json")

    # default prov path
    prov_out = pathlib.Path(args.prov_out) if args.prov_out else summary.with_suffix(".prov.jsonl")

    # --- load & compute ---
    phases = load_phases_from_summary(summary)
    # expected to return dict with keys: stress_index, winding, resistance, bianchi_residual, run_id, dataset_id, etc.
    metrics = compute_stress(phases, prov_out)  # pass-through if your toolkit uses it; safe even if ignored

    # fallbacks if toolkit doesn't populate IDs
    run_id = str(metrics.get("run_id") or summary.stem)
    dataset_id = str(metrics.get("dataset") or metrics.get("dataset_id") or "unknown")

    # required numeric fields with safe defaults
    stress_index   = float(metrics.get("stress_index", 0.0))
    winding        = float(metrics.get("winding", 0.0))
    resistance     = float(metrics.get("resistance", 0.0))
    bianchi_resid  = float(metrics.get("bianchi_residual", metrics.get("bianchi_resid", 0.0)))
    duration_s     = float(metrics.get("duration_s", metrics.get("duration_secs", 0.0)))

    # --- write metrics JSON ---
    out_payload = {
        "run_id": run_id,
        "dataset": dataset_id,
        "stress_index": stress_index,
        "winding": winding,
        "resistance": resistance,
        "bianchi_residual": bianchi_resid,
        "duration_s": duration_s,
        "source_summary": str(summary),
        "written_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
    }
    out_path.write_text(json.dumps(out_payload, indent=2), encoding="utf-8")
    print(f"[stress] wrote metrics -> {out_path}")

    # --- exhaustibility class inference (very conservative defaults) ---
    approx_used               = bool(metrics.get("approx_used", False))
    truncated_for_runtime     = bool(metrics.get("truncated_for_runtime", False))
    phase_tensor_ir_needed    = bool(metrics.get("phase_tensor_ir_needed", False))
    phase_tensor_ir_implemented = bool(metrics.get("phase_tensor_ir_implemented", True))
    theoretical_barrier       = bool(metrics.get("theoretical_barrier_detected", False))

    inferred_class = None
    inferred_evidence = []
    if approx_used or truncated_for_runtime:
        inferred_class = "I"
        inferred_evidence = ["approximation" if approx_used else None,
                             "runtime_truncation" if truncated_for_runtime else None]
    elif phase_tensor_ir_needed and not phase_tensor_ir_implemented:
        inferred_class = "II"
        inferred_evidence = ["translator_missing", "phase_tensor_ir_required"]
    elif theoretical_barrier:
        inferred_class = "III"
        inferred_evidence = ["undecidability_hint", "no_go_argument"]

    # CLI wins over inference
    exh_class = args.exhaustibility_class or inferred_class
    evidence  = (args.evidence or [e for e in inferred_evidence if e]) or None

    # --- append provenance JSONL ---
    payload = {
        "run_id": run_id,
        "dataset": dataset_id,
        "stress_index": stress_index,
        "winding": winding,
        "resistance": resistance,
        "bianchi_residual": bianchi_resid,
        "duration_s": duration_s,
    }

    git_rev = _git_rev_or_none()
    machine_id = socket.gethostname()

    append_prov(
        path=str(prov_out),
        event="stress_index_run",
        payload=payload,
        exhaustibility_class=exh_class,
        evidence=evidence,
        reviewer=(args.reviewer or "WAP-IV"),
        context={
            "cli": vars(args),
            "git_rev": git_rev,
            "machine": machine_id,
        },
    )
    print(f"[stress] appended provenance -> {prov_out}")

if __name__ == "__main__":
    main()
