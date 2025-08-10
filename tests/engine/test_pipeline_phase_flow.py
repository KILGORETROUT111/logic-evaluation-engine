from src.engine import Pipeline

def test_alive_jam_mem_history_for_contradiction():
    pipe = Pipeline(log_name="phase7_test")
    res = pipe.run("p & ~p  # CONTRADICTION")
    assert res["state"]["phase"] == "MEM"
    phases = res["history"]["phases"]
    assert phases[:3] == ["ALIVE", "JAM", "MEM"] or phases[-3:] == ["ALIVE", "JAM", "MEM"]
