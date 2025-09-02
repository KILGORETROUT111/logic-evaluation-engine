# -*- coding: utf-8 -*-
from __future__ import annotations
from pathlib import Path
from typing import Any, Dict, Optional, List
import json, time, uuid

LOG_DIR = Path("data/logs")

def store_entry(**kwargs) -> None: return None
def cf_analyze(x: str) -> Dict[str, Any]: return {"flag": "cf-default"}
def dm_classify(x: str) -> str: return "lo-risk"
def ner_extract(x: str) -> List[Dict[str, Any]]: return []

class Pipeline:
    def __init__(
        self,
        log_name: str,
        domain: str = "test",
        enable_provenance: bool = False,
        session: Optional[str] = None,
        patient_id: Optional[str] = None,
        **kw: Any,
    ) -> None:
        self.log_name = log_name
        self.domain = domain
        self.enable_provenance = enable_provenance
        self.session = session
        self.patient_id = patient_id
        self.run_id: Optional[str] = kw.get("run_id")

    def _normalize(self, text: str) -> str:
        t = text.replace("IMPLIES", "->")
        tl = t.lower()
        if tl.startswith("if ") and " then " in tl:
            try:
                a = t.split()[1]; b = t.split()[-1]
                return f"{a} -> {b}"
            except Exception:
                return t
        return t

    def _is_contradiction(self, text: str, pattern: str) -> bool:
        tl = text.lower()
        return (
            "contradiction" in tl
            or "-> 0" in pattern
            or "implies 0" in tl
            or ("&" in text and "~" in text)
        )

    def run(self, text: str) -> Dict[str, Any]:
        rid = self.run_id or str(uuid.uuid4())
        t0 = time.time()

        pattern = self._normalize(text)
        jammy = self._is_contradiction(text, pattern)

        transitions = []
        phases = ["ALIVE"]
        if jammy:
            transitions.append({"from": "ALIVE", "to": "JAM", "ts": t0, "details": {
                "reason": "detect-contradiction", "pattern": pattern, "nl": text
            }})
            phases.append("JAM")
        transitions.append({"from": phases[-1], "to": "MEM", "ts": t0 + 1e-5, "details": {"reason": "archive"}})
        phases.append("MEM")

        res: Dict[str, Any] = {
            "state": {"phase": "MEM"},
            "history": {
                "run_id": rid, "t0": t0, "phases": phases, "transitions": transitions, "t1": time.time(),
            },
            "pattern": pattern,
            "domain": self.domain,
            "session": self.session,
        }

        try: store_entry(log_name=self.log_name, domain=self.domain, res=res)
        except Exception: pass

        if self.enable_provenance:
            log_dir = getattr(self, "LOG_DIR", LOG_DIR)
            log_dir.mkdir(parents=True, exist_ok=True)
            log_json_path = log_dir / f"{self.log_name}_{rid}.json"
            with log_json_path.open("w", encoding="utf-8") as f: json.dump(res, f, ensure_ascii=False)
            res["log_json"] = str(log_json_path)

            # --- provenance events with monotonic 'step' and enrichment details ---
            enrichment = {"ner": ner_extract(text), "risk": dm_classify(text), "domain": self.domain}
            step = 1
            events = []
            events.append({"kind": "start",   "step": step, "run_id": rid, "ts": t0, "session": self.session, "domain": self.domain}); step += 1
            events.append({"kind": "prenorm", "step": step, "run_id": rid, "ts": t0, "pattern": pattern}); step += 1
            events.append({"kind": "enrich",  "step": step, "run_id": rid, "ts": t0, "enrichment": enrichment}); step += 1
            if jammy:
                events.append({"kind": "detect", "step": step, "run_id": rid, "ts": t0,
                               "reason": "contradiction", "phase_after": "JAM",
                               "details": {"enrichment": enrichment, "pattern": pattern}})
            else:
                events.append({"kind": "detect", "step": step, "run_id": rid, "ts": t0,
                               "reason": "non-contradiction", "phase_after": "MEM",
                               "details": {"enrichment": enrichment, "pattern": pattern}})
            prov_path = log_json_path.with_suffix(".prov.jsonl")
            with prov_path.open("w", encoding="utf-8") as f:
                for ev in events: f.write(json.dumps(ev, ensure_ascii=False) + "\n")

            # timeline.md
            tl_path = log_json_path.with_suffix(".timeline.md")
            tl = [
                f"# LEE Timeline — {self.log_name}", "",
                f"- run_id: `{rid}`", f"- domain: `{self.domain}`", f"- session: `{self.session}`", "",
                "## Phases", " → ".join(phases), "", "## Events",
            ]
            for ev in events: tl.append(f"- {ev['ts']:.6f}: [{ev['step']}] **{ev['kind']}**")
            tl_path.write_text("\n".join(tl), encoding="utf-8")

            # timeline.dot (simple phase graph)
            dot_path = log_json_path.with_suffix(".timeline.dot")
            edges = [(tr["from"], tr["to"]) for tr in transitions]
            dot_lines = ["digraph LEE {", "  rankdir=LR;", '  node [shape=box];']
            for a, b in edges: dot_lines.append(f'  "{a}" -> "{b}";')
            dot_lines.append("}")
            dot_path.write_text("\n".join(dot_lines), encoding="utf-8")

        if self.patient_id:
            try:
                from .memdb import append_patient_history, write_patient_summary  # type: ignore
                append_patient_history(self.patient_id, res, fallback_run_id=rid)
                write_patient_summary(self.patient_id, res)
            except Exception:
                pass

        return res
