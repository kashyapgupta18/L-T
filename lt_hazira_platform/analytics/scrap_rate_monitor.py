"""Scrap rate and quality defect monitoring."""
import pandas as pd

def compute_scrap_rates_by_product(df: pd.DataFrame) -> pd.DataFrame:
    summary = df.groupby(["product_id", "product_name"]).agg(
        total_produced=("units_produced", "sum"),
        total_defective=("units_defective", "sum")
    ).reset_index()
    summary["scrap_rate_pct"] = (summary["total_defective"] / summary["total_produced"] * 100).round(3)
    return summary.sort_values(by="scrap_rate_pct", ascending=False)
