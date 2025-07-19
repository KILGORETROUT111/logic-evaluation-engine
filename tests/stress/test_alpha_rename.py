import sys
import os
import pytest

# Ensure root directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from utils.alpha_rename import alpha_rename
from core.expressions import Lambda, Variable
from core.states import State

def test_alpha_rename_avoids_collision():
    expr = Lambda("x", Variable("x"))
    renamed = alpha_rename(expr, {"x"})
    assert renamed.var != "x"
    assert isinstance(renamed.body, Variable)
