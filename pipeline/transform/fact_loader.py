import pandas as pd
from sqlalchemy import text
from db.connection import get_engine

def load_fact_nav():
    """
    Populates fact_nav_history by joining cleaned staging data with dimensions.
    """
    print("Loading Fact Table...")
    engine = get_engine()
    
    # 1. Load staging data
    df_fund = pd.read_sql("SELECT * FROM stg_fund_clean", engine)
    df_index = pd.read_sql("SELECT * FROM stg_index_clean", engine)
    
    if df_fund.empty or df_index.empty:
        print("Staging data missing for fact load.")
        return

    # 2. Load dimensions for mapping
    dim_fund = pd.read_sql("SELECT fund_sk, fund_id FROM dim_fund WHERE is_current = TRUE", engine)
    dim_index = pd.read_sql("SELECT index_sk, index_name FROM dim_index", engine)
    dim_date = pd.read_sql("SELECT date_id, full_date FROM dim_date", engine)
    
    # Standardize dates for joining
    df_fund['nav_date'] = pd.to_datetime(df_fund['nav_date']).dt.date
    df_index['index_date'] = pd.to_datetime(df_index['index_date']).dt.date
    dim_date['full_date'] = pd.to_datetime(dim_date['full_date']).dt.date
    
    # 3. Join Fund with its Dimension
    df = df_fund.merge(dim_fund, on='fund_id')
    
    # 4. Map Fund to Benchmark Index
    # In a real scenario, this mapping would be in a reference table.
    # For now, we'll map all funds to 'NIFTY 50' as a default benchmark.
    df['benchmark_index'] = 'NIFTY 50'
    
    # 5. Join with Index Data
    df = df.merge(df_index, left_on=['benchmark_index', 'nav_date'], right_on=['index_name', 'index_date'])
    
    # 6. Join with Index Dimension
    df = df.merge(dim_index, left_on='benchmark_index', right_on='index_name')
    
    # 7. Join with Date Dimension
    df = df.merge(dim_date, left_on='nav_date', right_on='full_date')
    
    # 8. Calculate Daily Returns
    df = df.sort_values(['fund_sk', 'date_id'])
    df['daily_return'] = df.groupby('fund_sk')['nav_price'].pct_change()
    df['index_daily_return'] = df.groupby('index_sk')['close_price'].pct_change()
    df['tracking_error'] = df['daily_return'] - df['index_daily_return']
    
    # 9. Final Select and Load
    final_df = df[[
        'fund_sk', 'index_sk', 'date_id', 'nav_price', 
        'close_price', 'daily_return', 'index_daily_return', 'tracking_error'
    ]].rename(columns={'close_price': 'index_price'})
    
    # Handle NaNs from pct_change
    final_df = final_df.fillna(0)
    
    final_df.to_sql('fact_nav_history', engine, if_exists='replace', index=False)
    print(f"Fact Table loaded with {len(final_df)} records.")

if __name__ == "__main__":
    load_fact_nav()
