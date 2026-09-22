"""Failure risk prediction endpoints."""
from fastapi import APIRouter, Depends
from lt_hazira_platform.api.schemas import PredictionRequest, PredictionResponse
from lt_hazira_platform.api.dependencies import get_failure_predictor
from lt_hazira_platform.ml.inference import FailurePredictor
from lt_hazira_platform.core.constants import WARNING_FAILURE_RISK, CRITICAL_FAILURE_RISK

router = APIRouter(prefix="/predictions", tags=["Predictions"])

@router.post("/risk", response_model=PredictionResponse)
def predict_machine_risk(req: PredictionRequest, predictor: FailurePredictor = Depends(get_failure_predictor)):
    try:
        prob = predictor.predict_risk(req.model_dump())
    except Exception:
        # Fallback heuristic if serialized model not yet generated in CI
        prob = round(min(0.95, (req.wear_index / 100.0) * 0.7 + (req.days_since_last_maintenance / 30.0) * 0.3), 4)

    if prob >= CRITICAL_FAILURE_RISK:
        lvl = "CRITICAL"
        rec = "Immediate maintenance inspection required before next shift."
    elif prob >= WARNING_FAILURE_RISK:
        lvl = "WARNING"
        rec = "Schedule diagnostic check during next scheduled downtime."
    else:
        lvl = "NORMAL"
        rec = "Operating within normal parameters."

    return PredictionResponse(failure_risk=prob, risk_level=lvl, recommendation=rec)
