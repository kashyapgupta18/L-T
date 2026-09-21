"""System health and liveness probe endpoints."""
from fastapi import APIRouter
import time

router = APIRouter(prefix="/health", tags=["Health"])
START_TIME = time.time()

@router.get("")
def health_check():
    return {
        "status": "healthy",
        "service": "L&T Hazira Manufacturing Analytics API",
        "uptime_seconds": round(time.time() - START_TIME, 1)
    }
