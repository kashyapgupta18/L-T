"""
Generates a synthetic manufacturing dataset modeled after a heavy engineering
plant like L&T's Hazira Manufacturing Complex: multiple plants, multiple
machines per plant, shift-wise production, quality, downtime, energy, and
maintenance records.

This is NOT real L&T data — L&T doesn't publish machine-level production
figures publicly, and nobody outside the company has access to them. This is
a realistic synthetic dataset built to demonstrate the analytics pipeline
end to end. Say this plainly if anyone asks; claiming it's real operational
data would be misrepresentation.

Run:
    python generate_data.py
Outputs CSVs into ../data/
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import os

rng = np.random.default_rng(42)

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(OUT_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# Dimension: Plants
# ---------------------------------------------------------------------------
plants = pd.DataFrame([
    {"plant_id": "P01", "plant_name": "Hazira Heavy Engineering", "city": "Surat", "state": "Gujarat", "plant_type": "Heavy Fabrication"},
    {"plant_id": "P02", "plant_name": "Hazira Process Equipment", "city": "Surat", "state": "Gujarat", "plant_type": "Process Equipment"},
    {"plant_id": "P03", "plant_name": "Hazira Modular Fabrication", "city": "Surat", "state": "Gujarat", "plant_type": "Modular Fabrication"},
    {"plant_id": "P04", "plant_name": "Powai Precision Unit", "city": "Mumbai", "state": "Maharashtra", "plant_type": "Precision Machining"},
    {"plant_id": "P05", "plant_name": "Coimbatore Components Unit", "city": "Coimbatore", "state": "Tamil Nadu", "plant_type": "Component Manufacturing"},
])

# ---------------------------------------------------------------------------
# Dimension: Machines (8 per plant, 40 total)
# ---------------------------------------------------------------------------
machine_types = [
    ("CNC Plate Cutting", 4.0, 60),
    ("Heavy Press Forming", 3.2, 90),
    ("Welding Robot Cell", 5.5, 45),
    ("Shot Blasting Unit", 6.0, 30),
    ("Sub-arc Welding Station", 4.8, 55),
    ("Rolling Mill", 7.2, 40),
    ("CNC Machining Center", 3.8, 65),
    ("Heat Treatment Furnace", 8.5, 25),
]

machine_rows = []
mid = 1
for _, prow in plants.iterrows():
    for i, (mtype, base_energy, base_capacity) in enumerate(machine_types):
        install_offset_days = int(rng.integers(365, 365 * 12))
        machine_rows.append({
            "machine_id": f"M{mid:03d}",
            "plant_id": prow["plant_id"],
            "machine_name": f"{mtype} #{i+1}",
            "machine_type": mtype,
            "install_date": (datetime(2026, 3, 31) - timedelta(days=install_offset_days)).date().isoformat(),
            "rated_capacity_units_per_hour": round(base_capacity * rng.uniform(0.85, 1.15), 1),
            "base_energy_kwh_per_hour": round(base_energy * rng.uniform(0.9, 1.1), 2),
        })
        mid += 1
machines = pd.DataFrame(machine_rows)

# ---------------------------------------------------------------------------
# Dimension: Shifts
# ---------------------------------------------------------------------------
shifts = pd.DataFrame([
    {"shift_id": "S1", "shift_name": "Morning", "start_time": "06:00", "end_time": "14:00"},
    {"shift_id": "S2", "shift_name": "Afternoon", "start_time": "14:00", "end_time": "22:00"},
    {"shift_id": "S3", "shift_name": "Night", "start_time": "22:00", "end_time": "06:00"},
])

# ---------------------------------------------------------------------------
# Dimension: Products
# ---------------------------------------------------------------------------
products = pd.DataFrame([
    {"product_id": "PR01", "product_name": "Pressure Vessel Shell", "category": "Process Equipment", "uom": "Units"},
    {"product_id": "PR02", "product_name": "Structural Steel Module", "category": "Heavy Fabrication", "uom": "Units"},
    {"product_id": "PR03", "product_name": "Heat Exchanger Bundle", "category": "Process Equipment", "uom": "Units"},
    {"product_id": "PR04", "product_name": "Reactor Component", "category": "Precision Machining", "uom": "Units"},
    {"product_id": "PR05", "product_name": "Piping Spool", "category": "Modular Fabrication", "uom": "Units"},
]).sample(frac=1, random_state=1).reset_index(drop=True)

# ---------------------------------------------------------------------------
# Dimension: Date (210 days -> ~7 months of daily records)
# ---------------------------------------------------------------------------
start_date = datetime(2025, 9, 1)
n_days = 210
dates = pd.DataFrame({"date": [start_date + timedelta(days=i) for i in range(n_days)]})
dates["date_id"] = dates["date"].dt.strftime("%Y%m%d")
dates["year"] = dates["date"].dt.year
dates["quarter"] = dates["date"].dt.quarter
dates["month"] = dates["date"].dt.month
dates["day"] = dates["date"].dt.day
dates["day_of_week"] = dates["date"].dt.day_name()
dates["is_weekend"] = dates["date"].dt.dayofweek >= 5
dates["date"] = dates["date"].dt.date.astype(str)

# ---------------------------------------------------------------------------
# Fact: Production (machine x day x shift)
# Target: ~40 machines x 3 shifts x 210 days = 25,200 rows
# ---------------------------------------------------------------------------
records = []
record_id = 1

# per-machine "health" trajectory so failures aren't pure noise - a machine
# accumulates wear, gets serviced, wear drops, and so on. This makes the
# eventual ML failure-prediction task learnable instead of random.
machine_wear = {m: rng.uniform(0.05, 0.2) for m in machines["machine_id"]}
machine_age_days = {
    m: (datetime(2025, 9, 1).date() - datetime.fromisoformat(d).date()).days
    for m, d in zip(machines["machine_id"], machines["install_date"])
}

maintenance_records = []
maint_id = 1

for date_row in dates.itertuples():
    for _, mrow in machines.iterrows():
        m_id = mrow["machine_id"]
        wear = machine_wear[m_id]

        # daily wear accumulation
        wear += rng.uniform(0.001, 0.006)
        wear = min(wear, 0.98)

        for _, srow in shifts.iterrows():
            plant_id = mrow["plant_id"]
            product = products.sample(1, random_state=int(rng.integers(0, 1_000_000))).iloc[0]

            planned_qty = mrow["rated_capacity_units_per_hour"] * 8 * rng.uniform(0.85, 1.0)

            # downtime increases with wear, with occasional spikes representing failures
            base_downtime = rng.gamma(shape=1.5, scale=8) * (1 + wear * 2)
            failure_event = rng.random() < (0.01 + wear * 0.05)
            downtime_minutes = base_downtime + (rng.uniform(90, 240) if failure_event else 0)
            downtime_minutes = min(downtime_minutes, 480)

            effective_hours = max(0, 8 - downtime_minutes / 60)
            produced_qty = max(0, planned_qty * (effective_hours / 8) * rng.uniform(0.92, 1.03))

            defect_rate = 0.01 + wear * 0.04 + rng.uniform(-0.005, 0.01)
            defect_rate = max(0, defect_rate)
            defective_qty = round(produced_qty * defect_rate)

            energy_kwh = mrow["base_energy_kwh_per_hour"] * effective_hours * rng.uniform(0.95, 1.15) * (1 + wear * 0.3)

            records.append({
                "record_id": record_id,
                "date_id": date_row.date_id,
                "plant_id": plant_id,
                "machine_id": m_id,
                "shift_id": srow["shift_id"],
                "product_id": product["product_id"],
                "planned_qty": round(planned_qty, 1),
                "produced_qty": round(produced_qty, 1),
                "defective_qty": int(defective_qty),
                "downtime_minutes": round(downtime_minutes, 1),
                "energy_consumed_kwh": round(energy_kwh, 2),
                "failure_event": bool(failure_event),
                "machine_wear_index": round(wear, 4),
            })
            record_id += 1

            if failure_event:
                maintenance_records.append({
                    "maintenance_id": f"MT{maint_id:05d}",
                    "machine_id": m_id,
                    "date_id": date_row.date_id,
                    "maintenance_type": "Corrective",
                    "duration_minutes": round(rng.uniform(120, 360), 0),
                    "cost_inr": round(rng.uniform(15000, 120000), 0),
                    "technician_team": rng.choice(["Team A", "Team B", "Team C", "Team D"]),
                })
                maint_id += 1
                wear = max(0.02, wear * rng.uniform(0.2, 0.4))  # service resets wear down

        machine_wear[m_id] = wear

    # scheduled preventive maintenance, roughly weekly per machine at random
    if date_row.Index % 7 == 0:
        for _, mrow in machines.sample(frac=0.15, random_state=int(rng.integers(0, 1_000_000))).iterrows():
            maintenance_records.append({
                "maintenance_id": f"MT{maint_id:05d}",
                "machine_id": mrow["machine_id"],
                "date_id": date_row.date_id,
                "maintenance_type": "Preventive",
                "duration_minutes": round(rng.uniform(60, 180), 0),
                "cost_inr": round(rng.uniform(5000, 30000), 0),
                "technician_team": rng.choice(["Team A", "Team B", "Team C", "Team D"]),
            })
            maint_id += 1
            machine_wear[mrow["machine_id"]] = max(0.02, machine_wear[mrow["machine_id"]] * rng.uniform(0.3, 0.5))

fact_production = pd.DataFrame(records)
fact_maintenance = pd.DataFrame(maintenance_records)

# ---------------------------------------------------------------------------
# Save everything
# ---------------------------------------------------------------------------
plants.to_csv(os.path.join(OUT_DIR, "dim_plant.csv"), index=False)
machines.to_csv(os.path.join(OUT_DIR, "dim_machine.csv"), index=False)
shifts.to_csv(os.path.join(OUT_DIR, "dim_shift.csv"), index=False)
products.to_csv(os.path.join(OUT_DIR, "dim_product.csv"), index=False)
dates.to_csv(os.path.join(OUT_DIR, "dim_date.csv"), index=False)
fact_production.to_csv(os.path.join(OUT_DIR, "fact_production.csv"), index=False)
fact_maintenance.to_csv(os.path.join(OUT_DIR, "fact_maintenance.csv"), index=False)

print(f"fact_production: {len(fact_production):,} rows")
print(f"fact_maintenance: {len(fact_maintenance):,} rows")
print(f"machines: {len(machines)}, plants: {len(plants)}, days: {n_days}")
print("CSV files written to", os.path.abspath(OUT_DIR))
