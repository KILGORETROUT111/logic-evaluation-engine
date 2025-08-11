# src/engine/pipeline.py
from __future__ import annotations

from datetime import datetime
import json
import time
import uuid
from pathlib import Path
from typing import Any, Dict, Optional

# --- State manager (handle old/new ctor signatures & missing 'set') ----------
try:
    from src.engine.state_manager import StateManager  # type: ignore
except Exception:
    class StateManager:  # minimal shim (won't be used if real class exists)
        def __init__(self) -> None:
            self._state = {}
            self._history: list[tuple[float, str, Any]] = []
        def snapshot(self) -> Dict[str, Any]:
            return dict(self._state)

# --- memdb -------------------------------------------------------------------
try:
    from src.engine.memdb import store_entry  # type: ignore
except Exception:
    def store_entry(**kwargs) -> None:
        return

# --- adapters & provenance ----------------------------------------------------
from src.engine.adapters import AdapterRegistry
from src.engine.provenance import ProvenanceRecorder

# --- optional real hooks for adapters ----------------------------------------
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

LOG_DIR = Path("data/logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)


class _LogHandle:
    def __init__(self, log_name: str):
        ts = datetime.now().strftime("%Y%m%d_%H%M%S_%f")  # Windows-safe
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

        # COMPAT: StateManager may accept (initial_dict) OR no args
        try:
            self.state_mgr = StateManager(self.state)  # new API
        except TypeError:
            self.state_mgr = StateManager()            # old API
            # keep self.state in sync if snapshot returns a dict
            try:
                snap = self.state_mgr.snapshot()
                if isinstance(snap, dict):
                    self.state = snap
            except Exception:
                pass

        self.log = _LogHandle(log_name)

    # Phase 13 prenorm
    def _prenorm(self, expr: str) -> Dict[str, Any]:
        norm = expr.replace("IMPLIES", "->").strip()
        return {"input": expr, "normalized": norm}

    # Adapter enrichment
    def _enrich(self, norm_expr: str) -> Dict[str, Any]:
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

    def _write_logs(self, payload: dict, recorder: ProvenanceRecorder) -> None:
        with open(self.log.json_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)

        prov_path = Path(self.log.json_path).with_suffix(".prov.jsonl")
        jl = recorder.to_jsonl()
        with open(prov_path, "w", encoding="utf-8") as f:
            if jl:
                f.write(jl + "\n")

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

    def _safe_snapshot(self) -> Dict[str, Any]:
        try:
            snap = self.state_mgr.snapshot()
            return dict(snap) if isinstance(snap, dict) else {}
        except Exception:
            return {}

    # Execute
    def run(self, expr: str) -> Dict[str, Any]:
        start_time = time.time()
        run_id = uuid.uuid4().hex[:16]
        recorder = ProvenanceRecorder(run_id=run_id)

        # simulate MEM arrival
        phase_before = self._safe_snapshot().get("phase")
        # Prefer manager.set, but tolerate managers without it
        try:
            setter = getattr(self.state_mgr, "set", None)
            if callable(setter):
                setter("phase", "MEM")
            else:
                # Fall back to directly updating our public state dict
                self.state["phase"] = "MEM"
        except Exception:
            self.state["phase"] = "MEM"

        snap_after = self._safe_snapshot()
        if "phase" not in snap_after and "phase" in self.state:
            snap_after = dict(snap_after)
            snap_after["phase"] = self.state["phase"]

        recorder.record(
            kind="start",
            phase_before=phase_before,
            phase_after=snap_after.get("phase", "MEM"),
            reason="init",
            details={"domain": self.domain, "session": self.session},
        )

        jam = {"pattern": expr}

        pren = self._prenorm(expr)
        recorder.record(
            kind="prenorm",
            phase_before="MEM",
            phase_after="MEM",
            reason="canon",
            details=pren,
        )

        enr = self._enrich(pren["normalized"])
        recorder.record(
            kind="enrich",
            phase_before="MEM",
            phase_after="MEM",
            reason="domain-enrichment",
            details=enr,
        )

        recorder.record(
            kind="detect",
            phase_before="MEM",
            phase_after="JAM",
            reason="implication-jam",
            details={"enrichment": enr},
        )

        elapsed_ms = round((time.time() - start_time) * 1000, 3)

        final_snap = self._safe_snapshot()
        if "phase" not in final_snap and "phase" in self.state:
            final_snap = dict(final_snap)
            final_snap["phase"] = self.state["phase"]
        final_phase = final_snap.get("phase", "MEM")

        store_entry(
            run_id=run_id,
            session=self.session,
            patient_id=self.patient_id,
            case_id=self.case_id,
            domain=self.domain,
            final_phase=final_phase,
            time_to_mem_ms=elapsed_ms,
            jam=jam,
        )

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

        return {
            "state": final_snap,
            "history": final_snap,
            "elapsed_ms": elapsed_ms,
            "log_json": self.log.json_path,
            "log_svg": self.log.svg_path,
        }
