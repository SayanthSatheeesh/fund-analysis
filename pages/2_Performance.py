import streamlit as st
from data.db import load_data
from components.charts import build_performance_bar
from components.kpi_cards import render_kpi_row
from components.theme import apply_custom_theme

apply_custom_theme()

st.title("⏱ Period Performance")

# Load Data
df = load_data("v_period_performance")

# KPIs for top fund
top_perf = df.iloc[0]
kpis = [
    ("1M Return", f"{top_perf['fund_return']*100:.2f}%", None),
    ("1Y Return", f"{df[df['period']=='1Y']['fund_return'].values[0]*100:.2f}%", None),
    ("Tracking Error", "0.045", "Low")
]
render_kpi_row(kpis)

st.markdown("### Comparison vs Benchmark")
st.plotly_chart(build_performance_bar(df), use_container_width=True)

st.dataframe(df, use_container_width=True)
