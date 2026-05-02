-- Migration 001: Staging Tables
-- Created: 2026-04-27

-- Table for Raw NSE Index Data
CREATE TABLE IF NOT EXISTS stg_index_raw (
    id SERIAL PRIMARY KEY,
    index_name VARCHAR(255) NOT NULL,
    index_date DATE NOT NULL,
    open_price DECIMAL(18,6),
    high_price DECIMAL(18,6),
    low_price DECIMAL(18,6),
    close_price DECIMAL(18,6),
    volume BIGINT,
    source_identifier VARCHAR(255), -- 'MOCK' or Filename
    extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table for Raw Fund NAV Data
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

-- Data Quality Audit Log
CREATE TABLE IF NOT EXISTS dq_audit_log (
    log_id SERIAL PRIMARY KEY,
    table_name VARCHAR(100),
    field_name VARCHAR(100),
    entity_id VARCHAR(100), -- fund_id or index_name
    entity_date DATE,
    original_value TEXT,
    imputed_value TEXT,
    rule_applied VARCHAR(255),
    run_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Pipeline Run History
CREATE TABLE IF NOT EXISTS pipeline_run_log (
    run_id SERIAL PRIMARY KEY,
    pipeline_name VARCHAR(100),
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    status VARCHAR(20), -- SUCCESS, FAILURE, PARTIAL
    records_processed INT,
    records_rejected INT,
    error_message TEXT
);

-- Watermark tracking for incremental loads
CREATE TABLE IF NOT EXISTS watermark (
    entity_name VARCHAR(255) PRIMARY KEY, -- index_name or fund_id
    last_processed_date DATE NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Cleaned Data Tables
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
