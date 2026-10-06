"""Visualizations for production output and defect rates."""
import streamlit as st
import plotly.express as px
import pandas as pd

def render_production_trends(df: pd.DataFrame):
    st.subheader("Production Throughput & Output Trends")
    if "date_id" in df.columns and "units_produced" in df.columns:
        daily = df.groupby("date_id").agg(
            total_produced=("units_produced", "sum"),
            total_defects=("units_defective", "sum")
        ).reset_index()
        fig = px.line(
            daily,
            x="date_id",
            y=["total_produced", "total_defects"],
            title="Daily Production Output vs Defect Count",
            labels={"value": "Units", "date_id": "Day Index", "variable": "Metric"}
        )
        st.plotly_chart(fig, use_container_width=True)
