import pandas as pd
import exchange_calendars as xcals
from datetime import datetime, date
from sqlalchemy import text
from db.connection import get_engine

def load_dim_date(start_year=2015, end_year=2026):
    """
    Generates and loads the dim_date table using the NSE holiday calendar.
    """
    print(f"Generating Date Dimension from {start_year} to {end_year}...")
    
    # Get Indian exchange calendar (using XBOM as proxy for NSE holidays)
    nse = xcals.get_calendar("XBOM")
    
    start_date = pd.Timestamp(f"{start_year}-01-01")
    end_date = pd.Timestamp(f"{end_year}-12-31")
    
    all_dates = pd.date_range(start=start_date, end=end_date, freq='D')
    
    data = []
    for dt in all_dates:
        is_trading = nse.is_session(dt)
        # For simplicity, we'll mark weekends as non-trading, 
        # which is already handled by is_session.
        
        data.append({
            'date_id': int(dt.strftime('%Y%m%d')),
            'full_date': dt.date(),
            'year': dt.year,
            'quarter': (dt.month - 1) // 3 + 1,
            'month': dt.month,
            'month_name': dt.strftime('%B'),
            'day': dt.day,
            'day_of_week': dt.dayofweek + 1, # 1=Monday
            'is_trading_day': bool(is_trading),
            'is_holiday': not is_trading and dt.dayofweek < 5,
            'holiday_name': None # Could be expanded with nse.get_holiday_name if available
        })
    
    df = pd.DataFrame(data)
    engine = get_engine()
    df.to_sql('dim_date', engine, if_exists='replace', index=False)
    print(f"Date Dimension loaded with {len(df)} records.")

def load_dim_index():
    """
    Populates dim_index from cleaned staging data.
    """
    print("Loading Index Dimension...")
    engine = get_engine()
    df_stg = pd.read_sql("SELECT DISTINCT index_name FROM stg_index_clean", engine)
    
    if df_stg.empty:
        print("No index data in staging.")
        return

    # Add default metadata if missing
    df_stg['domain'] = 'Equity'
    df_stg['sector'] = 'Broad'
    df_stg['category'] = 'Benchmark'
    
    with engine.connect() as conn:
        for _, row in df_stg.iterrows():
            # Check if exists
            exists = conn.execute(
                text("SELECT 1 FROM dim_index WHERE index_name = :name"),
                {"name": row['index_name']}
            ).fetchone()
            
            if not exists:
                conn.execute(
                    text("""
                        INSERT INTO dim_index (index_name, domain, sector, category)
                        VALUES (:name, :dom, :sec, :cat)
                    """),
                    {"name": row['index_name'], "dom": row['domain'], "sec": row['sector'], "cat": row['category']}
                )
        conn.commit()
    print("Index Dimension load complete.")

def load_dim_fund():
    """
    Populates dim_fund from cleaned staging data (Initial Load / SCD Type 2).
    """
    print("Loading Fund Dimension...")
    engine = get_engine()
    
    # For now, we take the latest state from staging
    df_stg = pd.read_sql("""
        SELECT fund_id, category, expense_ratio, MIN(nav_date) as inception 
        FROM stg_fund_clean 
        GROUP BY fund_id, category, expense_ratio
    """, engine)
    
    if df_stg.empty:
        print("No fund data in staging.")
        return

    with engine.connect() as conn:
        for _, row in df_stg.iterrows():
            # Check if exists and if expense_ratio changed
            existing = conn.execute(
                text("SELECT fund_sk, expense_ratio FROM dim_fund WHERE fund_id = :id AND is_current = TRUE"),
                {"id": row['fund_id']}
            ).fetchone()
            
            if existing:
                if existing[1] != row['expense_ratio']:
                    # SCD Type 2: Close old, insert new
                    conn.execute(
                        text("UPDATE dim_fund SET is_current = FALSE, effective_to = :today WHERE fund_sk = :sk"),
                        {"today": date.today(), "sk": existing[0]}
                    )
                    conn.execute(
                        text("""
                            INSERT INTO dim_fund (fund_id, category, expense_ratio, effective_from, is_current)
                            VALUES (:id, :cat, :er, :today, TRUE)
                        """),
                        {"id": row['fund_id'], "cat": row['category'], "er": row['expense_ratio'], "today": date.today()}
                    )
            else:
                # Initial insert
                conn.execute(
                    text("""
                        INSERT INTO dim_fund (fund_id, category, expense_ratio, effective_from, is_current)
                        VALUES (:id, :cat, :er, :start, TRUE)
                    """),
                    {"id": row['fund_id'], "cat": row['category'], "er": row['expense_ratio'], "start": row['inception']}
                )
        conn.commit()
    print("Fund Dimension load complete.")

if __name__ == "__main__":
    load_dim_date()
    load_dim_index()
    load_dim_fund()
