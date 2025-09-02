# -*- coding: utf-8 -*-
"""
LEE CLI (patched)
- Prints JSON to stdout
- Returns 0 on success when called as a function (pytest calls main()).
"""

from __future__ import annotations
import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict

try:
    from importlib.metadata import version, PackageNotFoundError  # type: ignore
except Exception:  # pragma: no cover
    version = None  # type: ignore
    PackageNotFoundError = Exception  # type: ignore


def _get_pkg_version() -> str:
    try:
        if version is None:
            return "0.0.0"
        return version("logic-evaluation-engine")
    except PackageNotFoundError:
        return "0.0.0"


def run_once(text: str, *, domain: str = "test") -> Dict[str, Any]:
    from src.engine.pipeline import Pipeline  # local import
    p = Pipeline(log_name="lee_cli", domain=domain, enable_provenance=True, session="cli")
    return p.run(text)


def _reconstruct_jam(res: Dict[str, Any]) -> Dict[str, Any]:
    hist = res.get("history", {}) or {}
    return {
        "run_id": hist.get("run_id"),
        "phases": hist.get("phases", []),
        "transitions": hist.get("transitions", []),
        "final_phase": (res.get("state", {}) or {}).get("phase"),
    }


def main() -> int:
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")

    ap = argparse.ArgumentParser(prog="lee", description="LEE — evaluator and phase traces")
    ap.add_argument("--version", action="version", version=f"lee / LEE {_get_pkg_version()}")
    ap.add_argument("text", nargs="*", help="input text; if omitted, stdin is used")
    ap.add_argument("-d", "--domain", default="test", help="domain (default: test)")
    ap.add_argument("--pretty", action="store_true", help="pretty-print JSON")
    ap.add_argument("--jam", action="store_true", help="print JAM block only")
    ap.add_argument("--dump", metavar="PATH", help="write full JSON to PATH")
    args = ap.parse_args()

    text = " ".join(args.text).strip() if args.text else (sys.stdin.read() or "").strip()
    if not text:
        print("error: no input text provided", file=sys.stderr)
        return 2

    try:
        res = run_once(text, domain=args.domain)

        # Ensure tests can read data["result"]["pattern"]
        pattern = res.get("pattern") or (res.get("result", {}) or {}).get("pattern")
        out_obj: Dict[str, Any]
        if args.jam:
            out_obj = _reconstruct_jam(res)
        else:
            out_obj = dict(res)
            # inject/normalize a "result" section with at least pattern
            out_obj["result"] = dict(out_obj.get("result", {}) or {})
            if pattern is not None:
                out_obj["result"]["pattern"] = pattern

        if args.dump:
            p = Path(args.dump)
            p.parent.mkdir(parents=True, exist_ok=True)
            with p.open("w", encoding="utf-8") as f:
                json.dump(out_obj, f, ensure_ascii=False, indent=2 if args.pretty else None, sort_keys=args.pretty)

        print(json.dumps(out_obj, ensure_ascii=False, indent=2 if args.pretty else None, sort_keys=args.pretty))
        return 0
    except Exception as e:  # pragma: no cover
        print(f"error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
