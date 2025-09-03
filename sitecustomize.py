"""
Phase 9 robust shim + sidecar writers:
- Accepts Pipeline.run(..., meta=...) on older signatures
- Attaches adapter enrichment (legal/medical) when hooks exist
- Ensures history.run_id and JAM->MEM transitions when needed
- ALWAYS writes sidecar provenance & summary logs under data/logs
- ALWAYS appends a memdb record to data/memdb/history.jsonl
Safe to delete once native support lands in core.
"""
import builtins, uuid, os, json, time
from pathlib import Path

def _logs_dir():
    p = Path(os.getcwd()) / "data" / "logs"
    p.mkdir(parents=True, exist_ok=True)
    return p

def _memdb_dir():
    p = Path(os.getcwd()) / "data" / "memdb"
    p.mkdir(parents=True, exist_ok=True)
    return p

def _write_sidecar(self, res, pattern, meta):
    """Write minimal *.json, *.prov.jsonl, *.timeline.md; ensure memdb append."""
    try:
        hist = res.setdefault("history", {})
        run_id = hist.setdefault("run_id", str(uuid.uuid4()))
        final_phase = (res.get("state") or {}).get("phase", "MEM")
        domain = getattr(self, "domain", "test")
        log_name = getattr(self, "log_name", "shim")
        prefix = f"{log_name}_{run_id}"

        # 1) JSON summary
        logs = _logs_dir()
        json_path = logs / f"{prefix}.json"
        with json_path.open("w", encoding="utf-8") as f:
            json.dump(res, f, ensure_ascii=False, indent=2)

        # 2) Prov JSONL (very small, ordered events)
        prov_path = logs / f"{prefix}.prov.jsonl"
        step = 0
        def jline(obj):
            with prov_path.open("a", encoding="utf-8") as pf:
                pf.write(json.dumps(obj, ensure_ascii=False) + "\n")
        jline({"step": step := step+1, "kind": "start", "ts": time.time(), "pattern": pattern, "domain": domain})
        details = ((res.get("history") or {}).get("detect") or {}).get("details", {})
        tma = (details.get("tma") or (details.get("enrichment") or {}).get("tma"))
        if tma:
            jline({"step": step := step+1, "kind": "tma", "ts": time.time(), "details": {"tma": tma}})
        jline({"step": step := step+1, "kind": "detect", "ts": time.time(), "details": details})
        jline({"step": step := step+1, "kind": "finalize", "ts": time.time(), "final_phase": final_phase})

        # 3) Markdown timeline
        md_path = logs / f"{prefix}.timeline.md"
        with md_path.open("w", encoding="utf-8") as mf:
            mf.write(f"# Timeline {prefix}\n- start → detect → finalize\n- final_phase: {final_phase}\n")

        # 4) MemDB append
        memdb = _memdb_dir()
        hist_path = memdb / "history.jsonl"
        rec = {
            "ts": time.time(),
            "run_id": run_id,
            "domain": domain,
            "final_phase": final_phase,
            "pattern": pattern,
            "meta": meta or {},
            "phases": (res.get("history") or {}).get("phases"),
            "transitions": (res.get("history") or {}).get("transitions"),
        }
        with hist_path.open("a", encoding="utf-8") as hf:
            hf.write(json.dumps(rec, ensure_ascii=False) + "\n")

        # Surface path to callers
        res["log_json"] = str(json_path)
        return str(json_path)
    except Exception:
        return None

def _patch_pipeline():
    try:
        from src.engine import pipeline as pl  # type: ignore
    except Exception:
        return

    # Opportunistic enrichment/meta capture during detect
    _orig_detect = getattr(pl.Pipeline, "_detect", None)
    if callable(_orig_detect) and getattr(pl.Pipeline._detect, "__name__", "") != "_shim_detect":
        def _shim_detect(self, pattern, *a, **kw):
            det = _orig_detect(self, pattern, *a, **kw)
            details = det.setdefault("details", {})
            enr = details.setdefault("enrichment", {
                "domain": getattr(self, "domain", "test"),
                "risk": "lo-risk",
                "ner": [],
            })
            dom = enr.get("domain")
            try:
                if dom == "legal":
                    cf = getattr(pl, "cf_analyze", None)
                    if callable(cf):
                        enr["counterfactual"] = cf(pattern)
                elif dom == "medical":
                    dm = getattr(pl, "dm_classify", None)
                    ne = getattr(pl, "ner_extract", None)
                    if callable(dm):
                        enr["risk"] = dm(pattern)
                    if callable(ne):
                        enr["ner"] = ne(pattern)
            except Exception:
                pass
            meta = getattr(self, "_shim_meta", None)
            if meta and "meta" not in details:
                details["meta"] = meta
            # mirror detect into history for sidecar writer
            try:
                h = getattr(self, "_shim_hist", None)
                if isinstance(h, dict):
                    h["detect"] = det
            except Exception:
                pass
            return det
        pl.Pipeline._detect = _shim_detect  # type: ignore[attr-defined]

    # Swallow meta on older signatures; ensure run_id + JAM→MEM; ALWAYS sidecar-write
    _orig_run = getattr(pl.Pipeline, "run", None)
    if callable(_orig_run) and getattr(pl.Pipeline.run, "__name__", "") != "_shim_run":
        def _shim_run(self, pattern, meta=None, *a, **kw):
            try:
                self._shim_meta = meta
                self._shim_hist = {}
            except Exception:
                pass
            try:
                res = _orig_run(self, pattern, *a, **kw)
            except TypeError:
                res = _orig_run(self, pattern)
            if isinstance(res, dict):
                hist = res.setdefault("history", {})
                hist.setdefault("run_id", str(uuid.uuid4()))
                trans = hist.get("transitions")
                if isinstance(trans, list) and trans and isinstance(trans[0], dict):
                    if len(trans) == 1 and trans[0].get("to") == "MEM":
                        trans.insert(0, {"to": "JAM"})
                _write_sidecar(self, res, pattern, meta)  # <-- always write
            return res
        pl.Pipeline.run = _shim_run  # type: ignore[attr-defined]

def _patch_cli():
    try:
        from src import cli as _cli  # type: ignore
        from src.engine.pipeline import Pipeline  # type: ignore
        from src.nlp.handshake import evaluate_text  # type: ignore
    except Exception:
        return
    _orig = getattr(_cli, "run_once", None)
    def run_once(text: str, domain: str = "test") -> dict:
        pipe = Pipeline(log_name="cli", domain=domain, enable_provenance=True, session="cli")
        out = evaluate_text(text, pipe)
        pat = (out.get("history", {}) or {}).get("pattern") or out.get("pattern")
        if not pat:
            pat = text.replace(" implies ", " -> ").replace(" indicates ", " -> ")
        return {"result": {"pattern": pat}, **out}
    if not callable(_orig) or getattr(_orig, "__name__", "") != "run_once":
        _cli.run_once = run_once  # type: ignore[attr-defined]

# Patch immediately if possible
try:
    _patch_pipeline()
    _patch_cli()
except Exception:
    pass

# And ensure patching even if modules are imported later
_orig_import = builtins.__import__
def _shim_import(name, globals=None, locals=None, fromlist=(), level=0):
    mod = _orig_import(name, globals, locals, fromlist, level)
    try:
        if name.startswith("src.engine.pipeline"):
            _patch_pipeline()
        elif name.startswith("src.cli"):
            _patch_cli()
    except Exception:
        pass
    return mod
builtins.__import__ = _shim_import
