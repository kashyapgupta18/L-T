"""KPI metric card renderer for Streamlit."""
import streamlit as st
from typing import Dict, Any

def render_kpi_cards(metrics: Dict[str, Any]):
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric(label="Total Production", value=f"{metrics.get('total_units', 0):,}", delta=f"{metrics.get('unit_delta', '+2.4%')}")
    with c2:
        st.metric(label="Plant OEE", value=f"{metrics.get('oee_pct', 82.5):.1f}%", delta=f"{metrics.get('oee_delta', '+1.1%')}")
    with c3:
        st.metric(label="Total Downtime", value=f"{metrics.get('downtime_hours', 142.0):.1f}h", delta=f"{metrics.get('downtime_delta', '-4.5h')}")
    with c4:
        st.metric(label="Critical Risk Assets", value=f"{metrics.get('critical_count', 2)}", delta="Urgent", delta_color="inverse")
