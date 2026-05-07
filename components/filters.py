import streamlit as st

def sidebar_filters(funds, indices):
    """Render sidebar filters and return selected values."""
    st.sidebar.header("Navigation & Filters")
    
    selected_index = st.sidebar.selectbox("Select Index", indices)
    selected_fund = st.sidebar.selectbox("Select Fund", funds)
    
    date_range = st.sidebar.date_input("Date Range", [])
    
    st.sidebar.markdown("---")
    st.sidebar.info("Data updates automatically every 5 minutes.")
    
    return selected_fund, selected_index, date_range
