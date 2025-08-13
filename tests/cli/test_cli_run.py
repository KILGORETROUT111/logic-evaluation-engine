import json, importlib, sys

def test_cli_run_basic(monkeypatch, capsys, tmp_path):
    # isolate logs + avoid real IO
    pl = importlib.import_module("src.engine.pipeline")
    monkeypatch.setattr(pl, "LOG_DIR", tmp_path / "logs", raising=False)
    monkeypatch.setattr(pl, "store_entry", lambda **k: None, raising=False)

    # run via main() with argv
    import src.cli as cli
    monkeypatch.setenv("PYTHONIOENCODING", "utf-8")
    argv = ["lee", "if A then B", "--domain", "legal"]
    monkeypatch.setattr(sys, "argv", argv)
    cli.main()

    out = capsys.readouterr().out.strip()
    data = json.loads(out)
    assert data["state"]["phase"] == "MEM"
    assert data["result"]["pattern"] == "A -> B"

def test_run_once_api(monkeypatch, tmp_path):
    pl = importlib.import_module("src.engine.pipeline")
    monkeypatch.setattr(pl, "LOG_DIR", tmp_path / "logs", raising=False)
    monkeypatch.setattr(pl, "store_entry", lambda **k: None, raising=False)

    from src.cli import run_once
    res = run_once("breach implies liability", domain="legal")
    assert res["result"]["pattern"] == "breach -> liability"
    assert res["state"]["phase"] == "MEM"
