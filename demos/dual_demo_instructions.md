---

## 🌐 REST API Sample (O---O API)

You can also run the same dual demo logic via the new REST API interface:

### Step 1: Start the API Server

From the root of your repo, run:

```bash
uvicorn api.lee_api:app --reload
```

You should see confirmation like:

```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### Step 2: Open the Swagger UI

Visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) in your browser.

### Step 3: Run the Legal Diagnostic Case

Paste the following JSON into the `POST /diagnose` interface:

```json
{
  "goal": "PenaltyApplies(x)",
  "facts": [
    "ContractBreach(x)",
    "NoticeGiven(x)",
    "UnavoidableCircumstances(x)"
  ],
  "axioms": [
    "(ContractBreach(x) ∧ ¬NoticeGiven(x)) → PenaltyApplies(x)",
    "(NoticeGiven(x) ∧ MitigatingCircumstances(x)) → ¬PenaltyApplies(x)",
    "UnavoidableCircumstances(x) → MitigatingCircumstances(x)"
  ]
}
```

### Step 4: Check Output

You will get a JSON trace response and a `.txt` / `.json` pair will be exported to:

```
evaluation/cpee_output/diagnostic_trace_<timestamp>.json
```

> This demonstrates REST-backed invocation of phase logic and contradiction-rotation handling.