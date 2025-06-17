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