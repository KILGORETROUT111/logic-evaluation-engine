class Expr: pass

class Value(Expr):
    def __init__(self, value): self.value = value
    def __repr__(self): return f"Value({self.value!r})"

class Var(Expr):
    def __init__(self, name): self.name = name
    def __repr__(self): return f"Var({self.name!r})"

class Functor(Expr):
    def __init__(self, name, children=None):
        self.name = name
        self.children = children if children else []
    def __repr__(self):
        return f"{self.name}({', '.join(repr(c) for c in self.children)})"
=======
class Functor:
    def __init__(self, name, args=None):
        self.name = name
        self.args = args if args else []

    def __repr__(self):
        args_repr = ", ".join(repr(a) for a in self.args)
        return f"{self.name}({args_repr})"

class Var:
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return f"Var('{self.name}')"

class Value:
    def __init__(self, val):
        self.val = val
    def __repr__(self):
        return f"Value({self.val})"
    79041d6 (Initial commit with CLI + SUB support)
