-- Migration 002: Dimension Tables (Star Schema)
-- Created: 2026-04-27

-- Dimension: Index (SCD Type 1)
CREATE TABLE IF NOT EXISTS dim_index (
    index_sk SERIAL PRIMARY KEY,
    index_name VARCHAR(255) NOT NULL UNIQUE,
    domain VARCHAR(50),
    sector VARCHAR(100),
    category VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Dimension: Fund (SCD Type 2 for expense_ratio)
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

-- Dimension: Date
CREATE TABLE IF NOT EXISTS dim_date (
    date_id INT PRIMARY KEY, -- YYYYMMDD
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

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_dim_fund_id ON dim_fund(fund_id);
-- Note: SQLite does not support conditional indexes in the same way as PG in some versions, 
-- but we'll try standard syntax or just a normal index.
CREATE INDEX IF NOT EXISTS idx_dim_fund_current ON dim_fund(is_current);
CREATE INDEX IF NOT EXISTS idx_dim_date_full ON dim_date(full_date);
