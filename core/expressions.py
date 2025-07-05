class Expression:
    def walk(self):
        yield self

class Variable(Expression):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

class Literal(Expression):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return str(self.value)

class Lambda(Expression):
    def __init__(self, var, body):
        self.var = var
        self.body = body

    def __repr__(self):
        return f"(λ{self.var}.{self.body})"

class Application(Expression):
    def __init__(self, func, arg):
        self.func = func
        self.arg = arg

    def __repr__(self):
        return f"({self.func} {self.arg})"

class Substitution(Expression):
    def __init__(self, var, value, body):
        self.var = var
        self.value = value
        self.body = body

    def __repr__(self):
        return f"[{self.body} ⟶ {self.var} := {self.value}]"

class Memory(Expression):
    def __init__(self, var):
        self.var = var

    def __repr__(self):
        return f"M[{self.var}]"

class Quantifier(Expression):
    def __init__(self, var, body, universal=True):
        self.var = var
        self.body = body
        self.universal = universal  # True = ∀, False = ∃

    def __repr__(self):
        q = "∀" if self.universal else "∃"
        return f"({q}{self.var}.{self.body})"

class Define(Expression):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return f"(DEFINE {self.name} = {self.value})"
    
class BinaryOp:
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def __repr__(self):
        return f"({self.left} {self.op} {self.right})"


class IfThenElse:
    def __init__(self, condition, then_branch, else_branch):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

    def __repr__(self):
        return f"(if {self.condition} then {self.then_branch} else {self.else_branch})"
