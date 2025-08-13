[![CI (v3.0)](https://github.com/KILGORETROUT111/logic-evaluation-engine/actions/workflows/ci.yml/badge.svg?branch=v3.0)](https://github.com/KILGORETROUT111/logic-evaluation-engine/actions/workflows/ci.yml)
![Python 3.10–3.13](https://img.shields.io/badge/python-3.10%E2%80%933.13-blue)

# Logic Evaluation Engine (LEE) — v3.0

## Inspiration
![Billy Joel - Live in Uniondale, December 29, 1982](docs/billy-joel-uniondale-1982.png)
> **“Happy New Year Long Island. And don’t take any shit from anybody!”**  
> — Billy Joel, [Live in Uniondale (December 29, 1982)](https://www.youtube.com/watch?v=wDEvqyiRpzE&t=5596s)

_This project, like Billy said, is about doing the work right — and not taking any crap from broken logic, bad data, or bloated design._

Basis5 rotational phase logic + NL → λ-calculus → evaluator handshake.  
Canonical phase path: **ALIVE → JAM → MEM** with Basis5 winding/witness recorded in traces.

## Quickstart
```bash
# from repo root
pip install -e .
lee "if A then B" -d legal --pretty