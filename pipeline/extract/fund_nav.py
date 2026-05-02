from mftool import Mftool
import pandas as pd
from datetime import datetime, timedelta
from sqlalchemy import text
from db.connection import get_engine

def fetch_fund_nav_data(fund_code):
    """
    Fetches historical NAV data for a given fund code using mftool.
    """
    mf = Mftool()
    print(f"Fetching data for fund code: {fund_code}")
    
    try:
        # Get historical data
        data = mf.get_scheme_historical_nav(fund_code, as_Dataframe=True)
        
        if data is None or data.empty:
            print(f"No data found for fund {fund_code}")
            return pd.DataFrame()
            
        print(f"Columns in data: {data.columns}")
        # mftool returns dataframe with index as date
        df = data.reset_index()
        # Columns are ['date', 'nav', 'dayChange']
        df = df[['date', 'nav']]
        df.columns = ['nav_date', 'nav_price']
        
        # Convert date to datetime
        df['nav_date'] = pd.to_datetime(df['nav_date'], format='%d-%m-%Y').dt.date
        df['nav_price'] = pd.to_numeric(df['nav_price'], errors='coerce')
        
        # Get scheme details for metadata
        details = mf.get_scheme_details(fund_code)
        
        df['fund_id'] = fund_code
        df['exchange_code'] = 'NSE' # Assuming NSE for now
        df['currency_code'] = 'INR'
        df['category'] = details.get('scheme_category', 'Unknown')
        df['inception_date'] = None # mftool details might have it but let's be safe
        df['load_timestamp'] = datetime.now()
        
        return df
        
    except Exception as e:
        print(f"Error fetching data for {fund_code}: {e}")
        return pd.DataFrame()

def get_watermark(fund_id):
    engine = get_engine()
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT last_processed_date FROM watermark WHERE entity_name = :name"),
            {"name": f"FUND_{fund_id}"}
        ).fetchone()
        return result[0] if result else None

def update_watermark(fund_id, last_date):
    engine = get_engine()
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT 1 FROM watermark WHERE entity_name = :name"),
            {"name": f"FUND_{fund_id}"}
        ).fetchone()
        
        if result:
            conn.execute(
                text("UPDATE watermark SET last_processed_date = :date, updated_at = CURRENT_TIMESTAMP WHERE entity_name = :name"),
                {"name": f"FUND_{fund_id}", "date": last_date}
            )
        else:
            conn.execute(
                text("INSERT INTO watermark (entity_name, last_processed_date, updated_at) VALUES (:name, :date, CURRENT_TIMESTAMP)"),
                {"name": f"FUND_{fund_id}", "date": last_date}
            )
        conn.commit()

def run_fund_extraction(fund_codes=None):
    if fund_codes is None:
        # SBI Bluechip, HDFC Top 100, ICICI Pru Bluechip
        fund_codes = ['103504', '101961', '108466']
    
    engine = get_engine()
    
    for code in fund_codes:
        last_date = get_watermark(code)
        if isinstance(last_date, str):
            last_date = datetime.strptime(last_date, '%Y-%m-%d').date()
        
        df = fetch_fund_nav_data(code)
        
        if not df.empty:
            # Filter for new data
            if last_date:
                df = df[df['nav_date'] > last_date]
            
            if not df.empty:
                df.to_sql('stg_fund_raw', engine, if_exists='append', index=False)
                update_watermark(code, df['nav_date'].max())
                print(f"Loaded {len(df)} records for fund {code}")
            else:
                print(f"No new records for fund {code}")
        else:
            print(f"Failed to fetch data for fund {code}")

if __name__ == "__main__":
    run_fund_extraction()
