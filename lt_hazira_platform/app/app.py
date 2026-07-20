"""
L&T Hazira Smart Manufacturing Analytics — exploration app.

Filter by plant, machine, and date range; view production, downtime, energy,
and quality KPIs; inspect the failure-prediction model's feature importances
and honest performance numbers.

Run:
    streamlit run app.py
"""

import os
import sqlite3
import pandas as pd
import plotly.express as px
import streamlit as st


BASE = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE, "..", "data", "hazira_manufacturing.db")

st.set_page_config(page_title="Hazira Smart Manufacturing Analytics", page_icon="⚙️", layout="wide")


@st.cache_data
def load_data():
    conn = sqlite3.connect(DB_PATH)
    fact = pd.read_sql("""
        SELECT f.*, p.plant_name, p.city, m.machine_name, m.machine_type,
               d.date, d.year, d.month, d.day_of_week, d.is_weekend,
               pr.product_name, pr.category, s.shift_name
        FROM fact_production f
        JOIN dim_plant p ON f.plant_id = p.plant_id
        JOIN dim_machine m ON f.machine_id = m.machine_id
        JOIN dim_date d ON f.date_id = d.date_id
        JOIN dim_product pr ON f.product_id = pr.product_id
        JOIN dim_shift s ON f.shift_id = s.shift_id
    """, conn)
    maint = pd.read_sql("""
        SELECT fm.*, m.machine_name, m.plant_id, p.plant_name
        FROM fact_maintenance fm
        JOIN dim_machine m ON fm.machine_id = m.machine_id
        JOIN dim_plant p ON m.plant_id = p.plant_id
    """, conn)
    conn.close()
    fact["date"] = pd.to_datetime(fact["date"])
    return fact, maint


if not os.path.exists(DB_PATH):
    st.error(f"Database not found at {DB_PATH}. Run etl/generate_data.py then etl/load_to_sql.py first.")
    st.stop()

fact, maint = load_data()

st.sidebar.title("⚙️ Filters")
plants = st.sidebar.multiselect("Plant", sorted(fact["plant_name"].unique()), default=sorted(fact["plant_name"].unique()))
machine_types = st.sidebar.multiselect("Machine type", sorted(fact["machine_type"].unique()), default=sorted(fact["machine_type"].unique()))
date_range = st.sidebar.date_input(
    "Date range",
    value=(fact["date"].min().date(), fact["date"].max().date()),
    min_value=fact["date"].min().date(),
    max_value=fact["date"].max().date(),
)

if len(date_range) == 2:
    start, end = date_range
else:
    start, end = fact["date"].min().date(), fact["date"].max().date()

mask = (
    fact["plant_name"].isin(plants)
    & fact["machine_type"].isin(machine_types)
    & (fact["date"].dt.date >= start)
    & (fact["date"].dt.date <= end)
)
df = fact[mask]

st.title("L&T Hazira Smart Manufacturing Analytics")
st.caption("Synthetic dataset built for portfolio/demo purposes — not real L&T operational data. See README.")

if df.empty:
    st.warning("No data matches the current filters.")
    st.stop()

# ---------------------------------------------------------------------------
# KPI row
# ---------------------------------------------------------------------------
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Units Produced", f"{df['produced_qty'].sum():,.0f}")
c2.metric("Avg Downtime / Shift", f"{df['downtime_minutes'].mean():.1f} min")
c3.metric("Defect Rate", f"{(df['defective_qty'].sum() / df['produced_qty'].sum() * 100):.2f}%")
c4.metric("Total Energy", f"{df['energy_consumed_kwh'].sum():,.0f} kWh")
c5.metric("Failure Events", f"{int(df['failure_event'].sum())}")

st.divider()

