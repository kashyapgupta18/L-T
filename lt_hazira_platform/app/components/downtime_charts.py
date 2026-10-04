"""Visualizations for equipment downtime and Pareto root cause."""
import streamlit as st
import plotly.express as px
import pandas as pd

def render_downtime_breakdown(df: pd.DataFrame):
    st.subheader("Equipment Downtime by Category")
    if "downtime_hours" in df.columns and "machine_type" in df.columns:
        grouped = df.groupby("machine_type")["downtime_hours"].sum().reset_index()
        fig = px.bar(
            grouped,
            x="machine_type",
            y="downtime_hours",
            title="Total Downtime Hours by Machine Type",
            labels={"machine_type": "Machine Type", "downtime_hours": "Hours"},
            color="downtime_hours",
            color_continuous_scale="Reds"
        )
        st.plotly_chart(fig, use_container_width=True)
