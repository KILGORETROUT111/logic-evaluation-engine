import json
import os

def emit_trace_to_json(trace, filename="trace_output.json", out_dir="out"):
    """
    Emit the trace to a JSON file for later visualization or inspection.

    Parameters:
    - trace: A list of LEEEvent instances or dictionaries.
    - filename: Output JSON filename.
    - out_dir: Directory to write the JSON file into.
    """
    os.makedirs(out_dir, exist_ok=True)
    output_path = os.path.join(out_dir, filename)

# Convert to dict if trace contains LEEEvent objects
def emit_trace_to_json(trace: list, output_path: str = "out/trace_output.json"):
    """Serializes the trace to a JSON file."""
    serialized = []
    for e in trace:
        event_dict = e.to_dict() if hasattr(e, "to_dict") else e
        if isinstance(event_dict, dict) and "value" in event_dict:
            event_dict["value"] = repr(event_dict["value"])
        serialized.append(event_dict)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(serialized, f, indent=2, ensure_ascii=False)

    print(f"[TRACE EXPORT] Trace written to: {output_path}")