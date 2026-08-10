"""ETL execution audit trail tracker."""
from dataclasses import dataclass, field
import datetime
import json
from pathlib import Path
from typing import Optional

@dataclass
class ETLAuditRecord:
    stage: str
    records_processed: int
    records_rejected: int
    duration_seconds: float
    status: str
    timestamp: str = field(default_factory=lambda: datetime.datetime.now().isoformat())
    error_message: Optional[str] = None

class ETLAuditor:
    def __init__(self, log_path: Optional[Path] = None):
        self.log_path = log_path
        self.records = []

    def log_record(self, record: ETLAuditRecord):
        self.records.append(record)
        if self.log_path:
            with open(self.log_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(record.__dict__) + "\n")
