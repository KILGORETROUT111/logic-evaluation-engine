# StressIndex Metric

The **StressIndex** quantifies logical strain within a LEE run by combining **structural** and **temporal** factors:

- **Contradiction density** — proportion of contradiction events over total phase events.
- **Time-weighting** — penalizing prolonged unresolved contradictions.
- **Topology distortion** — optional integration with manifold distortion metrics (future).

## Formula

Let:
- `C` = number of contradiction events
- `N` = total events
- `T_c` = total duration contradictions persisted
- `T_total` = total run duration

Then:

$$
\text{StressIndex} = \alpha \frac{C}{N} + (1 - \alpha) \frac{T_c}{T_{total}}
$$

Where \( \alpha \) balances structure vs time (default 0.5).

## Interpretation
- **0.0** → completely stable logical flow
- **1.0** → maximum strain, system persistently in contradiction
- Mid-range values often indicate intermittent but recoverable stress states

---

## Usage in LEE

```bash
python scripts/compute_stress.py \
  --summary scripts/data/logs/<log>.json \
  --prov scripts/data/logs/<log>.prov.jsonl \
  --output scripts/data/metrics/stress_<log>.json
