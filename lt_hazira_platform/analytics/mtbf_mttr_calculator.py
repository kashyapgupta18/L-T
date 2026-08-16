"""Reliability metrics: MTBF (Mean Time Between Failures) and MTTR (Mean Time to Repair)."""
import pandas as pd
from typing import Dict

def calculate_reliability_metrics(maintenance_df: pd.DataFrame, total_operating_hours: float) -> Dict[str, float]:
    failures = maintenance_df[maintenance_df["maintenance_type"] == "Corrective"]
    failure_count = len(failures)
    
    if failure_count == 0:
        return {"mtbf_hours": total_operating_hours, "mttr_hours": 0.0, "failure_count": 0}
        
    total_downtime = failures["duration_hours"].sum()
    mtbf = round((total_operating_hours - total_downtime) / failure_count, 2)
    mttr = round(total_downtime / failure_count, 2)
    return {"mtbf_hours": mtbf, "mttr_hours": mttr, "failure_count": failure_count}
