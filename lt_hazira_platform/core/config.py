"""Centralized configuration management for the platform."""
import os
from dataclasses import dataclass
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

@dataclass(frozen=True)
class AppConfig:
    data_dir: Path = BASE_DIR / "data"
    db_path: Path = BASE_DIR / "data" / "hazira_manufacturing.db"
    model_path: Path = BASE_DIR / "data" / "failure_model.joblib"
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    prediction_threshold: float = float(os.getenv("PREDICTION_THRESHOLD", "0.35"))
    app_port: int = int(os.getenv("APP_PORT", "8501"))
    api_port: int = int(os.getenv("API_PORT", "8000"))

config = AppConfig()
