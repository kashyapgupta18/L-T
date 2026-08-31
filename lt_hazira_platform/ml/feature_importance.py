"""Feature importance extraction and ranking."""
import pandas as pd
from typing import List

def extract_feature_importances(model, feature_names: List[str]) -> pd.DataFrame:
    if hasattr(model, "feature_importances_"):
        imps = model.feature_importances_
    elif hasattr(model, "coef_"):
        imps = model.coef_[0]
    else:
        imps = [1.0 / len(feature_names)] * len(feature_names)
        
    df = pd.DataFrame({"feature": feature_names, "importance": imps})
    return df.sort_values(by="importance", ascending=False).reset_index(drop=True)
