import argparse
from diagnostic_phase_engine import DiagnosticPhaseEvaluator

def main():
    parser = argparse.ArgumentParser(description="LEE Diagnostic Phase Engine CLI")
    parser.add_argument("--input", required=True, help="Comma-separated list of symptoms (e.g., 'fever,cough,fatigue')")
    args = parser.parse_args()

    symptoms = [s.strip() for s in args.input.split(",")]
    engine = DiagnosticPhaseEvaluator()
    result = engine.evaluate(symptoms)

    print("\n🧠 LEE Diagnostic Phase Engine v1.1")
    print(f"Input symptoms: {', '.join(symptoms)}\n")
    print(f"Phase-State Resolved: {result['phase_zone']}")
    print(f"→ Condition Likely: {result['likely_condition']}")
    print(f"→ Error pathways: {result['error_pathways']}")
    print(f"→ Additional probe recommended: {result['recommendations']}\n")
    print("Trace Summary:")
    for line in result["trace"]:
        print(f"✔ {line}")
    print(f"\nConfidence: {result['confidence']}%")

if __name__ == "__main__":
    main()
