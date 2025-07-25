class DiagnosticPhaseEvaluator:
    def __init__(self):
        self.trace = []
        self.goal = None
        self.facts = []
        self.axioms = []
        self.output_path = None

    def add_initial_facts(self, facts):
        self.facts.extend(facts)

    def add_axioms(self, axioms):
        self.axioms.extend(axioms)

    def run(self, goal):
        self.goal = goal
        print(f"[ϕ₀] Running evaluation for goal: {goal}")
        print("➤ Loaded facts:", self.facts)
        print("➤ Loaded axioms:", self.axioms)
        print("➤ Diagnostic phase engine logic would execute here.")
        self.trace.append(f"Evaluated goal: {goal}")

    def export_results(self):
        import os, json
        from datetime import datetime

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = os.path.join(os.path.dirname(__file__), "cpee_output")
        os.makedirs(output_dir, exist_ok=True)

        txt_path = os.path.join(output_dir, f"diagnostic_trace_{timestamp}.txt")
        json_path = os.path.join(output_dir, f"diagnostic_trace_{timestamp}.json")

        with open(txt_path, "w", encoding="utf-8") as f:
            f.write("\n".join(self.trace))

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump({"goal": self.goal, "trace": self.trace}, f, indent=4)

        print(f"Results saved to: {txt_path} and {json_path}")

def run_recursive_diagnosis_and_export(goal, facts, axioms):
    manager = DiagnosticPhaseEvaluator()
    manager.add_initial_facts(facts)
    manager.add_axioms(axioms)
    manager.run(goal)
    manager.export_results()
