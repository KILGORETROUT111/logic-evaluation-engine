#This file is part of Logic Evaluation Engine.
#Logic Evaluation Engine is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
#Logic Evaluation Engine is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#You should have received a copy of the GNU General Public License along with Logic Evaluation Engine.
#If not, see <https://www.gnu.org/licenses/>.

#

import sys
import os
# Tell Python how to find core modules
CURRENT = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.abspath(os.path.join(CURRENT, ".."))
sys.path.insert(0, PARENT)

from core.expressions import Functor, Var
from core.evaluation import evaluate_full
import streamlit as st
import json

st.set_page_config(page_title="Logic Engine Demo", layout="wide")
st.title("🧠 Logic Evaluation Engine")

expr_input = st.text_input("Enter expression (EX(x, JAM()), MEM, etc):", "EX(x, JAM())")
context_input = st.text_area("Context (Python dict):", "{'x': 1, 'z': 2}")

def parse_expr(expr_str):
    expr_str = expr_str.strip().replace(" ", "").upper()
    if expr_str == "EX(X,JAM())":
        return Functor("EX", [Var("x"), Functor("JAM")])
    elif expr_str == "MEM":
        return Functor("MEM")
    raise ValueError(f"Unsupported: {expr_str}")

if st.button("Evaluate"):
    try:
        expr = parse_expr(expr_input)
        context = eval(context_input)
        state, trace = evaluate_full(expr, context)

        st.success(f"Final state: {state}")
        st.subheader("Trace Output:")
        st.json({k: [str(vv) for vv in v] for k, v in trace.items()})

        st.download_button("Download Trace as JSON", json.dumps(
            {k: [str(vv) for vv in v] for k, v in trace.items()}, indent=2),
            file_name="trace_output.json", mime="application/json")
    except Exception as e:
        st.error(str(e))

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import json
from core.parser import parse_expression
from core.evaluation import evaluate_full
from core.visualize import visualize_trace_graph

st.set_page_config(page_title="Logic Evaluation Engine", layout="wide")

st.title("Logic Evaluation Engine")
st.markdown("""
Enter an expression in JSON format:
- Example: `["Root", ["EX", "x", "JAM"], ["Node", {"value": 3}, "MEM", "z"]]`
- Or simpler: `["EX", "x", "JAM"]`
""")

expr_str = st.text_area("Expression Input", height=200)

if expr_str:
    try:
        expr_str = expr_str.replace("'", '"')
        raw = json.loads(expr_str)
        expr = parse_expression(raw)
        st.success(f"✔️ Parsed Expression:\n`{expr}`")

        context = {"x": 1, "z": 2, "y": 7}
        state, trace = evaluate_full(expr, context)

        st.subheader("Evaluation Results")
        st.success(f"✅ Final state: `{state}`")

        st.subheader("Trace Output")
        st.json({k: [str(vv) for vv in v] for k, v in trace.items()})

        if st.button("📈 Generate Diagram"):
            result = visualize_trace_graph(trace, context=context, final_state=state)
            st.success("Diagram and manifest saved!")
            st.markdown(f"📁 SVG Path: `{result['svg_path']}`")
            st.markdown(f"📁 PNG Path: `{result['png_path']}`")
            st.markdown(f"📁 Manifest: `{result['manifest_path']}`")

    except Exception as e:
        st.error(f"❌ Parser/Evaluator error: {e}")
