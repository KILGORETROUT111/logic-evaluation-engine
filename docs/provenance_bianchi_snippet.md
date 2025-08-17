
## Logical Bianchi Identity (v2): Provenance & Auditor

We adopt a discrete exterior-calculus view of the phase graph. Let `JAM` represent contradiction.  
Define per run:
- `flux_in(JAM)` = count of transitions entering `JAM`
- `flux_out(JAM)` = count of transitions leaving `JAM`

**Bianchi residual** (machine-checkable):
```
bianchi_residual = | flux_in(JAM) - flux_out(JAM) |
```
Target is `0` for complete, well-formed runs (no contradiction monopoles). The auditor writes this value alongside StressIndex.

**Recorder requirement:** emit a `transition` event with `before`/`after` on every phase change.

_Attribution:_ The explicit conservation reading and residual mapping build on an external contribution, “Revisiting Logical Bianchi Identity” (credited to the originator). LEE’s earlier Bianchi analogy and the identity of conjugate quantities remain original to LEE.
