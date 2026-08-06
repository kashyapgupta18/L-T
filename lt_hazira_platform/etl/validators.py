"""Validation logic for incoming manufacturing facts."""
import pandas as pd
from lt_hazira_platform.core.exceptions import DataValidationError
from lt_hazira_platform.core.constants import SHIFT_HOURS

def validate_production_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    required_cols = [
        "date_id", "plant_id", "machine_id", "shift_id", "product_id",
        "units_produced", "units_defective", "operating_hours",
        "downtime_hours", "energy_kwh", "wear_index"
    ]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise DataValidationError(f"Missing required columns in production dataframe: {missing}")

    # Physical checks
    if (df["operating_hours"] < 0).any() or (df["operating_hours"] > SHIFT_HOURS).any():
        raise DataValidationError("Operating hours must be between 0 and shift length (8h)")
    if (df["downtime_hours"] < 0).any() or (df["downtime_hours"] > SHIFT_HOURS).any():
        raise DataValidationError("Downtime hours must be between 0 and shift length (8h)")
    if (df["units_produced"] < 0).any():
        raise DataValidationError("Units produced cannot be negative")
    if (df["units_defective"] > df["units_produced"]).any():
        raise DataValidationError("Defects cannot exceed total units produced")
    if (df["wear_index"] < 0).any() or (df["wear_index"] > 100).any():
        raise DataValidationError("Wear index must be bounded between 0 and 100")

    return df
