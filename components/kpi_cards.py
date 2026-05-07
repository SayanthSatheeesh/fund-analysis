import streamlit as st

def render_kpi_row(metrics):
    """Render a row of styled metric cards."""
    cols = st.columns(len(metrics))
    for i, (label, value, delta) in enumerate(metrics):
        with cols[i]:
            st.metric(label=label, value=value, delta=delta)
