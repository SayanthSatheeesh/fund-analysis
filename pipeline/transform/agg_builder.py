import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sqlalchemy import text
from db.connection import get_engine

def build_agg_period_returns():
    print("Building Period Returns Aggregate...")
    engine = get_engine()
    df = pd.read_sql("SELECT * FROM fact_nav_history", engine)
    
    if df.empty:
        return

    # Sort to ensure latest is last
    df = df.sort_values(['fund_sk', 'date_id'])
    
    results = []
    periods = {
        '1M': 30,
        '1Y': 365,
        '3Y': 365 * 3,
        '5Y': 365 * 5,
        'INCEPTION': 99999
    }
    
    for fund_sk, group in df.groupby('fund_sk'):
        latest_nav = group.iloc[-1]['nav_price']
        latest_index = group.iloc[-1]['index_price']
        index_sk = group.iloc[-1]['index_sk']
        
        for p_name, days in periods.items():
            # Filter for the period
            if p_name == 'INCEPTION':
                p_df = group
            else:
                # Approximate date search
                cutoff = group.iloc[-1]['date_id'] - (days // 365 * 10000 + days % 365) # Very rough YYYYMMDD math
                # Better: get actual date
                latest_date_id = int(float(group.iloc[-1]['date_id']))
                latest_date = datetime.strptime(str(latest_date_id), '%Y%m%d')
                cutoff_date = (latest_date - timedelta(days=days)).strftime('%Y%m%d')
                p_df = group[group['date_id'] >= int(cutoff_date)]
            
            if len(p_df) > 1:
                start_nav = p_df.iloc[0]['nav_price']
                start_index = p_df.iloc[0]['index_price']
                
                f_ret = (latest_nav / start_nav) - 1
                i_ret = (latest_index / start_index) - 1
                
                results.append({
                    'fund_sk': int(fund_sk),
                    'index_sk': int(index_sk),
                    'period': p_name,
                    'fund_return': float(f_ret),
                    'index_return': float(i_ret),
                    'excess_return': float(f_ret - i_ret)
                })
    
    if results:
        res_df = pd.DataFrame(results)
        res_df.to_sql('agg_period_returns', engine, if_exists='replace', index=False)
        print(f"Period Returns Aggregate built with {len(res_df)} records.")

def build_agg_monthly_trends():
    print("Building Monthly Trends Aggregate...")
    engine = get_engine()
    df = pd.read_sql("""
        SELECT f.*, d.year * 100 + d.month as year_month 
        FROM fact_nav_history f
        JOIN dim_date d ON f.date_id = d.date_id
    """, engine)
    
    if df.empty:
        return

    agg = df.groupby(['fund_sk', 'index_sk', 'year_month']).agg(
        avg_nav=('nav_price', 'mean'),
        month_end_nav=('nav_price', 'last')
    ).reset_index()
    
    # Calculate monthly return
    agg = agg.sort_values(['fund_sk', 'year_month'])
    agg['monthly_return'] = agg.groupby('fund_sk')['month_end_nav'].pct_change().fillna(0)
    
    agg.to_sql('agg_monthly_trends', engine, if_exists='replace', index=False)
    print(f"Monthly Trends Aggregate built with {len(agg)} records.")

def build_agg_rolling_returns():
    print("Building Rolling Returns Aggregate...")
    engine = get_engine()
    df = pd.read_sql("SELECT * FROM fact_nav_history", engine)
    
    if df.empty:
        return

    df = df.sort_values(['fund_sk', 'date_id'])
    
    # Using pandas rolling for daily return compounding
    # Simplified: rolling return based on price at t vs price at t-N
    results = []
    for fund_sk, group in df.groupby('fund_sk'):
        group = group.copy()
        
        # We need actual date objects for rolling windows if they are irregular, 
        # but since we have daily rows, we can use row offsets as approximations 
        # or just use the price N days ago.
        
        # For simplicity in this demo:
        group['rolling_30d_return'] = group['nav_price'].pct_change(periods=20) # ~20 trading days
        group['rolling_90d_return'] = group['nav_price'].pct_change(periods=60)
        group['rolling_365d_return'] = group['nav_price'].pct_change(periods=250)
        
        results.append(group[['fund_sk', 'date_id', 'rolling_30d_return', 'rolling_90d_return', 'rolling_365d_return']])
    
    res_df = pd.concat(results).fillna(0)
    res_df.to_sql('agg_rolling_returns', engine, if_exists='replace', index=False)
    print(f"Rolling Returns Aggregate built with {len(res_df)} records.")

def build_watch_list():
    print("Building Watch List...")
    engine = get_engine()
    df = pd.read_sql("SELECT * FROM agg_period_returns", engine)
    
    if df.empty:
        return

    # Count periods where excess_return < 0
    df['is_negative'] = df['excess_return'] < 0
    watch = df.groupby('fund_sk')['is_negative'].sum().reset_index()
    watch.columns = ['fund_sk', 'negative_periods_count']
    
    # Filter for 2+ periods
    watch = watch[watch['negative_periods_count'] >= 2]
    watch['reason'] = "Negative excess return in 2 or more periods."
    watch['updated_at'] = datetime.now()
    
    watch.to_sql('watch_list', engine, if_exists='replace', index=False)
    print(f"Watch List built with {len(watch)} funds.")

if __name__ == "__main__":
    build_agg_period_returns()
    build_agg_monthly_trends()
    build_agg_rolling_returns()
    build_watch_list()
