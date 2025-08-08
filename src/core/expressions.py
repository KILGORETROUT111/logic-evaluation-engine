# src/core/expressions.py

from dataclasses import dataclass
from typing import Any, List, Optional, Union

# --- Core Expression Classes ---

@dataclass(frozen=True)
class Variable:
    name: str

    def __str__(self):
        return self.name

@dataclass(frozen=True)
class Lambda:
    param: Variable
    body: Any  # Can be another expression

    def __str__(self):
        return f"(\u03bb{self.param}. {self.body})"

@dataclass(frozen=True)
class Application:
    func: Any
    arg: Any

    def __str__(self):
        return f"({self.func} {self.arg})"

@dataclass(frozen=True)
class Quantifier:
    kind: str  # 'forall' or 'exists'
    var: Variable
    body: Any

    def __str__(self):
        symbol = '∀' if self.kind == 'forall' else '∃'
        return f"({symbol}{self.var}. {self.body})"

# --- Type Hint Alias ---
Expression = Union[Variable, Lambda, Application, Quantifier]
