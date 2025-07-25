# logic_truth.py

def evaluate_truth(expr, facts):
    """
    Basic truth evaluator.
    For now, just check if the expression is in known facts.
    """
    return expr in facts
