import pandas as pd
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load credentials
load_dotenv()

def migrate():
    # Connection details
    sqlite_db = 'fund_analysis.db'
    pg_user = os.getenv('DB_USER', 'postgres')
    pg_pass = os.getenv('DB_PASS', 'newpassword')
    pg_host = os.getenv('DB_HOST', 'localhost')
    pg_port = os.getenv('DB_PORT', '5432')
    pg_name = os.getenv('DB_NAME', 'fund_analysis')
    
    pg_url = f"postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_name}"
    sqlite_url = f"sqlite:///{sqlite_db}"
    
    print(f"Connecting to SQLite: {sqlite_db}")
    sqlite_engine = create_engine(sqlite_url)
    
    print(f"Connecting to PostgreSQL: {pg_host}:{pg_port}/{pg_name}")
    pg_engine = create_engine(pg_url)
    
    # 1. Create Schema in PostgreSQL
    schema_sql = """
    -- [Schema definition remains same, but using CREATE OR REPLACE VIEW]
    -- Staging
    CREATE TABLE IF NOT EXISTS stg_index_raw (
        id SERIAL PRIMARY KEY,
        index_name VARCHAR(255) NOT NULL,
        index_date DATE NOT NULL,
        open_price DECIMAL(18,6),
        high_price DECIMAL(18,6),
        low_price DECIMAL(18,6),
        close_price DECIMAL(18,6),
        volume BIGINT,
        source_identifier VARCHAR(255),
        extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS stg_fund_raw (
        load_id SERIAL PRIMARY KEY,
        fund_id VARCHAR(50) NOT NULL,
        nav_price DECIMAL(18,6) NOT NULL,
        nav_date DATE NOT NULL,
        exchange_code VARCHAR(50),
        currency_code CHAR(3),
        expense_ratio DECIMAL(6,4),
        category VARCHAR(100),
        net_asset DECIMAL(20,2),
        inception_date DATE,
        load_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS dq_audit_log (
        log_id SERIAL PRIMARY KEY,
        table_name VARCHAR(100),
        field_name VARCHAR(100),
        entity_id VARCHAR(100),
        entity_date DATE,
        original_value TEXT,
        imputed_value TEXT,
        rule_applied VARCHAR(255),
        run_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS pipeline_run_log (
        run_id SERIAL PRIMARY KEY,
        pipeline_name VARCHAR(100),
        start_time TIMESTAMP,
        end_time TIMESTAMP,
        status VARCHAR(20),
        records_processed INT,
        records_rejected INT,
        error_message TEXT
    );

    CREATE TABLE IF NOT EXISTS watermark (
        entity_name VARCHAR(255) PRIMARY KEY,
        last_processed_date DATE NOT NULL,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS stg_index_clean (
        id SERIAL PRIMARY KEY,
        index_name VARCHAR(255) NOT NULL,
        index_date DATE NOT NULL,
        close_price DECIMAL(18,6) NOT NULL,
        source_identifier VARCHAR(255),
        cleaned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS stg_fund_clean (
        fund_sk SERIAL PRIMARY KEY,
        fund_id VARCHAR(50) NOT NULL,
        nav_price DECIMAL(18,6) NOT NULL,
        nav_date DATE NOT NULL,
        exchange_code VARCHAR(50),
        currency_code CHAR(3),
        expense_ratio DECIMAL(6,4),
        category VARCHAR(100),
        original_rating DECIMAL(3,1),
        normalized_rating INT,
        cleaned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- Mart Dimensions
    CREATE TABLE IF NOT EXISTS dim_index (
        index_sk SERIAL PRIMARY KEY,
        index_name VARCHAR(255) NOT NULL UNIQUE,
        domain VARCHAR(50),
        sector VARCHAR(100),
        category VARCHAR(100),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS dim_fund (
        fund_sk SERIAL PRIMARY KEY,
        fund_id VARCHAR(50) NOT NULL,
        fund_name VARCHAR(255),
        category VARCHAR(100),
        expense_ratio DECIMAL(6,4),
        is_current BOOLEAN DEFAULT TRUE,
        effective_from DATE NOT NULL,
        effective_to DATE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS dim_date (
        date_id INT PRIMARY KEY,
        full_date DATE NOT NULL UNIQUE,
        year INT NOT NULL,
        quarter INT NOT NULL,
        month INT NOT NULL,
        month_name VARCHAR(20) NOT NULL,
        day INT NOT NULL,
        day_of_week INT NOT NULL,
        is_trading_day BOOLEAN DEFAULT TRUE,
        is_holiday BOOLEAN DEFAULT FALSE,
        holiday_name VARCHAR(255)
    );

    -- Mart Facts
    CREATE TABLE IF NOT EXISTS fact_nav_history (
        fact_id SERIAL PRIMARY KEY,
        fund_sk INT NOT NULL,
        index_sk INT NOT NULL,
        date_id INT NOT NULL,
        nav_price DECIMAL(18,6) NOT NULL,
        index_price DECIMAL(18,6) NOT NULL,
        daily_return DECIMAL(18,10),
        index_daily_return DECIMAL(18,10),
        tracking_error DECIMAL(18,10),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (fund_sk) REFERENCES dim_fund(fund_sk),
        FOREIGN KEY (index_sk) REFERENCES dim_index(index_sk),
        FOREIGN KEY (date_id) REFERENCES dim_date(date_id)
    );

    -- Aggregates
    CREATE TABLE IF NOT EXISTS agg_period_returns (
        fund_sk INT NOT NULL,
        index_sk INT NOT NULL,
        period VARCHAR(20) NOT NULL,
        fund_return DECIMAL(18,10),
        index_return DECIMAL(18,10),
        excess_return DECIMAL(18,10),
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (fund_sk, index_sk, period)
    );

    CREATE TABLE IF NOT EXISTS agg_monthly_trends (
        fund_sk INT NOT NULL,
        index_sk INT NOT NULL,
        year_month INT NOT NULL,
        avg_nav DECIMAL(18,6),
        month_end_nav DECIMAL(18,6),
        monthly_return DECIMAL(18,10),
        PRIMARY KEY (fund_sk, index_sk, year_month)
    );

    CREATE TABLE IF NOT EXISTS agg_rolling_returns (
        fund_sk INT NOT NULL,
        date_id INT NOT NULL,
        rolling_30d_return DECIMAL(18,10),
        rolling_90d_return DECIMAL(18,10),
        rolling_365d_return DECIMAL(18,10),
        PRIMARY KEY (fund_sk, date_id)
    );

    CREATE TABLE IF NOT EXISTS watch_list (
        fund_sk INT PRIMARY KEY,
        negative_periods_count INT,
        reason TEXT,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- Views
    CREATE OR REPLACE VIEW v_trend_history AS
    SELECT f.fund_id, f.category as fund_category, idx.index_name, dt.full_date, dt.year, dt.quarter, dt.month_name, nav.nav_price, nav.index_price, nav.daily_return, nav.index_daily_return, nav.tracking_error
    FROM fact_nav_history nav
    JOIN dim_fund f ON nav.fund_sk = f.fund_sk
    JOIN dim_index idx ON nav.index_sk = idx.index_sk
    JOIN dim_date dt ON nav.date_id = dt.date_id
    WHERE f.is_current = TRUE;

    CREATE OR REPLACE VIEW v_period_performance AS
    SELECT f.fund_id, f.category as fund_category, f.expense_ratio, idx.index_name, p.period, p.fund_return, p.index_return, p.excess_return,
    CASE WHEN w.fund_sk IS NOT NULL THEN 'YES' ELSE 'NO' END as is_watch_listed
    FROM agg_period_returns p
    JOIN dim_fund f ON p.fund_sk = f.fund_sk
    JOIN dim_index idx ON p.index_sk = idx.index_sk
    LEFT JOIN watch_list w ON f.fund_sk = w.fund_sk
    WHERE f.is_current = TRUE;

    CREATE OR REPLACE VIEW v_monthly_comparison AS
    SELECT f.fund_id, m.year_month, m.avg_nav, m.monthly_return
    FROM agg_monthly_trends m
    JOIN dim_fund f ON m.fund_sk = f.fund_sk
    WHERE f.is_current = TRUE;
    """
    
    with pg_engine.connect() as conn:
        print("Creating PostgreSQL schema...")
        for statement in schema_sql.split(';'):
            if statement.strip():
                conn.execute(text(statement))
        conn.commit()

    # 2. Copy Data
    tables = [
        'stg_index_raw', 'stg_fund_raw', 'dq_audit_log', 'pipeline_run_log', 
        'watermark', 'stg_index_clean', 'stg_fund_clean', 
        'dim_index', 'dim_fund', 'dim_date', 
        'fact_nav_history', 
        'agg_period_returns', 'agg_monthly_trends', 'agg_rolling_returns', 'watch_list'
    ]
    
    for table in tables:
        print(f"Migrating table: {table}...")
        try:
            # Read from SQLite using SQLAlchemy engine
            df = pd.read_sql_table(table, sqlite_engine)
            if not df.empty:
                # Append to PostgreSQL
                df.to_sql(table, pg_engine, if_exists='append', index=False)
                print(f"  Successfully migrated {len(df)} rows.")
            else:
                print(f"  Table {table} is empty.")
        except Exception as e:
            print(f"  Error migrating {table}: {type(e).__name__}: {str(e)}")

    print("\nMigration complete! You can now connect Power BI to PostgreSQL.")

if __name__ == "__main__":
    migrate()

