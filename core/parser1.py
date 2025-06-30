from core.expressions import Functor, Value, Var

def build(obj):
    print("🔍 Parsing:", obj)

    if isinstance(obj, list):
        if not obj:
            raise ValueError("Empty list cannot be parsed as a Functor")
        
        head = obj[0]
        args = obj[1:]

        # Recursively build children
        parsed_args = [build(arg) for arg in args]

        # Build Functor
        if isinstance(head, str):
            return Functor(head.upper(), parsed_args)
        elif isinstance(head, Functor):
            return Functor(head.name.upper(), parsed_args)
        else:
            raise TypeError(f"Invalid functor head: {head}")

    elif isinstance(obj, dict):
        if "value" in obj:
            return Value(obj["value"])
        else:
            raise ValueError(f"Unsupported dict format: {obj}")

    elif isinstance(obj, (int, float)):
        return Value(obj)

    elif isinstance(obj, str):
        if obj.isidentifier():
            return Var(obj)
        else:
            return Value(obj)

    else:
        raise TypeError(f"Unsupported expression type: {type(obj)}")

def parse_expression(obj):
    return build(obj)