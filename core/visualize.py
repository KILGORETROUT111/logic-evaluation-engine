
import os
import json
from datetime import datetime
from graphviz import Digraph

def visualize_trace_graph(trace, context=None, final_state=None, out_dir="out"):
    """
    Build and render the evaluation trace as a graph,
    then write a JSON manifest containing only serializable data.
    """
    # 1) Ensure output directory exists
    os.makedirs(out_dir, exist_ok=True)

    # 2) Create a new directed graph
    dot = Digraph(comment="Evaluation Trace", format="png")

    # 3) Add nodes: one per phase entry
    for phase, nodes in trace.items():
        for idx, node in enumerate(nodes):
            node_id = f"{phase}_{idx}"
            label = f"{phase}\\n{str(node)}"
            dot.node(node_id, label)

    # 4) Connect nodes in temporal order (simple linear chain)
    phase_keys = list(trace.keys())
    for i in range(len(phase_keys) - 1):
        dot.edge(f"{phase_keys[i]}_0", f"{phase_keys[i+1]}_0")

    # 5) Render PNG & SVG
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    png_path = os.path.join(out_dir, f"trace_{timestamp}.png")
    svg_path = os.path.join(out_dir, f"trace_{timestamp}.svg")
    dot.render(png_path, format="png", cleanup=True)
    dot.render(svg_path, format="svg", cleanup=True)

    # 6) Build JSON‐serializable manifest
    manifest = {
        "timestamp": timestamp,
        "final_state": str(final_state),
        "context": {k: str(v) for k, v in (context or {}).items()},
        "trace": {phase: [str(node) for node in nodes]
                  for phase, nodes in trace.items()}
    }

    manifest_path = os.path.join(out_dir, f"manifest_{timestamp}.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    # 7) Print output locations
    print(f"➜ Diagram PNG: {png_path}")
    print(f"➜ Diagram SVG: {svg_path}")
    print(f"➜ Manifest JSON: {manifest_path}")
