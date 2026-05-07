import streamlit as st
from data.db import load_data
from components.charts import build_heatmap
from components.theme import apply_custom_theme

apply_custom_theme()

st.title("🌡 Performance Heatmap")

# Load Data
df = load_data("v_monthly_comparison")

st.markdown("### Monthly Returns (%) Matrix")
st.plotly_chart(build_heatmap(df), use_container_width=True)

st.info("The heatmap uses a Red-Yellow-Green scale to highlight high and low performance periods.")
