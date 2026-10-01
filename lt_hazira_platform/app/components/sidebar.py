"""Sidebar navigation and dynamic filtering controls."""
import streamlit as st
from typing import List, Tuple

def render_sidebar_filters(plants: List[str], machine_types: List[str]) -> Tuple[str, str]:
    st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/e/e5/L%26T.png", width=120) if False else None
    st.sidebar.title("Operational Controls")
    st.sidebar.markdown("---")
    
    selected_plant = st.sidebar.selectbox("Select Plant Facility", ["All Plants"] + sorted(plants))
    selected_type = st.sidebar.selectbox("Machine Classification", ["All Machine Types"] + sorted(machine_types))
    
    st.sidebar.markdown("---")
    st.sidebar.caption("L&T Hazira Smart Manufacturing v1.0.0")
    return selected_plant, selected_type
