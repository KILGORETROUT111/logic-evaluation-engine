
## docs/pipeline.md
```md
# Pipeline

```mermaid
flowchart LR
  A[Input] --> B[Prenorm]
  B --> C[Rewrite/NLP]
  C --> D[Detect]
  D -->|JAM| E[MEM]
  D -->|No JAM| E
