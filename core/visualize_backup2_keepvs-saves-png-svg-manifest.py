from graphviz import Digraph
from datetime import datetime
import os
import json

def visualize_trace_graph(trace, context=None, final_state=None, out_dir="out", versioned_dir="releases"):
    os.makedirs(out_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    base_name = f"trace_diagram_{timestamp}"
    output_base = os.path.join(out_dir, base_name)

    dot = Digraph(comment="Evaluation Trace")  # no need to specify format here

    # Create nodes for each item in trace
    for phase, nodes in trace.items():
        for idx, node in enumerate(nodes):
            node_id = f"{phase}_{idx}"
            label = f"{phase}\n{str(node)}"
            dot.node(node_id, label)

    # Draw linear edges between phases (basic pass)
    phase_keys = list(trace.keys())
    for i in range(len(phase_keys) - 1):
        dot.edge(f"{phase_keys[i]}_0", f"{phase_keys[i + 1]}_0")

    # Render to .png and .svg
    png_path = dot.render(output_base, format="png", cleanup=True)
    svg_path = dot.render(output_base, format="svg", cleanup=True)

    # Optional: also export trace metadata as JSON
    manifest = {
        "timestamp": timestamp,
        "final_state": str(final_state),
        "context": context,
        "trace": {k: [str(n) for n in v] for k, v in trace.items()},
        "files": {
            "svg": svg_path,
            "png": png_path,
        }
    }

    manifest_path = os.path.join(out_dir, f"{base_name}_manifest.json")
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)

    print("✅ Trace diagram generated:")
    print("   PNG:", png_path)
    print("   SVG:", svg_path)
    print("   Manifest:", manifest_path)