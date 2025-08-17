# scripts/prov_utils.py
import json, time, os
from typing import Iterable, Optional, Dict, Any
from prov_util import append_prov


ISO = "%Y-%m-%dT%H:%M:%S%z"

def _now_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S%z", time.localtime())

def append_prov(
    path: str,
    event: str,
    payload: Dict[str, Any],
    exhaustibility_class: Optional[str] = None,  # "I" | "II" | "III"
    evidence: Optional[Iterable[str]] = None,
    reviewer: Optional[str] = None,
    context: Optional[Dict[str, Any]] = None,
) -> None:
    """
    Append a single provenance record as JSONL.
    - path: prov.jsonl output path
    - event: short tag e.g. "stress_index_run", "counterfactual_eval"
    - payload: core metrics/ids your pipeline already writes
    - exhaustibility_class: "I"|"II"|"III" (Basis5 taxonomy)
    - evidence: short strings like ["complexity_upper_bound","approx_algo_v1"]
    - reviewer: e.g. "WAP-IV" or a Git hash of the review commit
    - context: optional freeform dict (CLI args, dataset ids, etc.)
    """
    rec = {
        "ts": _now_iso(),
        "event": event,
        "payload": payload,
    }
    # New fields (only add if provided)
    if exhaustibility_class:
        rec["exhaustibility_class"] = exhaustibility_class
    if evidence:
        rec["evidence"] = list(evidence)
    if reviewer:
        rec["reviewer"] = reviewer
    if context:
        rec["context"] = context

    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
