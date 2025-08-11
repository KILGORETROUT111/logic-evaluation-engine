# API Overview

## Pipeline
```python
from src.engine import Pipeline

p = Pipeline(
  log_name="demo",
  domain="legal",               # 'legal' | 'medical' | 'general'
  enable_provenance=True,
  session="default",
  patient_id=None,
  case_id=None,
)

res = p.run("1 -> 0")
# res: {
#   "state": {"phase": "MEM"},
#   "history": {"phases": ["ALIVE","JAM","MEM"], "run_id": "..."},
#   "log_json": "data/logs/demo_...json",
#   ...
# }
