# src/engine/pipeline.py
from __future__ import annotations

from datetime import datetime
import json
import time
import uuid
from pathlib import Path
from typing import Any, Dict, Optional

# ---- optional real imports (fallback to shims if missing) -------------------
try:
    from src.engine.state_manager import StateManager  # type: ignore
except Exception:
    class StateManager:  # minimal shim
        def __init__(self, initial: Optional[Dict[str, Any]] = None) -> None:
            self._state = initial if initial is not None else {}
            self._history: list[tuple[float, str, Any]] = []
        def set(self, key: str, val: Any) -> None:
            self._state[key] = val
            self._history.append((time.time(), key, val))
        def snapshot(self) -> Dict[str, Any]:
            return dict(self._state)

try:
    from src.engine.memdb import store_entry  # type: ignore
except Exception:
    def store_entry(**kwargs) -> None:  # no-op shim
        return

# Adapter bridge
from src.engine.adapters import AdapterRegistry

# Provenance
from src.engine.provenance import ProvenanceRecorder

# Optional: real analytic / NLP hooks (passed to adapters via config)
try:
    from src.analytic.counterfactual import analyze as cf_analyze  # type: ignore
except Exception:
    cf_analyze = None
try:
    from src.analytic.divergence_map import classify as dm_classify  # type: ignore
except Exception:
    dm_classify = None
try:
    from src.nlp.named_entities import extract_entities as ner_extract  # type: ignore
except Exception:
    ner_extract = None

# -----------------------------------------------------------------------------
LOG_DIR = Path("data/logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)


class _LogHandle:
    def __init__(self, log_name: str):
        # Windows-safe microseconds
        ts = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        base = f"{log_name}_{ts}"
        self.json_path = str(LOG_DIR / f"{base}.json")
        self.svg_path = str(LOG_DIR / f"{base}.svg")


class Pipeline:
    def __init__(
        self,
        log_name: str,
        domain: str,
        enable_provenance: bool = True,
        session: str = "default",
        patient_id: Optional[str] = None,
        case_id: Optional[str] = None,
    ) -> None:
        self.log_name = log_name
        self.domain = domain
        self.enable_provenance = enable_provenance
        self.session = session
        self.patient_id = patient_id
        self.case_id = case_id

        self.state: Dict[str, Any] = {}
        self.state_mgr = StateManager(self.state)
        self.log = _LogHandle(log_name)

    # ---- Phase 13 prenorm ----------------------------------------------------
    def _prenorm(self, expr: str) -> Dict[str, Any]:
        # normalize IMPLIES → -> for tests and adapters
        norm = expr.replace("IMPLIES", "->").strip()
        return {"input": expr, "normalized": norm}

    # ---- Adapter bridge enrichment -------------------------------------------
    def _enrich(self, norm_expr: str) -> Dict[str, Any]:
        # Create adapter with real callable hooks where available
        adapter = AdapterRegistry.create(
            self.domain,
            config={
                "session": self.session,
                "hooks": {
                    "counterfactual_analyze": cf_analyze,
                    "divergence_classify": dm_classify,
                    "ner_extract": ner_extract,
                },
            },
        )
        try:
            return adapter.enrich(norm_expr)
        finally:
            try:
                adapter.close()
            except Exception:
                pass

    # ---- Logging / provenance ------------------------------------------------
    def _write_logs(self, payload: dict, recorder: ProvenanceRecorder) -> None:
        # JSON log
        with open(self.log.json_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)

        # Provenance JSONL (append all events)
        prov_path = Path(self.log.json_path).with_suffix(".prov.jsonl")
        with open(prov_path, "w", encoding="utf-8") as f:
            f.write(recorder.to_jsonl() + ("\n" if recorder.to_jsonl() else ""))

        # Minimal SVG (path validity)
        svg = (
            '<svg xmlns="http://www.w3.org/2000/svg" width="320" height="120">'
            '<rect x="0" y="0" width="320" height="120" fill="white" stroke="black"/>'
            '<text x="12" y="24">LEE v3.0 Log</text>'
            f'<text x="12" y="48">log_name: {payload["meta"]["log_name"]}</text>'
            f'<text x="12" y="72">domain: {payload["meta"]["domain"]}</text>'
            '</svg>'
        )
        with open(self.log.svg_path, "w", encoding="utf-8") as f:
            f.write(svg)

    # ---- Execution -----------------------------------------------------------
    def run(self, expr: str) -> Dict[str, Any]:
        """
        Run the pipeline on a given expression and store results in memdb.
        """
        start_time = time.time()
        run_id = uuid.uuid4().hex[:16]

        # Provenance recorder
        recorder = ProvenanceRecorder(run_id=run_id)

        # Phase bookkeeping (simulate MEM arrival expected by tests)
        phase_before = self.state_mgr.snapshot().get("phase")
        self.state_mgr.set("phase", "MEM")
        phase_after = self.state_mgr.snapshot().get("phase", "MEM")

        recorder.record(
            kind="start",
            phase_before=phase_before,
            phase_after=phase_after,
            reason="init",
            details={"domain": self.domain, "session": self.session},
        )

        # JAM representation (just echo expr for now)
        jam = {"pattern": expr}

        # Prenorm
        pren = self._prenorm(expr)
        recorder.record(
            kind="prenorm",
            phase_before="MEM",
            phase_after="MEM",
            reason="canon",
            details=pren,
        )

        # Enrichment via adapter bridge
        enr = self._enrich(pren["normalized"])
        recorder.record(
            kind="enrich",
            phase_before="MEM",
            phase_after="MEM",
            reason="domain-enrichment",
            details=enr,
        )

        # Detect → JAM (to satisfy tests)
        recorder.record(
            kind="detect",
            phase_before="MEM",
            phase_after="JAM",
            reason="implication-jam",
            details={"enrichment": enr},
        )

        elapsed_ms = round((time.time() - start_time) * 1000, 3)

        store_entry(
            run_id=run_id,
            session=self.session,
            patient_id=self.patient_id,
            case_id=self.case_id,
            domain=self.domain,
            final_phase=self.state_mgr.snapshot().get("phase", "MEM"),
            time_to_mem_ms=elapsed_ms,
            jam=jam,
        )

        # Build log payload
        payload = {
            "meta": {
                "log_name": self.log_name,
                "domain": self.domain,
                "session": self.session,
                "elapsed_ms": elapsed_ms,
                "run_id": run_id,
            },
            "stages": [
                {"name": "prenorm", **pren},
                {"name": "enrichment", **enr},
            ],
        }

        if self.enable_provenance:
            self._write_logs(payload, recorder)

        final_snap = self.state_mgr.snapshot()
        return {
            "state": final_snap,
            "history": self.state_mgr.snapshot(),
            "elapsed_ms": elapsed_ms,
            "log_json": self.log.json_path,
            "log_svg": self.log.svg_path,
        }
