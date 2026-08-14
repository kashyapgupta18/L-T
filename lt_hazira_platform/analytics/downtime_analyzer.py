"""Downtime Pareto and root-cause analysis."""
import pandas as pd
from typing import Dict, Any

def analyze_downtime_by_machine_type(df: pd.DataFrame) -> pd.DataFrame:
    grouped = df.groupby("machine_type")["downtime_hours"].sum().reset_index()
    grouped = grouped.sort_values(by="downtime_hours", ascending=False)
    total_downtime = grouped["downtime_hours"].sum()
    grouped["percentage"] = (grouped["downtime_hours"] / total_downtime * 100).round(2)
    grouped["cumulative_percentage"] = grouped["percentage"].cumsum().round(2)
    return grouped
