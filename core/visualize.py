from datetime import datetime
import os
from graphviz import Digraph
import json

def visualize_trace_graph(trace, context=None, final_state=None, out_dir="out", versioned_dir="releases"):
    os.makedirs(out_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    base_name = f"trace_diagram_{timestamp}"
    png_path = os.path.join(out_dir, f"{base_name}.png")
    svg_path = os.path.join(out_dir, f"{base_name}.svg")
    manifest_path = os.path.join(out_dir, f"{base_name}_manifest.json")

    dot = Digraph(comment="Evaluation Trace", format="png")

    for phase, nodes in trace.items():
        for idx, node in enumerate(nodes):
            node_id = f"{phase}_{idx}"
            dot.node(node_id, f"{phase}\n{str(node)}")

    phase_keys = list(trace.keys())
    for i in range(len(phase_keys) - 1):
        dot.edge(f"{phase_keys[i]}_0", f"{phase_keys[i + 1]}_0")

    dot.render(filename=png_path, format="png", cleanup=True)
    dot.render(filename=svg_path, format="svg", cleanup=True)

    manifest = {
        "timestamp": timestamp,
        "final_state": str(final_state),
        "context": context,
        "trace": {k: [str(n) for n in v] for k, v in trace.items()},
        "files": {
            "png": png_path,
            "svg": svg_path
        }
    }

    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)

    return {
        "timestamp": timestamp,
        "svg_path": svg_path,
        "png_path": png_path,
        "manifest_path": manifest_path
    }