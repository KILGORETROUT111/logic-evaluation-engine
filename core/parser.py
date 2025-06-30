from core.expressions import Functor, Value, Var

def build(obj):
    print("🔍 Parsing:", obj)

    if isinstance(obj, list):
        head = obj[0]
        args = obj[1:]
        parsed_args = [build(arg) for arg in args]
        return Functor(str(head).upper(), parsed_args)

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
        return Value(obj)

    else:
        raise ValueError(f"Unsupported expression type: {type(obj)}")

def parse_expression(obj):
    return build(obj)