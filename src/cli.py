# src/cli.py
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict

# --- robust imports: work both in-repo ("src.*") and installed package ("*") ---
try:
    from importlib.metadata import version as _pkg_version, PackageNotFoundError
except Exception:  # very old Python fallback (shouldn't happen on 3.10+)
    _pkg_version = lambda _name: "0+local"  # type: ignore[misc]
    class PackageNotFoundError(Exception): ...  # type: ignore[override]

try:
    from src.engine.pipeline import Pipeline  # dev/editable layout
    from src.nlp.handshake import evaluate_text
except Exception:
    # installed package layout
    from engine.pipeline import Pipeline
    from nlp.handshake import evaluate_text


def _ensure_utf8_stdio() -> None:
    """Try to ensure stdout/stderr use UTF-8 (Windows-safe)."""
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    except Exception:
        pass
    try:
        sys.stderr.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    except Exception:
        pass


def _get_pkg_version() -> str:
    try:
        return _pkg_version("logic-evaluation-engine")
    except PackageNotFoundError:
        return "0+local"


def run_once(text: str, domain: str = "test") -> Dict[str, Any]:
    """
    Execute one LEE run through the Pipeline using the NL→λ handshake.

    Returns the full result bundle:
      {
        "state": {"phase": "MEM"},
        "history": { ... transitions ... },
        "result": {
          "pattern": "A -> B",
          "basis5": {"winding": ..., "witness": ...}
        }
      }
    """
    pipe = Pipeline(log_name="cli", domain=domain, enable_provenance=True, session="cli")
    return evaluate_text(text, pipe)


def _reconstruct_jam(res: Dict[str, Any]) -> Dict[str, Any]:
    """
    Build a concise JAM payload from the returned history/result.
    (This mirrors what memdb receives, without requiring the memdb sink.)
    """
    pattern = res.get("result", {}).get("pattern")
    jam_details = {}
    try:
        jams = [t for t in res["history"]["transitions"] if t.get("to") == "JAM"]
        if jams:
            jam_details = jams[-1].get("details", {}) or {}
    except Exception:
        jam_details = {}

    jam = {"pattern": pattern or jam_details.get("pattern")}
    # carry optional fields when present
    for k in ("nl", "lambda_nf", "adapter"):
        if k in jam_details:
            jam[k] = jam_details[k]
    return jam


def main() -> None:
    _ensure_utf8_stdio()

    parser = argparse.ArgumentParser(
        prog="lee",
        description="Logic Evaluation Engine (LEE) — NL → λ → evaluator → basis5 traces",
    )

    # --version flag reads installed distribution version
    parser.add_argument(
        "--version",
        action="version",
        version=f"lee / LEE {_get_pkg_version()}",
        help="show version and exit",
    )

    # Positional text (optional). If omitted, read from stdin.
    parser.add_argument(
        "text",
        nargs="*",
        help='input text (e.g., if A then B, or A->B). If omitted, stdin is used.',
    )

    parser.add_argument(
        "--domain", "-d",
        default="test",
        help="domain (legal, medical, defense, ...). Default: %(default)s",
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="pretty-print JSON output",
    )
    parser.add_argument(
        "--jam",
        action="store_true",
        help="print only the JAM block reconstructed from history",
    )
    parser.add_argument(
        "--dump",
        metavar="PATH",
        help="save full JSON result to PATH",
    )

    args = parser.parse_args()

    # Determine the input text
    if args.text:
        # join in case user provided multiple tokens without quotes
        text = " ".join(args.text).strip()
    else:
        data = sys.stdin.read()
        text = (data or "").strip()

    if not text:
        print("error: no input text provided (pass TEXT or pipe via stdin)", file=sys.stderr)
        sys.exit(2)

    try:
        res = run_once(text, domain=args.domain)

        # optionally dump to file
        if args.dump:
            path = Path(args.dump)
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("w", encoding="utf-8") as f:
                json.dump(res, f, ensure_ascii=False, indent=2 if args.pretty else None, sort_keys=args.pretty)

        # choose output payload
        out_obj: Dict[str, Any]
        if args.jam:
            out_obj = _reconstruct_jam(res)
        else:
            out_obj = res

        # print to stdout
        if args.pretty:
            print(json.dumps(out_obj, ensure_ascii=False, indent=2, sort_keys=True))
        else:
            print(json.dumps(out_obj, ensure_ascii=False))

        sys.exit(0)

    except KeyboardInterrupt:
        print("aborted by user", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        # Fail-safe: never crash without a clear message + nonzero code
        print(f"error: {e.__class__.__name__}: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
