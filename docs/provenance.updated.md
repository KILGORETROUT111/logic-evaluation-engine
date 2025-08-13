# Provenance

When `enable_provenance=True`, LEE writes:
- `<log>.prov.jsonl` – line-delimited events
- `<log>.svg` – compact timeline
- `<log>.json` – run summary

Events you’ll see: `start`, `prenorm`, `rewrite`, `enrich`, `detect`, `transition`.

```python
from pathlib import Path
log = Path(res["log_json"])
print(log.with_suffix(".prov.jsonl").read_text().splitlines()[:3])

---

## StressIndex in Provenance

When enabled, StressIndex entries appear in `.prov.jsonl` with winding and jam ratio for each run (or window):

```json
{"event":"stress_index","value":0.38,"winding_deg":180,"jam_ratio":0.4}
```

---

## Winding and Resistance in Provenance

- **Winding** is stored as cumulative degrees and average phase vector.  
- **Resistance** records cycle counts and mean rotation deltas across repeated transitions.

These metrics enable post-run diagnosis and replay validation.
