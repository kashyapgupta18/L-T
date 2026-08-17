"""Shift performance comparison and variance analysis."""
import pandas as pd

def analyze_shift_performance(df: pd.DataFrame) -> pd.DataFrame:
    grouped = df.groupby("shift_name").agg(
        total_units=("units_produced", "sum"),
        avg_defect_rate=("units_defective", lambda x: (x.sum() / df.loc[x.index, "units_produced"].sum()) * 100),
        total_downtime=("downtime_hours", "sum"),
        avg_wear_increase=("wear_index", "mean")
    ).reset_index()
    return grouped
