import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import sys
import os
from sqlalchemy import text

# Add project root to sys.path so we can import db module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db.connection import get_engine

# --- Configuration & Styling ---
st.set_page_config(
    page_title="Fund Index Analysis Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a premium dark corporate theme
st.markdown("""
<style>
    .kpi-card {
        background-color: #1e2130;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        margin-bottom: 20px;
        border: 1px solid #2d3142;
    }
    .kpi-value {
        font-size: 28px;
        font-weight: 700;
        margin: 10px 0;
        color: #e2e8f0;
    }
    .kpi-label {
        font-size: 14px;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .positive-dev { color: #10b981 !important; }
    .negative-dev { color: #ef4444 !important; }
    .watch-listed {
        background-color: rgba(239, 68, 68, 0.2);
        color: #ef4444;
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: bold;
        border: 1px solid #ef4444;
    }
    .safe {
        background-color: rgba(16, 185, 129, 0.2);
        color: #10b981;
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: bold;
        border: 1px solid #10b981;
    }
</style>
""", unsafe_allow_html=True)

# --- Data Loading ---
@st.cache_data(ttl=3600) # Cache for 1 hour
def load_data():
    engine = get_engine()
    
    # Check if tables/views exist first (to avoid errors if pipeline hasn't run)
    try:
        with engine.connect() as conn:
            # Query the views directly
            v_trend_history = pd.read_sql("SELECT * FROM v_trend_history", conn)
            v_period_performance = pd.read_sql("SELECT * FROM v_period_performance", conn)
            v_monthly_comparison = pd.read_sql("SELECT * FROM v_monthly_comparison", conn)
            
            # Convert date columns
            v_trend_history['full_date'] = pd.to_datetime(v_trend_history['full_date'])
            
            return v_trend_history, v_period_performance, v_monthly_comparison
    except Exception as e:
        st.error(f"Database Error: Could not load views. Have you run the pipeline? Error: {e}")
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

df_trend, df_period, df_monthly = load_data()

if df_trend.empty:
    st.warning("No data available. Please ensure your database is populated and views are created.")
    st.stop()

# --- Sidebar Navigation & Slicers ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/b/b1/Tata_Consultancy_Services_Logo.svg/512px-Tata_Consultancy_Services_Logo.svg.png", width=150)
    st.markdown("### Navigation")
    page = st.radio("Select Page", ["1. Summary Dashboard", "2. Fund Detail", "3. Multi-Fund Comparison"])
    
    st.markdown("---")
    st.markdown("### Global Filters")
    
    # Global Slicers
    available_indices = df_trend['index_name'].unique().tolist()
    selected_index = st.selectbox("Index Category", ["All"] + available_indices)
    
    # Date Range
    min_date = df_trend['full_date'].min().date()
    max_date = df_trend['full_date'].max().date()
    date_range = st.date_input("Date Range", [min_date, max_date], min_value=min_date, max_value=max_date)

# Apply Global Filters to Trend Data
filtered_trend = df_trend.copy()
if selected_index != "All":
    filtered_trend = filtered_trend[filtered_trend['index_name'] == selected_index]
if len(date_range) == 2:
    filtered_trend = filtered_trend[(filtered_trend['full_date'].dt.date >= date_range[0]) & 
                                    (filtered_trend['full_date'].dt.date <= date_range[1])]

# --- Page 1: Summary Dashboard ---
if page == "1. Summary Dashboard":
    st.title("📈 Market Summary Dashboard")
    
    # Calculate KPIs based on the latest available date in the filtered data
    if not filtered_trend.empty:
        latest_date = filtered_trend['full_date'].max()
        latest_data = filtered_trend[filtered_trend['full_date'] == latest_date]
        
        # Aggregate logic (averaging if multiple funds/indices selected)
        latest_nav = latest_data['nav_price'].mean()
        latest_idx = latest_data['index_price'].mean()
        
        # Calculate deviation %
        if not df_period.empty:
            # Get overall period performance for deviation
            period_data = df_period.copy()
            if selected_index != "All":
                # Note: v_period_performance might not have index_name, assume we map it or aggregate generally
                pass
            
            avg_fund_ret = period_data['fund_return'].mean()
            avg_idx_ret = period_data['index_return'].mean()
            deviation = avg_fund_ret - avg_idx_ret
        else:
            deviation = 0.0

        # KPI Display
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Latest Avg NAV Price</div>
                <div class="kpi-value">₹ {latest_nav:,.2f}</div>
                <div class="kpi-label">As of {latest_date.strftime('%Y-%m-%d')}</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Latest Avg Index Price</div>
                <div class="kpi-value">₹ {latest_idx:,.2f}</div>
                <div class="kpi-label">Benchmark</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col3:
            dev_class = "positive-dev" if deviation >= 0 else "negative-dev"
            dev_icon = "▲" if deviation >= 0 else "▼"
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Overall Deviation (Alpha)</div>
                <div class="kpi-value {dev_class}">{dev_icon} {deviation:.2f}%</div>
                <div class="kpi-label">Fund vs Index Return</div>
            </div>
            """, unsafe_allow_html=True)

        # Dual-Axis Trend Chart
        st.markdown("### Price Trend History")
        
        # Group by date to show aggregate trend
        trend_agg = filtered_trend.groupby('full_date').agg({
            'nav_price': 'mean',
            'index_price': 'mean'
        }).reset_index()
        
        fig = go.Figure()
        
        # Add NAV Line
        fig.add_trace(go.Scatter(
            x=trend_agg['full_date'], y=trend_agg['nav_price'],
            name="NAV Price",
            line=dict(color="#3b82f6", width=2)
        ))
        
        # Add Index Line
        fig.add_trace(go.Scatter(
            x=trend_agg['full_date'], y=trend_agg['index_price'],
            name="Index Price",
            yaxis="y2",
            line=dict(color="#8b5cf6", width=2, dash="dot")
        ))
        
        # Layout for dual axis
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#e2e8f0"),
            xaxis=dict(showgrid=True, gridcolor="#334155", title="Date"),
            yaxis=dict(title="NAV Price", showgrid=True, gridcolor="#334155"),
            yaxis2=dict(title="Index Price", overlaying="y", side="right", showgrid=False),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=0, r=0, t=50, b=0)
        )
        
        st.plotly_chart(fig, use_container_width=True)

# --- Page 2: Fund Detail ---
elif page == "2. Fund Detail":
    st.title("🔍 Fund Detail Analysis")
    
    col_sel1, col_sel2 = st.columns([1, 2])
    with col_sel1:
        # Fund Drill-through selector
        available_funds = df_period['fund_id'].unique().tolist()
        selected_fund = st.selectbox("Select Fund (Drill-through)", available_funds)
    
    if selected_fund:
        fund_data = df_period[df_period['fund_id'] == selected_fund]
        
        with col_sel2:
            st.markdown("<br>", unsafe_allow_html=True) # Spacer
            # Watch List Indicator
            is_watch_listed = fund_data['is_watch_listed'].iloc[0] if not fund_data.empty else 'NO'
            if is_watch_listed == 'YES':
                st.markdown('<span class="watch-listed">⚠️ WARNING: ON WATCH LIST</span>', unsafe_allow_html=True)
            else:
                st.markdown('<span class="safe">✅ STATUS: HEALTHY</span>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Bar Chart: Period Performance Comparison
        st.markdown(f"### Performance Comparison: {selected_fund}")
        
        # Transform data for Plotly grouped bar chart
        periods = fund_data['period'].tolist()
        fund_returns = fund_data['fund_return'].tolist()
        index_returns = fund_data['index_return'].tolist()
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=periods, y=fund_returns,
            name='Fund Return (%)',
            marker_color='#10b981'
        ))
        fig.add_trace(go.Bar(
            x=periods, y=index_returns,
            name='Index Return (%)',
            marker_color='#64748b'
        ))
        
        fig.update_layout(
            barmode='group',
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#e2e8f0"),
            xaxis=dict(showgrid=False, title="Period"),
            yaxis=dict(showgrid=True, gridcolor="#334155", title="Return (%)"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        st.plotly_chart(fig, use_container_width=True)

# --- Page 3: Multi-Fund Comparison ---
elif page == "3. Multi-Fund Comparison":
    st.title("📊 Multi-Fund Matrix")
    st.markdown("Compare monthly returns across all funds.")
    
    # Pivot the monthly data for the matrix visual
    if not df_monthly.empty:
        # Ensure year_month is sorted properly
        df_monthly['year_month_sort'] = pd.to_datetime(df_monthly['year_month'], format='%Y-%m', errors='coerce')
        df_monthly = df_monthly.sort_values('year_month_sort')
        
        pivot_df = df_monthly.pivot(index='fund_id', columns='year_month', values='monthly_return')
        
        # Apply conditional formatting (Red-Yellow-Green)
        def color_returns(val):
            if pd.isna(val):
                return ''
            if val > 0:
                return 'background-color: rgba(16, 185, 129, 0.2); color: #10b981;'
            elif val < 0:
                return 'background-color: rgba(239, 68, 68, 0.2); color: #ef4444;'
            return 'background-color: rgba(245, 158, 11, 0.2); color: #f59e0b;'
        
        styled_df = pivot_df.style.map(color_returns).format("{:.2f}%", na_rep="-")
        
        st.dataframe(styled_df, use_container_width=True, height=600)
        
        # Export Button
        csv = pivot_df.to_csv().encode('utf-8')
        st.download_button(
            label="⬇️ Export Data to CSV",
            data=csv,
            file_name='multi_fund_comparison.csv',
            mime='text/csv',
        )
