import re

def match(pattern, target):
    """
    Matches a symbolic pattern like 'Q(x)' to a target like 'Q(a)'
    Returns dict of substitutions if match is successful, else None.
    """

    # Extract function name and arguments
    def parse(expr):
        match = re.match(r"([¬A-Z]+)\((.*?)\)", expr.replace(" ", ""))
        if not match:
            return expr, []
        functor, args = match.groups()
        return functor, args.split(",")

    p_fun, p_args = parse(pattern)
    t_fun, t_args = parse(target)

    if p_fun != t_fun or len(p_args) != len(t_args):
        return None

    substitution = {}
    for p_arg, t_arg in zip(p_args, t_args):
        if p_arg == t_arg:
            continue
        elif re.fullmatch(r"[a-z]", p_arg):  # single-letter variable
            substitution[p_arg] = t_arg
        else:
            return None  # non-variable mismatch

    return substitution

# Example
if __name__ == "__main__":
    print("Match Q(x) to Q(a):", match("Q(x)", "Q(a)"))
    print("Match R(x,y) to R(a,b):", match("R(x, y)", "R(a, b)"))
    print("Match ¬P(x) to ¬P(a):", match("¬P(x)", "¬P(a)"))
    print("Fail Match Q(x) to R(a):", match("Q(x)", "R(a)"))
