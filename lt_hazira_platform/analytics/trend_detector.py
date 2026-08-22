"""Longitudinal degradation and trend detection."""
import pandas as pd

def detect_wear_acceleration(df: pd.DataFrame, window: int = 7) -> pd.DataFrame:
    df_sorted = df.sort_values(by=["machine_id", "date_id"])
    df_sorted["rolling_wear_slope"] = (
        df_sorted.groupby("machine_id")["wear_index"]
        .diff()
        .rolling(window=window, min_periods=1)
        .mean()
    )
    return df_sorted
