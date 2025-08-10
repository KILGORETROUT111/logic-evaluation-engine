# src/engine/analytics.py
from __future__ import annotations
import json
from pathlib import Path
from typing import Dict, Iterable, Optional
from datetime import datetime
from datetime import datetime, UTC
from html import escape


ROOT = Path(__file__).resolve().parents[2]  # project root
LOG_DIR = ROOT / "data" / "logs"
ANALYTICS_DIR = ROOT / "data" / "analytics"
HISTORY = ANALYTICS_DIR / "history.jsonl"
SUMMARY_MD = ANALYTICS_DIR / "summary.md"


# ---------- util ----------

def _ensure_dirs() -> None:
    ANALYTICS_DIR.mkdir(parents=True, exist_ok=True)

def _read_event_log(json_path: str | Path) -> Dict:
    p = Path(json_path)
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)

def _iter_history() -> Iterable[Dict]:
    if not HISTORY.exists():
        return []
    with HISTORY.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except Exception:
                # skip bad lines but don’t die
                continue


# ---------- public API used by Pipeline ----------

def record_run_summary(*, run_id: str, log_json_path: str, session: Optional[str]) -> None:
    """
    Append one JSONL record summarizing a single pipeline run.
    Robust to missing fields; never raises out.
    """
    _ensure_dirs()
    try:
        data = _read_event_log(log_json_path)
        events = data.get("events", [])
        # extract timestamps
        ts_start = None
        ts_end = None
        final_phase = None
        time_to_mem_ms = None

        for ev in events:
            if ev.get("type") == "start":
                ts_start = ev.get("ts")
            if ev.get("type") == "end":
                ts_end = ev.get("ts")
                final_phase = (ev.get("data") or {}).get("phase")
            if ev.get("type") == "mem":
                t = (ev.get("data") or {}).get("time_to_mem_ms")
                if isinstance(t, (int, float)):
                    time_to_mem_ms = float(t)

        rec = {
            "run_id": run_id,
            "session": session,
            "log_json": str(log_json_path),
            "ts_start": ts_start,
            "ts_end": ts_end,
            "final_phase": final_phase,
            "time_to_mem_ms": time_to_mem_ms,
            "recorded_at": datetime.now(UTC).isoformat(),
    }

        with HISTORY.open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    except Exception:
        # never crash the caller
        return


def aggregate() -> Dict:
    """
    Build a simple aggregate from history.jsonl.
    """
    by_phase: Dict[str, int] = {}
    by_session: Dict[str, int] = {}
    total = 0
    jam = 0
    last_runs: list[Dict] = []

    for rec in _iter_history():
        total += 1
        fp = rec.get("final_phase") or "UNKNOWN"
        by_phase[fp] = by_phase.get(fp, 0) + 1
        sess = rec.get("session") or "default"
        by_session[sess] = by_session.get(sess, 0) + 1
        if fp == "JAM":
            jam += 1
        last_runs.append(rec)

    # keep only last 10 in display order (most recent last)
    last_runs = last_runs[-10:]

    jam_rate = (jam / total) if total else 0.0
    return {
        "total_runs": total,
        "by_phase": by_phase,
        "by_session": by_session,
        "jam_rate": jam_rate,
        "last_runs": last_runs,
    }


def write_summary_md() -> Path:
    """
    Regenerate data/analytics/summary.md
    """
    _ensure_dirs()
    agg = aggregate()
    lines: list[str] = []
    lines.append("# LEE Temporal Analytics Summary\n")
    lines.append(f"- Generated: {datetime.now(UTC).isoformat()}")
    lines.append(f"- Total runs: **{agg['total_runs']}**")
    lines.append(f"- JAM rate: **{agg['jam_rate']:.2%}**\n")

    lines.append("## By Final Phase")
    if agg["by_phase"]:
        for k, v in sorted(agg["by_phase"].items()):
            lines.append(f"- {k}: {v}")
    else:
        lines.append("- (no data)")

    lines.append("\n## By Session")
    if agg["by_session"]:
        for k, v in sorted(agg["by_session"].items()):
            lines.append(f"- {k}: {v}")
    else:
        lines.append("- (no data)")

    lines.append("\n## Last 10 Runs")
    if agg["last_runs"]:
        lines.append("| run_id | session | phase | time_to_mem_ms | end | log |")
        lines.append("|---|---|---|---:|---|---|")
        for r in agg["last_runs"]:
            lines.append(
                f"| {r.get('run_id','')} | {r.get('session','')} | "
                f"{r.get('final_phase','')} | {str(r.get('time_to_mem_ms') or '')} | "
                f"{r.get('ts_end','')} | {r.get('log_json','')} |"
            )
    else:
        lines.append("- (no recent runs)")

    SUMMARY_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return SUMMARY_MD


# ---------- charts (optional) ----------

def write_phase_bar_chart() -> Optional[Path]:
    """
    Bar chart of final phases → data/analytics/by_phase.png
    """
    try:
        import matplotlib.pyplot as plt  # no seaborn
    except Exception:
        return None
    _ensure_dirs()
    agg = aggregate()
    by_phase = agg.get("by_phase", {}) or {}
    if not by_phase:
        return None
    phases = list(sorted(by_phase.keys()))
    counts = [by_phase[p] for p in phases]

    out = ANALYTICS_DIR / "by_phase.png"
    plt.figure()
    plt.bar(phases, counts)
    plt.title("LEE Runs by Final Phase")
    plt.xlabel("Final Phase")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(out)
    plt.close()
    return out


