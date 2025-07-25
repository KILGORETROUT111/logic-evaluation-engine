
from evaluation.recursive_diagnostic_engine import run_recursive_diagnostic, Atom, Not, Axiom, And
import os
import json
import graphviz
from datetime import datetime

def export_diagnostic_output(branches, output_dir, timestamp):
    os.makedirs(output_dir, exist_ok=True)

    # .json
    with open(os.path.join(output_dir, f"diagnostic_output_{timestamp}.json"), "w", encoding="utf-8") as f_json:
        json.dump(branches, f_json, indent=2, ensure_ascii=False)

    # .txt
    with open(os.path.join(output_dir, f"diagnostic_output_{timestamp}.txt"), "w", encoding="utf-8") as f_txt:
        for b in branches:
            f_txt.write(f"=== BRANCH: {b['branch']} | PHASE: {b['phase']} ===\n")
            for step in b["steps"]:
                f_txt.write(f"➤ {step['expr']}\n")
            for k, v in b["meta"].items():
                f_txt.write(f"{k}: {v}\n")
            if b.get("contradiction"):
                f_txt.write("⚠ CONTRADICTION DETECTED\n")
            f_txt.write("\n")

    # .svg
    dot = graphviz.Digraph(comment="Diagnostic Phase Forks", format="svg")
    dot.attr(rankdir='LR')
    for b in branches:
        label = f"{b['branch']} ({b['phase']})\n" + "\n".join(f"• {s['expr']}" for s in b['steps'])
        label += f"\n• score: {b['meta']['confidence_score']}"
        label += f"\n• status: {b['meta']['resolution_status']}"
        if b['meta']['probes']:
            label += f"\n• probe: {', '.join(b['meta']['probes'][:2])}"
        dot.node(b["branch"], label, shape="box")
    if any(b["branch"] == "main_1" for b in branches):
        dot.edge("main", "main_1", label="contradiction fork")
    if any(b["branch"] == "main_2" for b in branches):
        dot.edge("main", "main_2", label="modal simulation")
    dot.render(os.path.join(output_dir, f"diagnostic_output_{timestamp}.svg"), cleanup=True)

if __name__ == "__main__":
    symptoms = [Atom("Fever", ["x"]), Atom("Headache", ["x"])]
    memory = [Not(Atom("VirusDetected", ["x"]))]
    axioms = [
        Axiom(And(Atom("Fever", ["x"]), Atom("Headache", ["x"])), Atom("VirusDetected", ["x"])),
        Axiom(Atom("Fever", ["x"]), Atom("PossibleTumor", ["x"])),
        Axiom(Atom("Headache", ["x"]), Atom("AllergyDetected", ["x"]))
    ]

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(base_dir, "cpee_output")

    result = run_recursive_diagnostic(symptoms, memory, axioms, branch="main", phase="ϕ₀")
    branches = result["branches"]

    export_diagnostic_output(branches, output_dir, timestamp)

    for b in branches:
        print(f"--- Branch: {b['branch']} | Phase: {b['phase']} ---")
        for step in b["steps"]:
            print(f"  ➤ {step['expr']}")
        print("  Meta:")
        for k, v in b["meta"].items():
            print(f"    {k}: {v}")
        if b.get("contradiction"):
            print("  ⚠ CONTRADICTION DETECTED")
