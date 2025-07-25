class ScopedContext:
    def __init__(self, parent=None):
        self.bindings = {}
        self.parent = parent

    def bind(self, var, value):
        self.bindings[var] = value

    def lookup(self, var):
        if var in self.bindings:
            return self.bindings[var]
        elif self.parent:
            return self.parent.lookup(var)
        else:
            raise NameError(f"Variable '{var}' not found in any scope")

    def extend(self):
        return ScopedContext(parent=self)

    def __repr__(self):
        return f"ScopedContext({self.bindings})"
