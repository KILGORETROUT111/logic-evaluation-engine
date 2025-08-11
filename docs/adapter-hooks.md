# Adapter Hooks

Adapters provide domain enrichments during the `enrich` stage of the pipeline. In tests/demos we often **monkeypatch** hooks onto `src.engine.pipeline` so `Pipeline` discovers them at import time.

## Hook names & signatures

- `dm_classify(text: str) -> str`  
  Divergence classification (e.g., `"low"`, `"hi-risk"`).
- `ner_extract(text: str) -> list[dict]`  
  Simple NER payloads.
- `cf_analyze(text: str) -> dict`  
  Counterfactual analysis.

## Example (monkeypatch + run)

```python
import importlib
import src.engine.pipeline as pl
from src.engine import Pipeline

pl.dm_classify = lambda s: "hi-risk"
pl.ner_extract = lambda s: [{"text": "1"}]
pl.cf_analyze  = lambda s: {"flag": "cf-ok"}
importlib.reload(pl)

p = Pipeline(log_name="hooks_demo", domain="medical", enable_provenance=True, session="t")
res = p.run("1 -> 0")

# Enrichment becomes part of detect details in provenance:
# detect.details.enrichment == {'domain': 'medical', 'pattern': '1 -> 0', 'score': 0.5,
#                               'tags': ['implication', 'boolean'], 'risk': 'hi-risk',
#                               'entities': [{'text': '1'}], 'counterfactual': {'flag': 'cf-ok'}}
