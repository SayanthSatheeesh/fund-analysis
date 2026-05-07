import streamlit as st
from data.db import load_data
from components.charts import build_trend_chart
from components.filters import sidebar_filters
from components.kpi_cards import render_kpi_row
from components.theme import apply_custom_theme

apply_custom_theme()

st.title("📈 Trend Analysis")

# Load Data
df = load_data("v_trend_history")

# Filters
funds = df['fund_id'].unique()
indices = df['index_name'].unique()
selected_fund, selected_index, date_range = sidebar_filters(funds, indices)

# Filter Data
filtered_df = df[(df['fund_id'] == selected_fund) & (df['index_name'] == selected_index)]

# KPIs
latest = filtered_df.iloc[-1]
prev = filtered_df.iloc[-2]
kpis = [
    ("Latest NAV", f"₹{latest['nav_price']:.2f}", f"{latest['nav_price'] - prev['nav_price']:.2f}"),
    ("Index Value", f"{latest['index_price']:.0f}", f"{latest['index_price'] - prev['index_price']:.0f}"),
    ("Active Return", f"{(latest['nav_price']/prev['nav_price'] - 1)*100:.2f}%", None)
]
render_kpi_row(kpis)

# Chart
st.plotly_chart(build_trend_chart(filtered_df, selected_fund, selected_index), use_container_width=True)
