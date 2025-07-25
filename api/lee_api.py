from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uuid
import os
import logging
logging.basicConfig(level=logging.DEBUG)
from evaluation.recursive_diagnostic_engine import run_recursive_diagnosis_and_export

app = FastAPI(title="O---O API – Logic Evaluation Engine", version="1.0")

# === Data Model ===
class DiagnosisRequest(BaseModel):
    goal: str
    facts: List[str]
    axioms: List[str]
    metadata: Optional[dict] = None

# === Endpoint ===
@app.post("/diagnose")
def diagnose(request: DiagnosisRequest):
    try:
        output = run_recursive_diagnosis_and_export(
            goal=request.goal,
            facts=request.facts,
            axioms=request.axioms,
            meta=request.metadata or {}
        )
        return {
            "trace": output.get("trace", []),
            "confidence_score": output.get("confidence_score", None),
            "probes": output.get("probes", []),
            "rotation_history": output.get("rotation_history", []),
            "diagnosis_id": str(uuid.uuid4()),
            "status": "success"
        }
    except Exception as e:
        import traceback
        traceback.print_exc()  # <—— Print the full traceback to console
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "OK", "message": "O---O API live"}

@app.get("/")
def root():
    return {
        "message": "Welcome to the O---O API for Logic Evaluation Engine (LEE)",
        "version": "1.0",
        "routes": ["/diagnose", "/health"]
    }
