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


