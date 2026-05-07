import streamlit as st
from components.theme import apply_custom_theme

st.set_page_config(
    page_title="Fund Index Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_custom_theme()

st.title("📊 Fund Index Analysis Dashboard")

st.markdown("""
### Welcome to the Professional Fund Analysis Portal
This dashboard provides deep insights into fund performance against benchmark indices.

#### Key Features:
- **Trend Analysis**: Compare Fund NAV growth against Index value.
- **Period Performance**: Analyze returns across multiple time horizons.
- **Heatmap Matrix**: Identify monthly performance trends and volatility.

**Select a page from the sidebar to begin your analysis.**
""")

st.info("💡 Tip: Click on chart legends to toggle visibility or double-click to reset view.")

with st.expander("System Documentation"):
    st.write("For detailed technical implementation, refer to `docs/tableau_dev_guide.md`.")
