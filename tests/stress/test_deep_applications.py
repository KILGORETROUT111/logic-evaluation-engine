import sys
import os
import pytest

# Ensure root directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from utils.alpha_rename import alpha_rename
from core.expressions import Lambda, Variable, Application, Literal, Substitution
from core.evaluation import evaluate_full
from core.states import State


def test_placeholder():
    assert True
