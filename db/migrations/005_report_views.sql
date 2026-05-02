-- Migration 005: Reporting Views
-- Created: 2026-04-27

-- View for Page 1: Summary & Dual-Axis Trend
CREATE OR REPLACE VIEW v_trend_history AS
SELECT 
    f.fund_id,
    f.category as fund_category,
    idx.index_name,
    dt.full_date,
    dt.year,
    dt.quarter,
    dt.month_name,
    nav.nav_price,
    nav.index_price,
    nav.daily_return,
    nav.index_daily_return,
    nav.tracking_error
FROM fact_nav_history nav
JOIN dim_fund f ON nav.fund_sk = f.fund_sk
JOIN dim_index idx ON nav.index_sk = idx.index_sk
JOIN dim_date dt ON nav.date_id = dt.date_id
WHERE f.is_current = TRUE;

-- View for Page 2: Fund Details & Period Returns
CREATE OR REPLACE VIEW v_period_performance AS
SELECT 
    f.fund_id,
    f.category as fund_category,
    f.expense_ratio,
    idx.index_name,
    p.period,
    p.fund_return,
    p.index_return,
    p.excess_return,
    CASE WHEN w.fund_sk IS NOT NULL THEN 'YES' ELSE 'NO' END as is_watch_listed
FROM agg_period_returns p
JOIN dim_fund f ON p.fund_sk = f.fund_sk
JOIN dim_index idx ON p.index_sk = idx.index_sk
LEFT JOIN watch_list w ON f.fund_sk = w.fund_sk
WHERE f.is_current = TRUE;

-- View for Page 3: Monthly Multi-Fund Matrix
CREATE OR REPLACE VIEW v_monthly_comparison AS
SELECT 
    f.fund_id,
    m.year_month,
    m.avg_nav,
    m.monthly_return
FROM agg_monthly_trends m
JOIN dim_fund f ON m.fund_sk = f.fund_sk
WHERE f.is_current = TRUE;
