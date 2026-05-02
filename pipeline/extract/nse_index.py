import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from sqlalchemy import text
from db.connection import get_engine, get_session

def generate_mock_index_data(index_name, start_date, end_date):
    """
    Generates realistic OHLCV data for a given index and date range.
    """
    dates = pd.date_range(start=start_date, end=end_date, freq='B') # Business days
    n = len(dates)
    
    if n == 0:
        return pd.DataFrame()

    # Generate a random walk for prices
    initial_price = random.uniform(5000, 20000)
    returns = np.random.normal(0.0001, 0.01, n)
    price_path = initial_price * np.exp(np.cumsum(returns))
    
    data = []
    for i, date in enumerate(dates):
        close_price = price_path[i]
        open_price = close_price * (1 + random.uniform(-0.005, 0.005))
        high_price = max(open_price, close_price) * (1 + random.uniform(0, 0.005))
        low_price = min(open_price, close_price) * (1 - random.uniform(0, 0.005))
        volume = random.randint(1000000, 50000000)
        
        data.append({
            'index_name': index_name,
            'index_date': date.date(),
            'open_price': round(open_price, 2),
            'high_price': round(high_price, 2),
            'low_price': round(low_price, 2),
            'close_price': round(close_price, 2),
            'volume': volume,
            'source_identifier': 'MOCK',
            'extracted_at': datetime.now()
        })
    
    return pd.DataFrame(data)

def get_watermark(index_name):
    """
    Retrieves the last processed date for an index from the watermark table.
    """
    engine = get_engine()
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT last_processed_date FROM watermark WHERE entity_name = :name"),
            {"name": index_name}
        ).fetchone()
        return result[0] if result else None

def update_watermark(index_name, last_date):
    """
    Updates the last processed date for an index in the watermark table.
    Dialect-agnostic approach for SQLite/PostgreSQL.
    """
    engine = get_engine()
    with engine.connect() as conn:
        # Check if exists
        result = conn.execute(
            text("SELECT 1 FROM watermark WHERE entity_name = :name"),
            {"name": index_name}
        ).fetchone()
        
        if result:
            conn.execute(
                text("UPDATE watermark SET last_processed_date = :date, updated_at = CURRENT_TIMESTAMP WHERE entity_name = :name"),
                {"name": index_name, "date": last_date}
            )
        else:
            conn.execute(
                text("INSERT INTO watermark (entity_name, last_processed_date, updated_at) VALUES (:name, :date, CURRENT_TIMESTAMP)"),
                {"name": index_name, "date": last_date}
            )
        conn.commit()

def run_nse_extraction(indices=None):
    """
    Main entry point for NSE mock extraction.
    """
    if indices is None:
        indices = ['NIFTY 50', 'NIFTY BANK', 'NIFTY IT']
    
    engine = get_engine()
    
    for index in indices:
        print(f"Processing index: {index}")
        
        last_date = get_watermark(index)
        
        if last_date:
            if isinstance(last_date, str):
                last_date = datetime.strptime(last_date, '%Y-%m-%d').date()
            start_date = last_date + timedelta(days=1)
        else:
            # Default to last 365 days for first load
            start_date = (datetime.now() - timedelta(days=365)).date()
        
        end_date = datetime.now().date()
        
        if start_date > end_date:
            print(f"Index {index} is already up to date.")
            continue
            
        print(f"Generating data from {start_date} to {end_date}")
        df = generate_mock_index_data(index, start_date, end_date)
        
        if not df.empty:
            df.to_sql('stg_index_raw', engine, if_exists='append', index=False)
            update_watermark(index, df['index_date'].max())
            print(f"Loaded {len(df)} records for {index}")
        else:
            print(f"No data generated for {index}")

if __name__ == "__main__":
    # Create tables if using SQLite for dev
    from sqlalchemy import MetaData
    engine = get_engine()
    # In a real scenario, we'd run the migration script. 
    # For this demo, we'll assume tables exist or SQLAlchemy handles them.
    run_nse_extraction()
