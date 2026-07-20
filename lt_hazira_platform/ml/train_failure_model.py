"""
Predicts whether a given machine-shift record is likely to be a failure event,
using features available at the time (no leakage from the failure_event label
itself, obviously, and no post-hoc maintenance info either — only what a
supervisor would actually know going into a shift).

Model: gradient-boosted trees (scikit-learn's HistGradientBoostingClassifier),
chosen over logistic regression because the wear/downtime relationship is
non-linear (risk accelerates, it doesn't grow steadily), and over a deep net
because 25k rows of tabular data doesn't need one and a tree model stays
interpretable via feature importance.

Run:
    python train_failure_model.py
Outputs a trained model to ../data/failure_model.joblib and prints metrics.
"""

import os
import sqlite3
import numpy as np
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.inspection import permutation_importance

BASE = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE, "..", "data", "hazira_manufacturing.db")
MODEL_PATH = os.path.join(BASE, "..", "data", "failure_model.joblib")


def load_features():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("""
        SELECT f.machine_id, f.date_id, f.shift_id, f.plant_id,
               f.planned_qty, f.produced_qty, f.defective_qty,
               f.downtime_minutes, f.energy_consumed_kwh, f.machine_wear_index,
               f.failure_event,
               m.machine_type, m.rated_capacity_units_per_hour, m.base_energy_kwh_per_hour,
               d.day_of_week, d.is_weekend
        FROM fact_production f
        JOIN dim_machine m ON f.machine_id = m.machine_id
        JOIN dim_date d ON f.date_id = d.date_id
    """, conn)
    conn.close()
    return df


def build_features(df):
    df = df.sort_values(["machine_id", "date_id", "shift_id"]).reset_index(drop=True)

    # rolling features per machine: recent downtime and defect trend are the
    # kind of signal a maintenance supervisor would actually watch
    df["defect_rate"] = df["defective_qty"] / df["produced_qty"].replace(0, np.nan)
    df["defect_rate"] = df["defect_rate"].fillna(0)

    df["prior_downtime_avg3"] = (
        df.groupby("machine_id")["downtime_minutes"]
        .transform(lambda s: s.shift(1).rolling(3, min_periods=1).mean())
        .fillna(0)
    )
    df["prior_wear"] = df.groupby("machine_id")["machine_wear_index"].shift(1).fillna(df["machine_wear_index"])

    # IMPORTANT: downtime_minutes and defect_rate for the *current* shift are
    # not used as features. Both are direct downstream consequences of the
    # failure event itself in this dataset's generation logic, so including
    # them would be leakage - the model would just be reading the label off
    # a disguised copy of itself. Only pre-shift-known information (prior
    # wear, prior downtime history, machine/plant identity) is fair game.
    feature_cols = [
        "planned_qty",
        "prior_wear", "prior_downtime_avg3",
        "rated_capacity_units_per_hour", "base_energy_kwh_per_hour",
        "is_weekend",
    ]
    categorical_cols = ["machine_type", "shift_id", "plant_id"]

    X = pd.get_dummies(df[feature_cols + categorical_cols], columns=categorical_cols, drop_first=True)
    y = df["failure_event"].astype(int)
    return X, y, df


def main():
    print("Loading data from SQLite...")
    df = load_features()
    print(f"  {len(df):,} rows, failure rate: {df['failure_event'].mean()*100:.2f}%")

    X, y, df_full = build_features(df)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print("Training HistGradientBoostingClassifier...")
    model = HistGradientBoostingClassifier(
        max_iter=200, learning_rate=0.08, max_depth=6,
        class_weight="balanced", random_state=42
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    print("\n--- Test set performance ---")
    print(classification_report(y_test, y_pred, target_names=["No failure", "Failure"]))
    print(f"ROC-AUC: {roc_auc_score(y_test, y_proba):.3f}")

    print("\nComputing permutation feature importance (this takes a moment)...")
    result = permutation_importance(model, X_test, y_test, n_repeats=5, random_state=42, n_jobs=-1)
    importance_df = pd.DataFrame({
        "feature": X.columns,
        "importance": result.importances_mean,
    }).sort_values("importance", ascending=False).head(10)
    print("\nTop features driving failure risk:")
    print(importance_df.to_string(index=False))

    joblib.dump({"model": model, "feature_columns": list(X.columns)}, MODEL_PATH)
    print(f"\nModel saved to {os.path.abspath(MODEL_PATH)}")


if __name__ == "__main__":
    main()
