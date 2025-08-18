# LEE · SWAP STATE (for next AI/operator)
Last updated: <YYYY-MM-DD> by <name/initials>

## 0) Project Coordinates
- Repo branch/tag: <v3.0 / v3.1-pre-grant / …>
- Active vertical(s): <medical / legal / defense / …>
- Patent: Provisional filed (Patent Pending). SB/16 + Spec + Drawings uploaded. Fee: <paid/pending>.
- Live docs index: /docs/whitepapers/README.md

## 1) Current Phase & Objectives
- Basis level: <Basis5LM | Basis5HM | Mixed>
- Primary objective (next 1–2 weeks): <e.g., StressIndex end-to-end with time-weighting>
- Secondary objective: <e.g., Bianchi residual v2 integration in provenance/stress>

## 2) State of Code
- Entry points:
  - `scripts/compute_stress.py` (CLI) — emits metrics + provenance
  - `scripts/prov_util.py` — `append_prov()` (JSONL)
- Important flags:
  - `--exhaustibility-class I|II|III`
  - `--evidence <tags…>`
  - `--prov-out <path.prov.jsonl>`
- Latest good run: <run_id> → logs in `scripts/data/logs/<run_id>*`
- Open code tasks:
  - [ ] Add time-weighted StressIndex (true Δt weighting)
  - [ ] Finalize Bianchi residual v2 computation & thresholds
  - [ ] Batch runner for multiple summaries

## 3) Data & Outputs
- Latest summary: `<path to *.json>`
- Latest prov log: `<path to *.prov.jsonl>`
- Latest figures: `<paths to *.svg *.png>`
- Datasets in play: <list>

## 4) Exhaustibility Tracking (Basis5 Taxonomy)
- Policy: record per run in prov JSONL:
  ```json
  {"exhaustibility_class":"I|II|III","evidence":["..."],"reviewer":"WAP-IV"}
