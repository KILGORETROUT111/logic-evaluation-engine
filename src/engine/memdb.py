# src/engine/memdb.py
from __future__ import annotations
import json
import csv
from pathlib import Path
from typing import Optional, Dict, List
from datetime import datetime, timezone
# at top of memdb.py
from typing import Optional, Dict
from datetime import datetime, UTC

# Storage locations
BASE = Path("data") / "memdb"
BASE.mkdir(parents=True, exist_ok=True)
FILE_UNIFIED = BASE / "memdb.jsonl"         # all records (patient + case)
FILE_PATIENT = BASE / "patient_history.jsonl"
FILE_CASE = BASE / "case_history.jsonl"

# In-memory cache (loaded on import)
_store: List[Dict] = []


def _utcnow_iso() -> str:
    return datetime.now(UTC).isoformat() + "Z"


def _load_file(path: Path) -> List[Dict]:
    if not path.exists():
        return []
    rows: List[Dict] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except Exception:
                # skip malformed lines
                continue
    return rows


def _append_jsonl(path: Path, rec: Dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def _load_all() -> None:
    """Load unified jsonl into in-memory store."""
    global _store
    _store = _load_file(FILE_UNIFIED)


# Load on import
_load_all()


def store_entry(*args,
    patient_id: Optional[str] = None,
    case_id: Optional[str] = None,
    domain: Optional[str] = None,
    final_phase: Optional[str] = None,
    time_to_mem_ms: Optional[float] = None,
    session: Optional[str] = None,
    run_id: Optional[str] = None,
    ts_end: Optional[str] = None,
    jam: Optional[Dict] = None,
) -> Dict:
    """
    Append a record to the unified memdb and appropriate secondary files.
    Supports both positional (patient_id, case_id, domain, final_phase)
    and keyword arguments.
    """
    # Back-compat for positional calls
    if args:
        if len(args) > 4:
            raise TypeError("store_entry() accepts at most 4 positional args: patient_id, case_id, domain, final_phase")
        # only fill if not already provided via keywords
        if len(args) >= 1 and patient_id is None: patient_id = args[0]
        if len(args) >= 2 and case_id   is None: case_id   = args[1]
        if len(args) >= 3 and domain    is None: domain    = args[2]
        if len(args) >= 4 and final_phase is None: final_phase = args[3]

    rec = {
        "run_id": run_id,
        "session": session,
        "patient_id": patient_id,
        "case_id": case_id,
        "domain": domain,
        "final_phase": final_phase,
        "time_to_mem_ms": time_to_mem_ms,
        "ts_end": ts_end or _utcnow_iso(),
        "ts_written": _utcnow_iso(),
    }
    if jam:
        rec["jam"] = jam

    _store.append(rec)

    _append_jsonl(FILE_UNIFIED, rec)
    if patient_id:
        _append_jsonl(FILE_PATIENT, rec)
    if case_id:
        _append_jsonl(FILE_CASE, rec)

    return rec

    # Update in-memory
    _store.append(rec)

    # Persist to files
    _append_jsonl(FILE_UNIFIED, rec)
    if patient_id:
        _append_jsonl(FILE_PATIENT, rec)
    if case_id:
        _append_jsonl(FILE_CASE, rec)

    return rec


def append_patient_history(patient_id: str, run_summary: Dict) -> None:
    # Back-compat with earlier pipeline calls
    store_entry(
        patient_id=patient_id,
        case_id=run_summary.get("case_id"),
        domain=run_summary.get("domain"),
        final_phase=run_summary.get("final_phase"),
        time_to_mem_ms=run_summary.get("time_to_mem_ms"),
        session=run_summary.get("session"),
        run_id=run_summary.get("run_id"),
        ts_end=run_summary.get("ts_end"),
        jam=run_summary.get("jam"),
    )


def append_case_history(case_id: str, run_summary: Dict) -> None:
    # Back-compat with earlier pipeline calls
    store_entry(
        patient_id=run_summary.get("patient_id"),
        case_id=case_id,
        domain=run_summary.get("domain"),
        final_phase=run_summary.get("final_phase"),
        time_to_mem_ms=run_summary.get("time_to_mem_ms"),
        session=run_summary.get("session"),
        run_id=run_summary.get("run_id"),
        ts_end=run_summary.get("ts_end"),
        jam=run_summary.get("jam"),
    )


def get_entries() -> List[Dict]:
    return list(_store)


def export_csv(path: str | Path = "data/analytics/memdb_export.csv") -> Path:
    # ensure latest persisted content is loaded
    _load_all()
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "run_id",
        "session",
        "patient_id",
        "case_id",
        "domain",
        "final_phase",
        "time_to_mem_ms",
        "ts_end",
        "ts_written",
        "jam",
    ]
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for rec in _store:
            row = dict(rec)
            # keep jam compact in CSV
            if isinstance(row.get("jam"), dict):
                row["jam"] = json.dumps(row["jam"], ensure_ascii=False)
            writer.writerow(row)
    return out


def write_patient_summary_md(patient_id: str) -> Path:
    # small helper for per-patient summaries (optional)
    path = BASE / f"patient_{patient_id}.md"
    entries = [r for r in _store if r.get("patient_id") == patient_id]
    entries.sort(key=lambda r: r.get("ts_end", ""))

    lines = [f"# Patient {patient_id} — History", ""]
    for r in entries:
        lines.append(
            f"- {r.get('ts_end','')} · phase=`{r.get('final_phase','?')}` "
            f"· domain=`{r.get('domain','?')}` "
            f"· time_to_mem_ms=`{r.get('time_to_mem_ms')}`"
        )
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def write_case_summary_md(case_id: str) -> Path:
    path = BASE / f"case_{case_id}.md"
    entries = [r for r in _store if r.get("case_id") == case_id]
    entries.sort(key=lambda r: r.get("ts_end", ""))

    lines = [f"# Case {case_id} — History", ""]
    for r in entries:
        lines.append(
            f"- {r.get('ts_end','')} · phase=`{r.get('final_phase','?')}` "
            f"· domain=`{r.get('domain','?')}` "
            f"· time_to_mem_ms=`{r.get('time_to_mem_ms')}`"
        )
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def report() -> None:
    # ensure we reflect persisted content
    _load_all()
    print("\n=== MEMDB Report ===")
    for rec in _store:
        pid = rec.get("patient_id")
        cid = rec.get("case_id")
        dom = rec.get("domain")
        ph = rec.get("final_phase")
        ts = rec.get("ts_end")
        print(f"[{ts}] Patient={pid} Case={cid} Domain={dom} FinalPhase={ph}")
    print(f"\nTotal Records: {len(_store)}")


if __name__ == "__main__":
    import sys
    cmd = sys.argv[1] if len(sys.argv) > 1 else "help"
    if cmd == "report":
        report()
    elif cmd == "export":
        out_path = export_csv()
        print(f"Exported to {out_path}")
    elif cmd == "patient":
        if len(sys.argv) < 3:
            print("Usage: python -m src.engine.memdb patient P001")
            sys.exit(1)
        p = sys.argv[2]
        write_patient_summary_md(p)
        print(f"Wrote {BASE / f'patient_{p}.md'}")
    elif cmd == "case":
        if len(sys.argv) < 3:
            print("Usage: python -m src.engine.memdb case C001")
            sys.exit(1)
        c = sys.argv[2]
        write_case_summary_md(c)
        print(f"Wrote {BASE / f'case_{c}.md'}")
    else:
        print("Usage: python -m src.engine.memdb [report|export|patient <id>|case <id>]")