tab1, tab2, tab3, tab4 = st.tabs(["Production & Quality", "Downtime & Energy", "Maintenance", "Failure Model"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        trend = df.groupby(df["date"].dt.to_period("W").astype(str))["produced_qty"].sum().reset_index()
        trend.columns = ["week", "produced_qty"]
        fig = px.line(trend, x="week", y="produced_qty", title="Weekly production volume")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        by_cat = df.groupby("category")["produced_qty"].sum().reset_index().sort_values("produced_qty", ascending=False)
        fig = px.bar(by_cat, x="category", y="produced_qty", title="Production by product category")
        st.plotly_chart(fig, use_container_width=True)

    by_plant = df.groupby("plant_name").agg(
        produced=("produced_qty", "sum"),
        defect_rate=("defective_qty", "sum"),
        produced_total=("produced_qty", "sum"),
    ).reset_index()
    by_plant["defect_rate_pct"] = by_plant["defect_rate"] / by_plant["produced_total"] * 100
    fig = px.bar(by_plant, x="plant_name", y="defect_rate_pct", title="Defect rate by plant (%)")
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    col1, col2 = st.columns(2)
    with col1:
        top_energy = df.groupby("machine_name")["energy_consumed_kwh"].sum().reset_index().sort_values(
            "energy_consumed_kwh", ascending=False).head(10)
        fig = px.bar(top_energy, x="machine_name", y="energy_consumed_kwh",
                     title="Top 10 machines by total energy consumption")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        downtime_by_type = df.groupby("machine_type")["downtime_minutes"].mean().reset_index().sort_values(
            "downtime_minutes", ascending=False)
        fig = px.bar(downtime_by_type, x="machine_type", y="downtime_minutes",
                     title="Average downtime per shift by machine type")
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Ask a direct question of the data")
    st.caption("e.g. 'Which manufacturing unit had the highest energy consumption?' — answered directly below, no LLM needed for numeric lookups like this.")
    top_machine = df.groupby("machine_name")["energy_consumed_kwh"].sum().idxmax()
    top_value = df.groupby("machine_name")["energy_consumed_kwh"].sum().max()
    st.info(f"**Highest energy consumption in the current filter:** {top_machine} — {top_value:,.0f} kWh total.")

with tab3:
    m_mask = maint["plant_name"].isin(plants)
    mdf = maint[m_mask]
    col1, col2 = st.columns(2)
    with col1:
        cost_by_type = mdf.groupby("maintenance_type")["cost_inr"].sum().reset_index()
        fig = px.pie(cost_by_type, names="maintenance_type", values="cost_inr", title="Maintenance cost: preventive vs corrective")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        cost_by_plant = mdf.groupby("plant_name")["cost_inr"].sum().reset_index().sort_values("cost_inr", ascending=False)
        fig = px.bar(cost_by_plant, x="plant_name", y="cost_inr", title="Maintenance cost by plant (INR)")
        st.plotly_chart(fig, use_container_width=True)
    st.dataframe(mdf.sort_values("cost_inr", ascending=False).head(20)[
        ["maintenance_id", "machine_name", "plant_name", "maintenance_type", "duration_minutes", "cost_inr", "technician_team"]
    ], use_container_width=True)

with tab4:
    st.subheader("Machine failure risk model")

    # Feature columns from the trained HistGradientBoostingClassifier model
    # (extracted from data/failure_model.joblib — hardcoded here to avoid
    # pickle compatibility issues across Python versions on Streamlit Cloud)
    MODEL_FEATURE_COLUMNS = [
        "planned_qty", "prior_wear", "prior_downtime_avg3",
        "rated_capacity_units_per_hour", "base_energy_kwh_per_hour", "is_weekend",
        "machine_type_CNC Plate Cutting", "machine_type_Heat Treatment Furnace",
        "machine_type_Heavy Press Forming", "machine_type_Rolling Mill",
        "machine_type_Shot Blasting Unit", "machine_type_Sub-arc Welding Station",
        "machine_type_Welding Robot Cell", "shift_id_S2", "shift_id_S3",
        "plant_id_P02", "plant_id_P03", "plant_id_P04", "plant_id_P05",
    ]

    st.write(
        "This model predicts failure risk using only information known **before** a shift starts "
        "(machine wear history, recent downtime pattern, machine specs) — it does not use the current "
        "shift's own downtime or defect numbers, since those are a consequence of a failure, not a "
        "predictor of one."
    )
    st.markdown(
        "**Honest result:** on held-out data this model gets ROC-AUC ≈ 0.49 — essentially no better "
        "than a coin flip. That's a real finding, not a bug: with only wear-index history and no true "
        "sensor telemetry (vibration, temperature, acoustic data), there isn't enough signal in this "
        "synthetic dataset to predict rare failure events (1.45% of shifts) reliably. A production version "
        "of this would need actual condition-monitoring sensor data, not just aggregate wear stats."
    )
    st.write("Feature columns used:")
    st.code(", ".join(MODEL_FEATURE_COLUMNS))
