import os
import json
from datetime import datetime

class DiagnosticPhaseEvaluator:
    def __init__(self):
        self.trace = []
        self.goal = None
        self.facts = []
        self.axioms = []
        self.output_path = None

    def evaluate(self, goal, facts, axioms, meta=None):
        self.trace = [f"[ϕ₀] Evaluating goal: {goal}"]
        self.rotation_history = ["ϕ₀"]
        self.confidence_score = 65
        self.probes = ["Check for mitigating context"]
        self.result = {
            "trace": self.trace,
            "rotation_history": self.rotation_history,
            "confidence_score": self.confidence_score,
            "probes": self.probes
        }

    def get_diagnostic_output(self):
        return self.result


def run_recursive_diagnosis_and_export(goal, facts, axioms, meta=None):
    evaluator = DiagnosticPhaseEvaluator()
    evaluator.evaluate(goal, facts, axioms, meta or {})
    results = evaluator.get_diagnostic_output()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = os.path.abspath("evaluation/cpee_output")
    os.makedirs(output_dir, exist_ok=True)

    json_path = os.path.join(output_dir, f"diagnostic_trace_{timestamp}.json")
    txt_path = os.path.join(output_dir, f"diagnostic_trace_{timestamp}.txt")

    with open(json_path, "w", encoding="utf-8") as jf:
        json.dump(results, jf, indent=4, ensure_ascii=False)

    with open(txt_path, "w", encoding="utf-8") as tf:
        tf.write(f"Goal: {goal}\n")
        tf.write("Trace:\n")
        for entry in results.get("trace", []):
            tf.write(entry + "\n")
        tf.write(f"\nConfidence Score: {results.get('confidence_score', 'N/A')}\n")
        tf.write(f"Probes: {', '.join(results.get('probes', []))}\n")
        tf.write(f"Rotation History: {', '.join(results.get('rotation_history', []))}\n")

    print(f"Results saved to: {txt_path} and {json_path}")
    return results
