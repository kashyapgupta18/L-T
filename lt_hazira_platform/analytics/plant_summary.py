"""Executive-level multi-plant performance rollups."""
import pandas as pd

def generate_executive_plant_summary(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby("plant_name").agg(
        active_machines=("machine_id", "nunique"),
        total_production=("units_produced", "sum"),
        avg_downtime_per_shift=("downtime_hours", "mean"),
        total_energy_mwh=("energy_kwh", lambda x: round(x.sum() / 1000.0, 2))
    ).reset_index()
