from src.engine.evaluator import evaluate_expression

class DummyLog:
    def __init__(self): self.events=[]
    def event(self, k, v): self.events.append((k, v))

def test_evaluator_logs_jam_only_on_contradiction():
    # no jam case
    log = DummyLog()
    s1 = evaluate_expression("1 -> 1", logger=log)
    assert s1.phase.name == "ALIVE"
    assert not any(k=="jam" for k,_ in log.events)

    # jam case
    log2 = DummyLog()
    s2 = evaluate_expression("1 -> 0", logger=log2)
    assert s2.phase.name in ("JAM",)  # pipeline will carry to MEM
    assert any(k=="jam" for k,_ in log2.events)
