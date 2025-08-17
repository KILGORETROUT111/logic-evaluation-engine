## Exhaustibility Provenance (Basis5 Taxonomy)

Every experiment can record its mathlog-to-code status.

**JSONL schema (added fields):**
```json
{
  "ts": "2025-08-17T21:11:03+0000",
  "event": "stress_index_run",
  "payload": {
    "run_id": "demo-001",
    "dataset": "demo",
    "stress_index": 0.742,
    "winding": 1.0,
    "resistance": 0.18,
    "bianchi_residual": 0.013,
    "duration_s": 2.41
  },
  "exhaustibility_class": "I",
  "evidence": ["complexity_upper_bound","approx_algo_v1"],
  "reviewer": "WAP-IV",
  "context": {
    "cli": { "...": "..." },
    "git_rev": "e7a9c3d",
    "machine": "LEE-WS01"
  }
}
