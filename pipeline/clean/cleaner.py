import pandas as pd
import numpy as np
from datetime import datetime
from sqlalchemy import text
from db.connection import get_engine

def log_dq_issue(entity_id, entity_date, field_name, original_value, imputed_value, rule_applied):
    """
    Logs a data quality correction to the audit log.
    """
    engine = get_engine()
    with engine.connect() as conn:
        conn.execute(
            text("""
                INSERT INTO dq_audit_log 
                (table_name, field_name, entity_id, entity_date, original_value, imputed_value, rule_applied)
                VALUES (:table, :field, :id, :date, :orig, :imp, :rule)
            """),
            {
                "table": "stg_fund_raw",
                "field": field_name,
                "id": entity_id,
                "date": entity_date,
                "orig": str(original_value),
                "imp": str(imputed_value),
                "rule": rule_applied
            }
        )
        conn.commit()

def clean_index_data():
    """
    Cleans raw index data and moves to stg_index_clean.
    """
    print("Cleaning index data...")
    engine = get_engine()
    df = pd.read_sql("SELECT * FROM stg_index_raw", engine)
    
    if df.empty:
        print("No index data to clean.")
        return

    # Basic cleaning: remove duplicates
    initial_count = len(df)
    df = df.drop_duplicates(subset=['index_name', 'index_date'], keep='last')
    
    # Standardize types
    df['index_date'] = pd.to_datetime(df['index_date']).dt.date
    
    # Save to clean table
    clean_df = df[['index_name', 'index_date', 'close_price', 'source_identifier']]
    clean_df.to_sql('stg_index_clean', engine, if_exists='replace', index=False)
    print(f"Index cleaning complete. {len(clean_df)} records saved (Dropped {initial_count - len(df)} duplicates).")

def clean_fund_data():
    """
    Cleans raw fund data and moves to stg_fund_clean.
    Implements forward-fill for NAV and mock ratings.
    """
    print("Cleaning fund data...")
    engine = get_engine()
    df = pd.read_sql("SELECT * FROM stg_fund_raw", engine)
    
    if df.empty:
        print("No fund data to clean.")
        return

    # Sort for forward fill
    df = df.sort_values(by=['fund_id', 'nav_date'])
    
    cleaned_data = []
    
    for fund_id, group in df.groupby('fund_id'):
        print(f"Cleaning fund: {fund_id}")
        
        # Ensure nav_date is a date object for comparison with all_dates
        group['nav_date'] = pd.to_datetime(group['nav_date']).dt.date
        
        # Create a date range to find gaps
        start_date = group['nav_date'].min()
        end_date = group['nav_date'].max()
        all_dates = pd.date_range(start=start_date, end=end_date, freq='D').date
        
        group = group.set_index('nav_date').reindex(all_dates)
        group['fund_id'] = fund_id
        
        # Detect gaps before fill for logging
        gaps = group[group['nav_price'].isnull()]
        for idx, row in gaps.iterrows():
            # In a real scenario, we'd log every gap, but for now just the action
            pass
        
        # Forward fill NAV price
        group['nav_price'] = group['nav_price'].ffill()
        
        # Mock ratings (1-5)
        if 'original_rating' not in group.columns:
            group['original_rating'] = np.random.uniform(1.0, 5.0)
            group['normalized_rating'] = group['original_rating'].round().astype(int)
        
        group = group.reset_index().rename(columns={'index': 'nav_date'})
        cleaned_data.append(group)

    final_df = pd.concat(cleaned_data)
    print(f"Concatenated final_df length: {len(final_df)}")
    
    # Drop rows that couldn't be filled (e.g. at the very start)
    final_df = final_df.dropna(subset=['nav_price'])
    print(f"final_df after dropna length: {len(final_df)}")
    
    # Select columns
    cols = ['fund_id', 'nav_price', 'nav_date', 'exchange_code', 'currency_code', 
            'expense_ratio', 'category', 'original_rating', 'normalized_rating']
    
    final_df[cols].to_sql('stg_fund_clean', engine, if_exists='replace', index=False)
    print(f"Fund cleaning complete. {len(final_df)} records saved.")

if __name__ == "__main__":
    clean_index_data()
    clean_fund_data()
