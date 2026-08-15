"""Energy intensity profiling for heavy fabrication machinery."""
import pandas as pd

def compute_energy_intensity(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    # Avoid zero division
    df["kwh_per_unit"] = (df["energy_kwh"] / df["units_produced"].replace(0, float("nan"))).round(3)
    summary = df.groupby("machine_id").agg(
        total_energy_kwh=("energy_kwh", "sum"),
        avg_energy_per_shift=("energy_kwh", "mean"),
        avg_kwh_per_unit=("kwh_per_unit", "mean")
    ).reset_index()
    return summary
