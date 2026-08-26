"""Pre-shift feature engineering preventing data leakage."""
import pandas as pd
from typing import List

FEATURE_COLS = [
    "wear_index",
    "days_since_last_maintenance",
    "prev_shift_downtime",
    "avg_downtime_last_5_shifts",
    "machine_age_years",
]

def engineer_preshift_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if "machine_age_years" not in df.columns:
        df["machine_age_years"] = 5.0
    if "days_since_last_maintenance" not in df.columns:
        df["days_since_last_maintenance"] = (df["wear_index"] / 3.0).round(1)
    if "prev_shift_downtime" not in df.columns:
        df["prev_shift_downtime"] = 0.0
    if "avg_downtime_last_5_shifts" not in df.columns:
        df["avg_downtime_last_5_shifts"] = 0.2
    return df
