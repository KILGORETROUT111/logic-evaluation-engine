import argparse
import os
import json
from core.expressions import Lambda, Variable, Application, Literal
from core.evaluation import evaluate_full
from utils.safe_print import safe_print
from utils.trace_export import emit_trace_to_json
from utils.trace_to_proof import trace_to_proof

OUTPUT_DIR = "out"
TRACE_FILENAME = "trace_output.json"
trace_path = os.path.join(OUTPUT_DIR, TRACE_FILENAME)

def main():
    parser = argparse.ArgumentParser(description="Run or replay LEE logic engine.")
    parser.add_argument("--replay", action="store_true", help="Replay from saved trace")
    args = parser.parse_args()

    if args.replay:
        # --- REPLAY MODE ---
        if not os.path.exists(trace_path):
            safe_print(f"[ERROR] No trace file found at: {trace_path}")
            return

        with open(trace_path, "r", encoding="utf-8") as f:
            try:
                loaded = json.load(f)
                trace_data = loaded["trace"] if isinstance(loaded, dict) else loaded
            except Exception as e:
                safe_print(f"[ERROR] Failed to load or parse JSON trace: {e}")
                return

        safe_print("\n🔁 Step-by-step trace replay:\n")
        for i, event in enumerate(trace_data, start=1):
            safe_print(f"{i:02d}. [{event.get('phase', '')}] {event.get('expr', '')} → {event.get('value', '')}")

    else:
        # --- NORMAL EXECUTION MODE ---
        # Example input: ((λx. x) 42)
        expr = Application(
            Lambda("x", Variable("x")),
            Literal(42)
        )

        result, trace = evaluate_full(expr)

        safe_print(f"✅ Final Result: {result}")
        emit_trace_to_json(trace, trace_path)

        trace_to_proof(trace)

if __name__ == "__main__":
    main()