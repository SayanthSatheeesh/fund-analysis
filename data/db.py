import streamlit as st
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import os

def get_connection():
    """Create a SQLAlchemy engine for PostgreSQL."""
    try:
        # Check for secrets/env vars
        db_config = st.secrets.get("postgres", {})
        if not db_config:
            # Fallback to local env or defaults
            host = os.getenv("DB_HOST", "localhost")
            port = os.getenv("DB_PORT", "5432")
            dbname = os.getenv("DB_NAME", "fund_analysis")
            user = os.getenv("DB_USER", "postgres")
            password = os.getenv("DB_PASSWORD", "newpassword")
        else:
            host = db_config["host"]
            port = db_config["port"]
            dbname = db_config["dbname"]
            user = db_config["user"]
            password = db_config["password"]

        engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{dbname}")
        return engine
    except Exception as e:
        st.sidebar.error(f"DB Connection Error: {e}")
        return None

@st.cache_data(ttl=300)
def load_data(view_name):
    """Load data from a database view with CSV fallback."""
    engine = get_connection()
    if engine:
        try:
            query = f"SELECT * FROM {view_name}"
            df = pd.read_sql(query, engine)
            return df
        except Exception as e:
            st.sidebar.warning(f"Error querying {view_name}: {e}. Loading sample data.")
    
    return load_sample_data(view_name)

def load_sample_data(view_name):
    """Generate or load sample data for demo purposes."""
    dates = pd.date_range(start="2023-01-01", end="2024-05-01", freq="D")
    
    if view_name == "v_trend_history":
        data = {
            "full_date": dates,
            "nav_price": 100 + np.cumsum(np.random.normal(0.1, 0.5, len(dates))),
            "index_price": 20000 + np.cumsum(np.random.normal(10, 100, len(dates))),
            "fund_id": "FUND_A",
            "index_name": "NIFTY 50"
        }
        return pd.DataFrame(data)
    
    elif view_name == "v_period_performance":
        periods = ["1M", "3M", "6M", "1Y", "YTD"]
        data = {
            "period": periods,
            "fund_return": np.random.uniform(-0.02, 0.1, len(periods)),
            "index_return": np.random.uniform(-0.01, 0.08, len(periods)),
            "fund_id": ["FUND_A"] * len(periods)
        }
        return pd.DataFrame(data)
    
    elif view_name == "v_monthly_comparison":
        months = pd.date_range(start="2023-01-01", end="2024-05-01", freq="MS")
        funds = ["FUND_A", "FUND_B", "FUND_C"]
        data = []
        for fund in funds:
            for month in months:
                data.append({
                    "fund_id": fund,
                    "year_month": month.strftime("%Y-%m"),
                    "monthly_return": np.random.uniform(-0.05, 0.1)
                })
        return pd.DataFrame(data)
    
    return pd.DataFrame()
