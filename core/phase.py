# core/phase.py

from enum import Enum

class EventPhase(Enum):
    APPLICATION = "Application"
    LAMBDA = "Lambda"
    VARIABLE = "Variable"
    LITERAL = "Literal"
    SUBSTITUTION = "Substitution"
    DEFINE = "Define"
    MEMORY = "Memory"
    QUANTIFIER = "Quantifier"
    JAM = "Jam"
    ALIVE = "Alive"