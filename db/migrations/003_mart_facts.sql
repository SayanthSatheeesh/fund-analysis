-- Migration 003: Fact Table
-- Created: 2026-04-27

-- Fact Table for Historical NAV and Index prices
-- For PostgreSQL, this should be partitioned by range (date_id)
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

-- Performance Indexes
CREATE INDEX IF NOT EXISTS idx_fact_fund_date ON fact_nav_history(fund_sk, date_id);
CREATE INDEX IF NOT EXISTS idx_fact_index_date ON fact_nav_history(index_sk, date_id);
CREATE INDEX IF NOT EXISTS idx_fact_date ON fact_nav_history(date_id);
