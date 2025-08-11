from __future__ import annotations
import json
from pathlib import Path
import importlib
from src.engine import Pipeline

def _resolve_prov(res: dict, log_name: str) -> list[dict]:
    p = Path(res["log_json"]).with_suffix(".prov.jsonl")
    lines = []
    with p.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                lines.append(json.loads(line))
    return lines

def test_legal_counterfactual_hook(monkeypatch, tmp_path):
    import src.engine.pipeline as pl
    # ensure we patch the module Pipeline reads hooks from
    called = {}
    def fake_cf(x: str):
        called["arg"] = x
        return {"flag": "cf-ok"}
    monkeypatch.setattr(pl, "cf_analyze", fake_cf, raising=False)
    importlib.reload(pl)  # reload so the patched symbol is used

    p = Pipeline(log_name="p14_cf", domain="legal", enable_provenance=True, session="t")
    res = p.run("1 IMPLIES 0")  # prenorm -> "1 -> 0"
    prov = _resolve_prov(res, "p14_cf")
    detect = [e for e in prov if e.get("kind") == "detect"][-1]
    enr = detect["details"]["enrichment"]
    assert enr.get("counterfactual") == {"flag": "cf-ok"}
    assert called["arg"] == "1 -> 0"

def test_medical_divergence_and_ner_hooks(monkeypatch, tmp_path):
    import src.engine.pipeline as pl
    monkeypatch.setattr(pl, "dm_classify", lambda s: "hi-risk", raising=False)
    monkeypatch.setattr(pl, "ner_extract", lambda s: [{"text": "1"}], raising=False)
    importlib.reload(pl)

    p = Pipeline(log_name="p14_med_hooks", domain="medical", enable_provenance=True, session="t")
    res = p.run("1 -> 0")
    prov = _resolve_prov(res, "p14_med_hooks")
    detect = [e for e in prov if e.get("kind") == "detect"][-1]
    enr = detect["details"]["enrichment"]
    assert enr.get("risk") == "hi-risk"
    assert isinstance(enr.get("entities"), list) and enr["entities"]
