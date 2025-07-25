def run_recursive_diagnosis_and_export(goal, facts, axioms, meta=None):
    from evaluation.recursive_diagnostic_engine import DiagnosticPhaseEvaluator
    from datetime import datetime
    import os
    import json

    evaluator = DiagnosticPhaseEvaluator()
    evaluator.evaluate(goal=goal, facts=facts, axioms=axioms, meta=meta or {})

    results = evaluator.get_diagnostic_output()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(base_dir, "cpee_output")
    os.makedirs(output_dir, exist_ok=True)

    json_path = os.path.join(output_dir, f"diagnostic_trace_{timestamp}.json")
    txt_path = os.path.join(output_dir, f"diagnostic_trace_{timestamp}.txt")

    with open(json_path, "w", encoding="utf-8") as jf:
        json.dump(results, jf, indent=4, ensure_ascii=False)

    with open(txt_path, "w", encoding="utf-8") as tf:
        for entry in results.get("trace", []):
            tf.write(entry + "\n")

    print(f"Results saved to: {txt_path} and {json_path}")
    return results
