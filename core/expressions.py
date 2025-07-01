#This file is part of Logic Evaluation Engine.
#Logic Evaluation Engine is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
#Logic Evaluation Engine is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#You should have received a copy of the GNU General Public License along with Logic Evaluation Engine.
#If not, see <https://www.gnu.org/licenses/>.

#

from enum import Enum

class State(Enum):
    ALIVE = "Alive"
    JAM = "Jam"
    VAC = "Vac"
    MEM = "Mem"
    UNBOUND = "Unbound"

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
