import sys
import json
from evaluation.recursive_diagnostic_engine import run_recursive_diagnosis_and_export

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python -m evaluation.diagnostic_phase_engine <input_json_path>")
    else:
        try:
            with open(sys.argv[1], "r", encoding="utf-8") as f:
                test_input = json.load(f)

            goal = test_input["goal"]
            facts = test_input["facts"]
            axioms = test_input["axioms"]

            print(f"Running diagnostic for: {test_input['meta']['title']}")
            print(f"Description: {test_input['meta'].get('description', '')}\n")

            run_recursive_diagnosis_and_export(goal, facts, axioms)

        except Exception as e:
            print(f"Error loading diagnostic input: {e}")