def write_time_to_mem_chart() -> Optional[Path]:
    """
    Line chart of time_to_mem_ms across runs → data/analytics/time_to_mem_ms.png
    """
    try:
        import matplotlib.pyplot as plt
    except Exception:
        return None
    _ensure_dirs()
    xs, ys = [], []
    i = 0
    for rec in _iter_history():
        t = rec.get("time_to_mem_ms")
        if isinstance(t, (int, float)):
            i += 1
            xs.append(i)
            ys.append(float(t))
    if not ys:
        return None

    out = ANALYTICS_DIR / "time_to_mem_ms.png"
    plt.figure()
    plt.plot(xs, ys)
    plt.title("Time to MEM per JAM Run")
    plt.xlabel("Run index (with timing)")
    plt.ylabel("ms")
    plt.tight_layout()
    plt.savefig(out)
    plt.close()
    return out

def _light_md_to_html(md: str) -> str:
    """Very small MD→HTML: #, ##, ### and **bold** only; everything else escaped."""
    out = []
    for raw in md.splitlines():
        line = raw.rstrip("\n")
        # headings
        if line.startswith("### "):
            out.append(f"<h3>{escape(line[4:])}</h3>")
            continue
        if line.startswith("## "):
            out.append(f"<h2>{escape(line[3:])}</h2>")
            continue
        if line.startswith("# "):
            out.append(f"<h1>{escape(line[2:])}</h1>")
            continue
        # bold: **text**
        esc = escape(line)
        parts = esc.split("**")
        if len(parts) > 1:
            buf = []
            for i, p in enumerate(parts):
                if i % 2 == 1:
                    buf.append(f"<strong>{p}</strong>")
                else:
                    buf.append(p)
            esc = "".join(buf)
        out.append(f"<p>{esc}</p>")
    return "\n".join(out)


def write_index_html() -> Path:
    """
    Emit data/analytics/index.html with rendered summary + embedded charts + links.
    """
    _ensure_dirs()
    # read summary md (ensure it exists)
    if not SUMMARY_MD.exists():
        write_summary_md()
    md = SUMMARY_MD.read_text(encoding="utf-8")
    body = _light_md_to_html(md)

    # latest run links (from aggregate)
    agg = aggregate()
    latest = agg["last_runs"][-1] if agg.get("last_runs") else None
    latest_links = ""
    if latest:
        log = latest.get("log_json", "")
        prov = str(Path(log).with_suffix(".prov.jsonl"))
        tmd = str(Path(log).with_suffix(".timeline.md"))
        dot = str(Path(log).with_suffix(".timeline.dot"))
        latest_links = (
            "<section><h2>Latest Run Artifacts</h2>"
            f"<ul>"
            f"<li><a href='{escape(log)}'>{escape(log)}</a></li>"
            f"<li><a href='{escape(prov)}'>{escape(prov)}</a></li>"
            f"<li><a href='{escape(tmd)}'>{escape(tmd)}</a></li>"
            f"<li><a href='{escape(dot)}'>{escape(dot)}</a></li>"
            f"</ul></section>"
        )

    # charts (if present)
    by_phase_png = (ANALYTICS_DIR / "by_phase.png")
    ttm_png = (ANALYTICS_DIR / "time_to_mem_ms.png")
    charts_html = "<section><h2>Charts</h2>"
    if by_phase_png.exists():
        charts_html += f"<figure><img src='{by_phase_png.as_posix()}' alt='By Phase'><figcaption>Runs by Final Phase</figcaption></figure>"
    if ttm_png.exists():
        charts_html += f"<figure><img src='{ttm_png.as_posix()}' alt='Time to MEM'><figcaption>Time to MEM per JAM Run</figcaption></figure>"
    charts_html += "</section>"

    # minimal Carver-esque style
    css = """
    body{font:14px/1.5 system-ui,-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;color:#111;margin:2rem;max-width:900px}
    h1,h2,h3{font-weight:600;letter-spacing:.2px;margin:.8rem 0 .4rem}
    h1{font-size:1.6rem;border-bottom:1px solid #ddd;padding-bottom:.2rem}
    h2{font-size:1.25rem;margin-top:1.2rem}
    p{margin:.4rem 0}
    ul{padding-left:1.2rem}
    figure{margin:1rem 0}
    img{max-width:100%;height:auto;border:1px solid #eee}
    footer{margin-top:2rem;color:#666;font-size:.9rem}
    """

    html = f"""<!doctype html>
<html lang="en">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>LEE Analytics</title>
<style>{css}</style>
<body>
{body}
{charts_html}
{latest_links}
<footer>Generated {datetime.now(UTC).isoformat()}</footer>
</body>
</html>"""

    out = ANALYTICS_DIR / "index.html"
    out.write_text(html, encoding="utf-8")
    return out

# ---------- CLI ----------

def _cli(argv: list[str]) -> int:
    if not argv:
        print("Usage: python -m src.engine.analytics [report|charts]")
        return 2
    cmd = argv[0]
    if cmd == "report":
        p = write_summary_md()
        print(f"Wrote {p}")
        return 0
    if cmd == "html":
        # ensure summary + charts exist first
        write_summary_md()
        write_phase_bar_chart()
        write_time_to_mem_chart()
        p = write_index_html()
        print(f"Wrote {p}")
        return 0
    if cmd == "charts":
        # ensure summary exists
        write_summary_md()
        p1 = write_phase_bar_chart()
        p2 = write_time_to_mem_chart()
        msg = "Wrote "
        parts = []
        if p1: parts.append(str(p1))
        if p2: parts.append(str(p2))
        if parts:
            print(msg + " and ".join(parts))
        else:
            print("No charts written (no matplotlib or no data)")
        return 0
    print("Unknown command. Use report or charts.")
    return 2

if __name__ == "__main__":
    import sys
    raise SystemExit(_cli(sys.argv[1:]))
