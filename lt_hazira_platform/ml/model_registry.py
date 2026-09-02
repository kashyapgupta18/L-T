"""Model metadata tracking and artifact management."""
from dataclasses import dataclass, field
import datetime
import json
from pathlib import Path
from typing import Dict, Any

@dataclass
class ModelManifest:
    model_name: str
    version: str
    algorithm: str
    metrics: Dict[str, float]
    created_at: str = field(default_factory=lambda: datetime.datetime.now().isoformat())

def save_model_manifest(manifest: ModelManifest, output_path: Path):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(manifest.__dict__, f, indent=2)
