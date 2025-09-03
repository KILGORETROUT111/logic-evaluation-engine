# Phase 9 (TMA) — Quick Runbook
# Usage (PowerShell): Right-click → Run with PowerShell, or execute line-by-line in an elevated PowerShell prompt.
# Adjust paths if your checkout differs.

# --- Repo root ---
Set-Location "C:\Users\Dell\Documents\LEE\logic-evaluation-engine"

# --- Activate venv (adjust if different) ---
if (Test-Path ".\.venv\Scripts\Activate.ps1") {
    . .\.venv\Scripts\Activate.ps1
} else {
    Write-Host "Virtualenv not found at .\.venv. Create one or adjust path." -ForegroundColor Yellow
}

# --- Ensure PYTHONPATH includes repo and src ---
$env:PYTHONPATH = "$pwd;$pwd\src"

# --- Sanity: show pipeline module location & CWD ---
python - <<'PY'
import os, importlib.util
spec = importlib.util.find_spec("src.engine.pipeline")
print("CWD:", os.getcwd())
print("Pipeline module spec:", spec)
try:
    import src.engine.pipeline as pl
    print("PIPELINE FILE:", pl.__file__)
except Exception as e:
    print("IMPORT ERROR:", e)
PY

# --- Full test sweep ---
pytest -q -rA

# --- Phase-9 tests only ---
pytest -q -rA tests\nlp\test_tma_smoke.py tests\engine\test_eval_tma_integration.py

# --- Quick provenance smoke ---
python - <<'PY'
from src.engine.pipeline import Pipeline
p = Pipeline(log_name='p9_probe', enable_provenance=True, session='t')
res = p.run('A would imply not B.')
print("log_json:", res.get('log_json'))
PY

# --- Inspect the most recent provenance log ---
$latestProv = Get-ChildItem "data\logs" -Filter *.prov.jsonl -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Desc | Select-Object -First 1
if ($null -ne $latestProv) {
    Write-Host "Latest provenance:" $latestProv.FullName -ForegroundColor Cyan
    Get-Content $latestProv.FullName | Select-Object -First 12
} else {
    Write-Host "No *.prov.jsonl files found under data\logs." -ForegroundColor Yellow
}

# --- Diff vs upstream (fetch first) ---
git fetch origin
git diff --name-only origin/v3.0..origin/phase9-tma

# --- Guardrail: remind about golden images ---
Write-Host "Reminder: Do NOT overwrite Phase 0–7 golden images. Keep tests deterministic." -ForegroundColor Magenta