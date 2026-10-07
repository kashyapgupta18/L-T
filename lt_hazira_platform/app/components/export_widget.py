"""Dataset export and report download controls."""
import streamlit as st
import pandas as pd

def render_export_controls(df: pd.DataFrame, report_name: str = "hazira_analytics"):
    st.markdown("### Export Analytics Data")
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label=f"Download {report_name}.csv",
        data=csv,
        file_name=f"{report_name}.csv",
        mime="text/csv"
    )
