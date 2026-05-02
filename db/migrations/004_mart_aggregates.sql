-- Migration 004: Aggregate Tables
-- Created: 2026-04-27

-- Period Returns (1M, 1Y, 3Y, 5Y, Inception)
CREATE TABLE IF NOT EXISTS agg_period_returns (
    fund_sk INT NOT NULL,
    index_sk INT NOT NULL,
    period VARCHAR(20) NOT NULL, -- '1M', '1Y', '3Y', '5Y', 'INCEPTION'
    fund_return DECIMAL(18,10),
    index_return DECIMAL(18,10),
    excess_return DECIMAL(18,10),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (fund_sk, index_sk, period)
);

-- Monthly Trends
CREATE TABLE IF NOT EXISTS agg_monthly_trends (
    fund_sk INT NOT NULL,
    index_sk INT NOT NULL,
    year_month INT NOT NULL, -- YYYYMM
    avg_nav DECIMAL(18,6),
    month_end_nav DECIMAL(18,6),
    monthly_return DECIMAL(18,10),
    PRIMARY KEY (fund_sk, index_sk, year_month)
);

-- Rolling Returns (30d, 90d, 365d)
CREATE TABLE IF NOT EXISTS agg_rolling_returns (
    fund_sk INT NOT NULL,
    date_id INT NOT NULL,
    rolling_30d_return DECIMAL(18,10),
    rolling_90d_return DECIMAL(18,10),
    rolling_365d_return DECIMAL(18,10),
    PRIMARY KEY (fund_sk, date_id)
);

-- Watch List (Funds with negative avg deviation in 2+ periods)
CREATE TABLE IF NOT EXISTS watch_list (
    fund_sk INT PRIMARY KEY,
    negative_periods_count INT,
    reason TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
