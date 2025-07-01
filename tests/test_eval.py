#This Test file is part of Logic Evaluation Engine.
#Logic Evaluation Engine is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
#Logic Evaluation Engine is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#You should have received a copy of the GNU General Public License along with Logic Evaluation Engine.
#If not, see <https://www.gnu.org/licenses/>.

#

import pytest
from core.parser import parse_expression
from core.evaluation import evaluate_full

def run_expr(json_obj):
    expr = parse_expression(json_obj)
    context = {"x": 1, "z": 2, "y": 99}
    state, trace = evaluate_full(expr, context)
    return str(state), {k: [str(vv) for vv in v] for k, v in trace.items()}

def test_basic_ex():
    state, trace = run_expr(["EX", "x", "JAM"])
    assert state == "State.ALIVE"
    assert "EX" in trace

def test_substitution():
    state, trace = run_expr(["SUB", "x", 42])
    assert state == "State.ALIVE"
    assert "BIND" in trace

def test_nested_sub_mem():
    expr = ["Root", ["SUB", "x", ["EX", "y", "JAM"]], ["Node", {"value": 3}, "MEM", "x"]]
    state, trace = run_expr(expr)
    assert state == "State.ALIVE"
    assert any(k in trace for k in ("MEM", "RESOLVE", "BIND"))

def test_counterfactual():
    state, trace = run_expr(["EEX", "x", "JAM"])
    assert state == "State.VAC"
    assert "EEX" in trace

def test_raw_value():
    state, trace = run_expr({"value": 7})
    assert state == "State.ALIVE"

def test_empty_input_error():
    with pytest.raises(ValueError):
        run_expr([])

def test_unknown_functor():
    state, trace = run_expr(["FOO", "x"])
    assert state in ["State.VAC", "State.ALIVE"]