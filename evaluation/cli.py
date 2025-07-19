import argparse
from evaluation.proof_engine import prove

def main():
    parser = argparse.ArgumentParser(description="Run a logic proof via LEE CLI")
    parser.add_argument("--goal", type=str, required=True, help="Goal expression (e.g., 'Q(a)')")
    parser.add_argument("--facts", type=str, required=True, help="Comma-separated known facts (e.g., 'P(a),R(b)')")
    parser.add_argument("--axioms", type=str, required=True, help="Comma-separated axioms (e.g., '¬P(x) ∨ Q(x)')")
    parser.add_argument("--export-json", type=str, help="Path to export JSON trace")
    parser.add_argument("--export-md", type=str, help="Path to export Markdown trace")

    args = parser.parse_args()

    goal = args.goal.strip()
    facts = [fact.strip() for fact in args.facts.split(",")]
    axioms = [ax.strip() for ax in args.axioms.split(",")]

    result = prove(
        goal,
        facts,
        axioms,
        log_json=bool(args.export_json),
        log_md=bool(args.export_md),
        log_path_json=args.export_json,
        log_path_md=args.export_md
    )

    print(f"Goal: {goal}")
    print(f"Result: {'✅ Proven' if result else '❌ Not Proven'}")

if __name__ == "__main__":
    main()
