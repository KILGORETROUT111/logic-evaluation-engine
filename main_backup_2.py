import os

# Add Graphviz's bin folder to the PATH at runtime
os.environ["PATH"] += os.pathsep + r"C:\Program Files\Graphviz\bin"

import sys
from core.parser import parse_expression
from core.evaluation import evaluate_full

import sys
import json
from datetime import datetime
from core.parser import parse_expression
from core.evaluation import evaluate_full
from core.visualize import visualize_trace_graph

def main():
    # Interactive CLI
    expr_input = input("Enter expression (e.g. [\"EX\", \"x\", \"JAM\"]): ").strip()
    try:
        parsed_json = json.loads(expr_input)
        expr = parse_expression(parsed_json)
    except Exception as e:
        print("❌ JSON parse or expression build failed:", e)
        sys.exit(1)

    # Optional context (you can expand this)
    context = {"x": 1, "z": 2}

    # Ask for version tag
    version_input = input("Enter version tag (e.g. v1.0.0): ").strip()
    if not version_input:
        version_input = "v0.0.0"

    # Create versioned output directory
    date_tag = datetime.now().strftime("v_%Y%m%d")
    version_folder = f"{version_input}__{date_tag}"
    output_path = os.path.join("releases", version_folder)

    # Evaluate
    state, trace = evaluate_full(expr, context)

    # Print to console
    print("Final state:", state)
    print("Trace:")
    for k, v in trace.items():
        print(f"{k} → {[str(e) for e in v]}")

    # Final evaluation output
    print("Final state:", state)
    print("Trace:")
    for k, v in trace.items():
        print(f"{k} → {[str(e) for e in v]}")

    # Generate diagram
    from core.visualize import visualize_trace_graph
    visualize_trace_graph(trace, context=context, final_state=state)


    # Generate diagrams and save metadata
    visualize_trace_graph(trace, context=context, final_state=state,
                          out_dir="out", versioned_dir=output_path)

if __name__ == "__main__":
    main()