import re

def evaluate_expression(expr, known_facts):
    """
    Evaluate a basic logical expression using known facts.
    Supports:
      - atomic forms like P(a), Q(b)
      - negation: ¬P(a)
      - disjunction: A ∨ B
    """

    expr = expr.replace(" ", "")

    # Handle disjunction
    if "∨" in expr:
        left, right = expr.split("∨", 1)
        left_val = evaluate_expression(left, known_facts)
        right_val = evaluate_expression(right, known_facts)
        return left_val or right_val

    # Handle negation
    if expr.startswith("¬"):
        inner = expr[1:]
        return inner not in known_facts

    # Atomic form
    return expr in known_facts

# Example usage
if __name__ == "__main__":
    facts = {"P(a)"}

    print("¬P(a):", evaluate_expression("¬P(a)", facts))     # False
    print("¬Q(a):", evaluate_expression("¬Q(a)", facts))     # True
    print("¬P(a) ∨ Q(a):", evaluate_expression("¬P(a) ∨ Q(a)", facts))  # False ∨ False = False
    facts.add("Q(a)")
    print("¬P(a) ∨ Q(a):", evaluate_expression("¬P(a) ∨ Q(a)", facts))  # False ∨ True = True
