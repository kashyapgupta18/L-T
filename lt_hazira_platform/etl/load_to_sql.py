"""
ETL step 2: load the generated CSVs into a normalized SQLite database.

This is deliberately written as a real (small) ETL, not a one-line pandas
to_sql dump: it validates referential integrity, coerces types, flags/drops
bad rows, and logs what happened. That's the part worth pointing to in an
interview, more than the SQL itself.

Run:
    python load_to_sql.py
"""

import os
import sqlite3
import pandas as pd

BASE = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE, "..", "data")
SCHEMA_PATH = os.path.join(BASE, "..", "sql", "schema.sql")
DB_PATH = os.path.join(DATA_DIR, "hazira_manufacturing.db")


def log(msg):
    print(f"[ETL] {msg}")


def clean_dim(df, key_col):
    before = len(df)
    df = df.drop_duplicates(subset=[key_col])
    df = df.dropna(subset=[key_col])
    after = len(df)
    if before != after:
        log(f"  dropped {before - after} duplicate/null-key rows from dimension on {key_col}")
    return df


def clean_fact_production(df, valid_ids):
    before = len(df)

    # referential integrity: every foreign key must exist in its dimension
    df = df[df["plant_id"].isin(valid_ids["plant_id"])]
    df = df[df["machine_id"].isin(valid_ids["machine_id"])]
    df = df[df["shift_id"].isin(valid_ids["shift_id"])]
    df = df[df["product_id"].isin(valid_ids["product_id"])]
    df = df[df["date_id"].isin(valid_ids["date_id"])]

    # sanity bounds — negative quantities or impossible downtime shouldn't exist,
    # but real-world ETL always has a few, so guard against them explicitly
    df = df[df["produced_qty"] >= 0]
    df = df[df["defective_qty"] >= 0]
    df = df[df["downtime_minutes"].between(0, 480)]
    df = df[df["energy_consumed_kwh"] >= 0]
    df["defective_qty"] = df[["defective_qty", "produced_qty"]].min(axis=1).round().astype(int)

    after = len(df)
    if before != after:
        log(f"  fact_production: dropped {before - after} rows failing validation ({before} -> {after})")
    return df


def main():
    log("Reading source CSVs...")
    dim_plant = pd.read_csv(os.path.join(DATA_DIR, "dim_plant.csv"))
    dim_machine = pd.read_csv(os.path.join(DATA_DIR, "dim_machine.csv"))
    dim_shift = pd.read_csv(os.path.join(DATA_DIR, "dim_shift.csv"))
    dim_product = pd.read_csv(os.path.join(DATA_DIR, "dim_product.csv"))
    dim_date = pd.read_csv(os.path.join(DATA_DIR, "dim_date.csv"), dtype={"date_id": str})
    fact_production = pd.read_csv(os.path.join(DATA_DIR, "fact_production.csv"), dtype={"date_id": str})
    fact_maintenance = pd.read_csv(os.path.join(DATA_DIR, "fact_maintenance.csv"), dtype={"date_id": str})

    log("Cleaning dimensions...")
    dim_plant = clean_dim(dim_plant, "plant_id")
    dim_machine = clean_dim(dim_machine, "machine_id")
    dim_shift = clean_dim(dim_shift, "shift_id")
    dim_product = clean_dim(dim_product, "product_id")
    dim_date = clean_dim(dim_date, "date_id")

    valid_ids = {
        "plant_id": set(dim_plant["plant_id"]),
        "machine_id": set(dim_machine["machine_id"]),
        "shift_id": set(dim_shift["shift_id"]),
        "product_id": set(dim_product["product_id"]),
        "date_id": set(dim_date["date_id"]),
    }

    log("Cleaning and validating fact_production...")
    fact_production = clean_fact_production(fact_production, valid_ids)

    log("Validating fact_maintenance...")
    before = len(fact_maintenance)
    fact_maintenance = fact_maintenance[fact_maintenance["machine_id"].isin(valid_ids["machine_id"])]
    fact_maintenance = fact_maintenance[fact_maintenance["date_id"].isin(valid_ids["date_id"])]
    after = len(fact_maintenance)
    if before != after:
        log(f"  fact_maintenance: dropped {before - after} rows failing referential checks")

    log(f"Building SQLite database at {os.path.abspath(DB_PATH)}...")
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    with open(SCHEMA_PATH) as f:
        conn.executescript(f.read())

    dim_plant.to_sql("dim_plant", conn, if_exists="append", index=False)
    dim_machine.to_sql("dim_machine", conn, if_exists="append", index=False)
    dim_shift.to_sql("dim_shift", conn, if_exists="append", index=False)
    dim_product.to_sql("dim_product", conn, if_exists="append", index=False)
    dim_date.to_sql("dim_date", conn, if_exists="append", index=False)
    fact_production.to_sql("fact_production", conn, if_exists="append", index=False)
    fact_maintenance.to_sql("fact_maintenance", conn, if_exists="append", index=False)
    conn.commit()

    # quick post-load sanity check
    counts = {}
    for t in ["dim_plant", "dim_machine", "dim_shift", "dim_product", "dim_date", "fact_production", "fact_maintenance"]:
        counts[t] = conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
    conn.close()

    log("Load complete. Row counts:")
    for t, c in counts.items():
        log(f"  {t}: {c:,}")


if __name__ == "__main__":
    main()
