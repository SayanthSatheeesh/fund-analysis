# Product Requirements Document
## Fund Index Analysis System

---

| Field | Value |
|---|---|
| **Document Title** | Fund Index Analysis — Product Requirements Document |
| **Version** | 1.0 |
| **Status** | Draft |
| **Date** | April 27, 2026 |
| **Project** | Industry Project — Fund Index Analysis |
| **Client** | Market Data Service Provider |
| **Primary Users** | Financial Auditors, Ad-hoc Analysts |
| **Platform** | Antigravity IDE |
| **Delivery Tool** | Streamlit / Plotly |

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Problem Statement](#2-problem-statement)
3. [Goals and Objectives](#3-goals-and-objectives)
4. [Stakeholders](#4-stakeholders)
5. [User Personas](#5-user-personas)
6. [System Architecture Overview](#6-system-architecture-overview)
7. [Functional Requirements — M1: Data Collection & Pre-processing](#7-functional-requirements--m1-data-collection--pre-processing)
8. [Functional Requirements — M2: Data Mart Loading](#8-functional-requirements--m2-data-mart-loading)
9. [Functional Requirements — M3: Report Development](#9-functional-requirements--m3-report-development)
10. [Functional Requirements — M4: Deployment](#10-functional-requirements--m4-deployment)
11. [Non-Functional Requirements](#11-non-functional-requirements)
12. [Data Requirements & Schema](#12-data-requirements--schema)
13. [User Stories](#13-user-stories)
14. [Agentic Automation Requirements](#14-agentic-automation-requirements)
15. [Acceptance Criteria Summary](#15-acceptance-criteria-summary)
16. [Risks and Mitigations](#16-risks-and-mitigations)
17. [Constraints and Assumptions](#17-constraints-and-assumptions)
18. [Milestone Summary & Timeline](#18-milestone-summary--timeline)
19. [Glossary](#19-glossary)

---

## 1. Executive Summary

The **Fund Index Analysis System** is an end-to-end financial data analytics platform that enables financial auditors and ad-hoc users to benchmark mutual fund performance against market indices published by NSE India. The system automates the full data lifecycle: extraction of index and fund NAV data, transformation and quality control, loading into a structured data mart, and delivery through an interactive Streamlit or Plotly dashboard.

Users can select any available NSE market index (across domains, sectors, and categories), compare it against one or more mutual funds, view NAV trend data over flexible date ranges, and evaluate fund performance using standardised KPIs including period returns, deviation from index, and average daily deviation.

The system is designed for a market data service provider whose primary audience is financial auditors conducting performance audits and portfolio adjustment reviews. It eliminates manual benchmarking effort, enforces data consistency, and delivers a governed, auditable reporting product.

This PRD covers the complete product scope across four delivery milestones, managed end-to-end in **Antigravity IDE**, with agentic automation at each pipeline stage.

---

## 2. Problem Statement

Financial auditors and portfolio analysts currently lack a unified, automated system to compare mutual fund performance against benchmark market indices. The existing process is entirely manual:

- Analysts pull fund NAV data from multiple sources with inconsistent formats
- Index data is downloaded ad-hoc from NSE India with no version control
- Benchmark selection varies between analysts with no standard methodology
- Period return calculations are done in Excel, prone to formula errors
- No time-variant trend view exists in a single governed location
- Reports are one-off documents with no repeatable pipeline or audit trail

This results in inconsistent benchmarking outputs, high analyst effort, and risk of calculation errors in formal audit reports.

The Fund Index Analysis System resolves all of these by:

- Automating daily extraction of index and fund data from authoritative sources
- Applying standardised cleaning, deduplication, and format normalisation rules
- Pre-computing all KPIs (period returns, deviation, rolling windows) in a governed data mart
- Delivering a single interactive dashboard accessible to all authorised users
- Providing a full audit log of every data transformation and pipeline run

---

## 3. Goals and Objectives

### 3.1 Primary Goal

Deliver a governed, automated benchmarking system that compares fund performance against chosen NSE market indices across all standard time periods (1M, 1Y, 3Y, 5Y, since inception), accessible through a single interactive dashboard to financial auditors and ad-hoc users.

### 3.2 Secondary Goals

- Reduce manual benchmarking effort for financial auditors by a minimum of 80%
- Provide a repeatable, auditable data pipeline from raw source to final report
- Enable portfolio managers to identify underperforming funds (negative deviation) within seconds
- Support regulatory and audit reporting with consistent, traceable, versioned data
- Establish a scalable data mart capable of growing to 500+ funds and 200+ indices without schema changes

### 3.3 Success Metrics

| Metric | Target |
|---|---|
| Manual benchmarking effort reduction | ≥ 80% |
| Report page load time | < 5 seconds |
| Slicer interaction response time | < 3 seconds |
| Daily mart refresh completion | < 60 minutes |
| Data quality score (critical fields) | ≥ 95% |
| KPI calculation accuracy (vs hand-calc) | < 0.01% error |
| Stakeholder UAT pass rate | 100% of Critical/High bugs resolved |

### 3.4 Out of Scope — v1.0

- Real-time or intraday NAV / index price streaming
- Predictive analytics or return forecasting models
- Direct trade execution or portfolio rebalancing actions
- Integration with non-NSE index sources (BSE, global indices)
- Custom web dashboard (delivery is Streamlit or Plotly only)
- Cloud infrastructure migration (delivery is on client's existing infrastructure)

---

## 4. Stakeholders

| Role | Responsibility | Access Level |
|---|---|---|
| **Product Owner** | Client project sponsor; approves milestone gates and sign-offs | Full |
| **Financial Auditors** | Primary dashboard users; conduct performance audits | Full report + export |
| **Ad-hoc Analysts** | Secondary users; review performance before strategy meetings | Read-only, summary + comparison pages |
| **Data Engineering Team** | Pipeline, mart schema, ETL, scheduling | System/backend |
| **BI Development Team** | Streamlit / Plotly report, Pandas aggregations, dashboard design | Report authoring |
| **IT / DevOps** | Server deployment, gateway config, refresh scheduling, RBAC | Admin |
| **Project Manager** | Antigravity milestone tracking, gate management, stakeholder comms | PM |

---

## 5. User Personas

### Persona 1 — Priya, Senior Financial Auditor

**Background:** Priya conducts quarterly performance audits across a portfolio of 40+ mutual funds at a mid-size asset management firm. She is a daily Streamlit user and is comfortable with financial data analysis.

**Goals:**
- Benchmark each fund against the most relevant NSE index for her audit category
- Identify funds with persistent negative deviation across multiple periods
- Export comparison data as Excel or PDF for inclusion in formal audit reports
- Trace data back to its source for audit defensibility

**Pain points today:**
- Downloads index data manually from NSE India every quarter
- Builds comparison tables in Excel with inconsistent formulas across team members
- Spends 2–3 hours per audit cycle on data preparation before any analysis begins

**Requirements from the system:**
- Fast, reliable dashboard with accurate period returns pre-computed
- Flexible index selection — not locked to a default benchmark
- Export capability for auditor role
- Data lineage and quality audit log access

---

### Persona 2 — Arjun, Ad-hoc Analyst

**Background:** Arjun is a portfolio analyst who reviews fund performance before quarterly strategy meetings. He is not a dedicated BI tool user and relies on straightforward interfaces.

**Goals:**
- Quickly see how a specific fund compares to a benchmark without configuration effort
- Drill into a specific time period when an anomaly is visible
- Get precise numbers from chart tooltips without switching pages

**Pain points today:**
- Relies on emailed Excel snapshots from the audit team, which may be stale
- Cannot explore the data interactively or change the benchmark index
- No way to drill down from annual to monthly or daily views

**Requirements from the system:**
- Self-explanatory interface requiring no training
- Default benchmark pre-selected based on fund category
- Drill-down navigation on trend charts
- Informative tooltips showing NAV, index price, and deviation on hover

---

## 6. System Architecture Overview

The system follows a four-layer architecture managed as four sequential milestones in Antigravity IDE:

```
Layer 1 — Data Sources
  NSE India Historical Index API  +  Fund NAV Data Feeds (AMFI / Provider)
            |                                    |
            v                                    v
Layer 2 — ETL Pipeline (Milestone 1)
  Extract → Stage → Clean → Deduplicate → Standardise → Transform → Quality Gate
            |
            v
Layer 3 — Data Mart (Milestone 2)
  dim_index  +  dim_fund  +  dim_date  +  fact_nav_history
  agg_period_returns  +  agg_monthly_trends  +  agg_rolling_returns  +  watch_list
            |
            v
Layer 4 — Reporting & Delivery (Milestones 3 & 4)
  Streamlit / Plotly Semantic Model → Dashboard (3 pages) → Published to Server
  Role-based access: Auditor (full) | Ad-hoc User (read-only)
```

**Agentic automation (Antigravity)** operates across all four layers:
- Scheduled triggers for extraction and refresh
- Quality gate enforcement before milestone transitions
- Automated alerts on pipeline failures, data conflicts, and deviation anomalies
- Auto-generated validation reports attached to each milestone record

---

## 7. Functional Requirements — M1: Data Collection & Pre-processing

### FR-01 — NSE Index Data Ingestion (Mock Data / Manual Fallback)

**Description:** Due to aggressive bot detection and lack of an official public API for the NSE India historical index data endpoint (`nseindia.com/reports-indices-historical-index-data`), the system shall use an automated mock data generator to simulate realistic index data, with a fallback to ingest manually downloaded CSV files.

**Details:**
- Simulate or ingest bulk data for all available NSE indices across equity, debt, hybrid, and other domains
- Store raw records in a staging table (`stg_index_raw`) with extraction timestamp and source identifier
- Avoid live scraping to ensure pipeline stability

**Acceptance Criteria:**
- Mock data generation or manual CSV ingestion runs successfully for all index categories in scope
- Raw records written to `stg_index_raw` with `extracted_at` and `source_url` (or generator tag) populated

---

### FR-02 — Incremental Index Load

**Description:** The system shall support incremental extraction, loading only index records for dates not already present in the staging table. Re-pulling of existing date ranges shall be avoided using a watermark mechanism.

**Details:**
- Watermark stored per index; updated after each successful run to the maximum successfully loaded date
- Incremental load compares incoming record dates against the watermark before insert
- Watermark value surfaced in Antigravity run history log

**Acceptance Criteria:**
- On a second run with identical parameters, zero duplicate records are inserted
- Watermark correctly updated to the latest loaded date after each successful run
- Watermark value visible in Antigravity pipeline run log

---

### FR-03 — Fund Source Data Schema

**Description:** The system shall define and populate a source fund data staging table (`stg_fund_raw`) with all required fields.

**Required Fields:**

| Field | Type | Constraints |
|---|---|---|
| Fund Id | VARCHAR | Not null; uppercase; matches fund master |
| NAV price | DECIMAL(18,6) | Not null; > 0 |
| NAV date | DATE (YYYY-MM-DD) | Not null |
| Exchange Code | VARCHAR | Not null |
| Currency Code | CHAR(3) | ISO 4217 format |
| Expense Ratio | DECIMAL(6,4) | Nullable; ≥ 0 |
| Category | VARCHAR | Controlled vocabulary |
| Net Asset | DECIMAL(20,2) | Nullable |
| Inception Date | DATE (YYYY-MM-DD) | Nullable; flagged if missing |
| load_id | INT | Surrogate PK; auto-generated |
| load_timestamp | TIMESTAMP | Auto-populated on insert |

**Acceptance Criteria:**
- All nine business fields populated for every fund in scope
- No record missing Fund Id or NAV price or NAV date
- Surrogate key (`load_id`) and `load_timestamp` present on every row

---

### FR-04 — Incremental Fund Data Ingestion

**Description:** The system shall support daily incremental ingestion of new NAV records using a watermark comparison on NAV date per Fund Id.

**Details:**
- If a NAV record already exists for the same Fund Id + NAV date: skip by default; overwrite only if explicitly configured
- Conflicting records (same Fund Id + NAV date, different NAV price): do not silently overwrite; escalate as a data issue ticket in Antigravity
- Support multiple fund provider feed formats: CSV flat file, REST API, SFTP drop folder

**Acceptance Criteria:**
- Duplicate fund records are not inserted on incremental runs (verified by row count assertion)
- Conflicting records produce an Antigravity data issue ticket within 5 minutes of detection
- Conflicting records excluded from the clean dataset until the ticket is resolved

---

### FR-05 — Missing Value Handling

**Description:** The system shall apply defined imputation strategies to resolve missing values in critical fields and log all imputation actions.

**Imputation Rules:**

| Field | Missing Value Rule |
|---|---|
| NAV price | Forward-fill from the last available NAV date for the same Fund Id |
| Exchange Code | Lookup from fund master reference table |
| Currency Code | Lookup from fund master reference table |
| Inception Date | Flag record as `DATA_ISSUE`; exclude from since-inception calculations |
| Category | Lookup from fund master; if not found, flag as `UNCATEGORISED` |

**Audit Logging:**
All imputation actions must be written to `dq_audit_log` with: field name, original value, imputed value, rule applied, run timestamp, Fund Id, NAV date.

**Acceptance Criteria:**
- Zero null NAV price values in the cleaned output dataset
- All imputation actions traceable in `dq_audit_log` with original and imputed values
- `DATA_ISSUE` flags visible in the staging table and reported in the quality summary

---

### FR-06 — Duplicate Detection and Resolution

**Description:** The system shall enforce uniqueness on the composite key (Fund Id, NAV date) in the cleaned dataset.

**Rules:**
- Identical duplicates (same Fund Id, NAV date, same NAV price): retain the record with the latest `load_timestamp`; discard others
- Conflicting duplicates (same Fund Id, NAV date, different NAV price): create Antigravity data issue ticket; exclude both records until resolved by data owner

**Acceptance Criteria:**
- Zero duplicate (Fund Id, NAV date) combinations in the cleaned output table
- Every conflict has a corresponding open Antigravity ticket
- Duplicate removal count logged to the data quality audit table per run

---

### FR-07 — Format Standardisation

**Description:** The system shall normalise all format-sensitive fields to consistent standards across both fund and index datasets.

**Standardisation Rules:**

| Field | Rule |
|---|---|
| All date fields | Enforce YYYY-MM-DD; auto-convert DD/MM/YYYY and MM-DD-YYYY variants |
| Currency codes | Normalise to ISO 4217 three-letter codes (e.g. INR, USD) |
| Category values | Map to controlled vocabulary: Equity, Debt, Hybrid, Liquid, Index Fund, ETF |
| Fund IDs | Strip leading/trailing whitespace; enforce uppercase; validate against fund master |
| NAV price | Strip currency symbols if present; parse as DECIMAL |

**Acceptance Criteria:**
- Zero non-conforming values in date, currency code, or category fields in the cleaned dataset
- All Fund Ids pass format validation against the fund master list
- Conversion counts for each rule logged to the quality audit report

---

### FR-08 — Fund Rating Standardisation (Mock Data)

**Description:** The system shall normalise fund ratings from multiple rating agencies onto a unified 1–5 numeric scale to enable cross-fund comparison. As rating data from CRISIL and Morningstar is proprietary and lacks free programmatic access, the system shall utilise a mock data generator or client-provided static files for ratings.

**Details:**
- Source rating agencies: Simulated CRISIL, Morningstar, SEBI
- Unified scale: 1 (lowest) to 5 (highest)
- Store both `original_rating` and `normalized_rating` as separate columns
- Store `rating_agency` and `rating_date` for every rating record
- Mapping table shall be documented and versioned in the data dictionary

**Acceptance Criteria:**
- Every fund with a rating has both `original_rating` and `normalized_rating` populated using the mock data
- `rating_agency` and `rating_date` non-null for all rated funds
- Mapping table documented in data dictionary and attached to M1 Antigravity milestone

---

### FR-09 — Data Quality Gate (M1 → M2 Transition)

**Description:** The system shall enforce an automated data quality gate at the end of Milestone 1. Milestone 2 pipeline shall not start until the gate passes.

**Gate Conditions (all must pass):**

| Check | Threshold |
|---|---|
| Null rate on Fund Id, NAV price, NAV date | < 1% |
| Duplicate rate on (Fund Id, NAV date) | 0% |
| Format non-conformance rate | < 0.5% |
| Unresolved DATA_ISSUE flags | Must be reviewed and acknowledged |

**Acceptance Criteria:**
- Automated quality score report generated after each cleaning run
- Gate status (PASS / FAIL) visible on Antigravity M1 board
- M2 pipeline remains blocked in Antigravity until gate status is PASS
- Gate result attached to M1 milestone record as a downloadable report

---

## 8. Functional Requirements — M2: Data Mart Loading

### FR-10 — Index Dimension Table (`dim_index`)

**Description:** The system shall load a reference dimension table for all available NSE indices.

**Schema:**

| Field | Type | Notes |
|---|---|---|
| index_sk | INT | Surrogate PK; auto-generated |
| index_id | VARCHAR | Business key from NSE |
| index_name | VARCHAR | Full index name |
| domain | VARCHAR | Equity / Debt / Hybrid / Other |
| sector | VARCHAR | Sector classification |
| category | VARCHAR | Sub-category classification |
| currency | CHAR(3) | ISO 4217 |
| active_flag | BOOLEAN | Current availability |
| effective_from | DATE | SCD Type 1 effective date |
| effective_to | DATE | SCD Type 1 end date (NULL if current) |

**Acceptance Criteria:**
- All NSE index categories populated with no gaps in domain/sector/category hierarchy
- No duplicate `index_sk` or `index_id` values
- `active_flag` correctly set for all indices

---

### FR-11 — Fund Dimension Table (`dim_fund`)

**Description:** The system shall load a fund dimension table with static and slowly changing attributes for all funds in scope.

**Schema:**

| Field | Type | Notes |
|---|---|---|
| fund_sk | INT | Surrogate PK |
| fund_id | VARCHAR | Business key |
| fund_name | VARCHAR | Full fund name |
| category | VARCHAR | Controlled vocabulary |
| exchange_code | VARCHAR | Exchange identifier |
| currency_code | CHAR(3) | ISO 4217 |
| inception_date | DATE | From source; null if DATA_ISSUE flagged |
| expense_ratio | DECIMAL(6,4) | SCD Type 2 tracked |
| effective_from | DATE | SCD Type 2 start |
| effective_to | DATE | SCD Type 2 end (NULL if current) |
| is_current | BOOLEAN | TRUE for current record |

**Notes:**
- `expense_ratio` tracked as SCD Type 2: every change creates a new row with updated effective dates; prior row closed with `effective_to` and `is_current = FALSE`

**Acceptance Criteria:**
- All funds in scope present with at least one current row (`is_current = TRUE`)
- Expense ratio history preserved with valid effective date ranges (no gaps, no overlaps per fund)
- No fund with a null `inception_date` in `dim_fund` unless flagged as `DATA_ISSUE` in staging

---

### FR-12 — Date Dimension Table (`dim_date`)

**Description:** The system shall generate a complete date dimension covering all calendar dates from the earliest fund inception date to the current date.

**Schema:**

| Field | Type | Notes |
|---|---|---|
| date_id | DATE | PK |
| day | INT | Day of month (1–31) |
| week_number | INT | ISO week number |
| month | INT | Month number (1–12) |
| month_name | VARCHAR | Full month name |
| quarter | INT | Quarter (1–4) |
| year | INT | Calendar year |
| is_trading_day | BOOLEAN | Excludes weekends and NSE holidays |
| is_holiday | BOOLEAN | NSE market holiday flag |

**Acceptance Criteria:**
- Date dimension covers full range from earliest inception date to today with zero gaps
- `is_trading_day` correctly excludes all weekends and NSE market holidays
- `is_holiday` populated using the NSE official holiday calendar for the relevant years

---

### FR-13 — Historical NAV & Index Price Fact Table (`fact_nav_history`)

**Description:** The system shall load the main historical fact table with daily NAV and index price records.

**Schema:**

| Field | Type | Notes |
|---|---|---|
| fact_id | BIGINT | Surrogate PK |
| fund_sk | INT | FK → dim_fund |
| index_sk | INT | FK → dim_index |
| date_id | DATE | FK → dim_date |
| nav_price | DECIMAL(18,6) | Fund NAV on this date |
| index_price | DECIMAL(18,6) | Selected index close price |
| net_asset | DECIMAL(20,2) | Fund net assets on this date |
| expense_ratio_snapshot | DECIMAL(6,4) | Expense ratio at point in time |
| load_timestamp | TIMESTAMP | ETL load time |

**Performance:**
- Table shall be partitioned by `year` from day one
- Index on (`fund_sk`, `date_id`) for time-series query performance
- Index on (`index_sk`, `date_id`) for index price lookups

**Acceptance Criteria:**
- Row count equals expected number of fund × trading day combinations from each fund's inception date
- Zero orphaned foreign keys on any FK column
- Year partitioning confirmed in database schema documentation
- Referential integrity check passes: all `fund_sk`, `index_sk`, `date_id` values exist in respective dimension tables

---

### FR-14 — Period Return KPI Derivation (`agg_period_returns`)

**Description:** The system shall calculate and store period return metrics for every fund × index combination across all standard benchmark periods.

**Return Formula:**
```
Return % = (Price_end - Price_start) / Price_start × 100
```

**Periods:**

| Period | Base Date |
|---|---|
| 1 Month | 30 calendar days before report date |
| 1 Year | 365 calendar days before report date |
| 3 Year | 3 years before report date |
| 5 Year | 5 years before report date |
| Since Inception | Fund's Inception Date |

**Derived Metrics per period:**
- `fund_return_pct`: return on fund NAV
- `index_return_pct`: return on index price for same date window
- `deviation_pct`: `fund_return_pct - index_return_pct`
- `avg_daily_deviation`: mean of (daily fund return − daily index return) over the period

**Acceptance Criteria:**
- All five periods × all fund × index combinations populated in `agg_period_returns`
- Since-inception return uses fund's `inception_date` from `dim_fund` as base date
- Manual verification: 5 funds × 3 periods each cross-checked against raw fact data; discrepancy < 0.01%
- Funds with null `inception_date` show `NULL` for since-inception fields (not zero or incorrect date)

---

### FR-15 — Time-Variant Aggregate Tables

**Description:** The system shall build pre-aggregated tables to support fast dashboard rendering across monthly and yearly granularities.

#### `agg_monthly_trends`

| Field | Notes |
|---|---|
| fund_sk (FK) | |
| index_sk (FK) | |
| year | |
| month | |
| avg_nav | Average NAV price for the month |
| month_end_nav | NAV price on last trading day of month |
| avg_index_price | Average index price for the month |
| month_end_index_price | Index close price on last trading day of month |
| monthly_fund_return_pct | Month-over-month fund return |
| monthly_index_return_pct | Month-over-month index return |

#### `agg_rolling_returns`

| Field | Notes |
|---|---|
| fund_sk (FK) | |
| index_sk (FK) | |
| date_id (FK) | |
| return_30d | Trailing 30-day return |
| return_90d | Trailing 90-day return |
| return_365d | Trailing 365-day return |

**Acceptance Criteria:**
- Monthly aggregate covers all fund × year/month combinations from inception to current month
- Yearly aggregate covers all fund × year combinations
- Rolling window aggregates updated within 15 minutes of daily mart refresh completion
- No gaps in monthly coverage per fund

---

### FR-16 — Average Deviation & Watch-List (`watch_list`)

**Description:** The system shall compute average deviation and maintain a watch-list of consistently underperforming funds.

**Watch-List Logic:**
- A fund is flagged as a persistent underperformer if it has negative `avg_daily_deviation` in two or more standard periods for the same index
- Watch-list record includes: `fund_sk`, `flagged_periods` (count of periods with negative deviation), `flagged_at` timestamp, `is_active` boolean
- Watch-list is fully refreshed on every mart refresh

**Acceptance Criteria:**
- `watch_list` table auto-refreshed on every mart refresh cycle
- Watch-list logic documented in data dictionary
- Dashboard watch-list flag indicator correctly reflects `is_active` status from `watch_list` table
- Funds removed from watch-list when deviation turns positive; `is_active` set to FALSE

---

### FR-17 — Mart Validation & Stakeholder Sign-off

**Description:** Before Milestone 2 is marked complete, the system shall run automated validation checks and obtain stakeholder sign-off.

**Automated Validation Checks:**

| Check | Description |
|---|---|
| Row count assertion | Fact table rows = expected fund × trading day combinations |
| Null check | All FK fields in fact table non-null |
| Range check — NAV | All NAV prices > 0 |
| Range check — returns | All return % values between −100% and +10,000% |
| Date gap detection | No missing trading day NAV records per fund |
| Referential integrity | All FKs resolve to dimension table records |
| Aggregate coverage | All fund × period combinations in `agg_period_returns` |

**Output:**
- Auto-generated validation summary report attached to Antigravity M2 milestone record
- Stakeholder sign-off recorded in Antigravity before M3 tasks unlock
- M3 pipeline blocked until sign-off is captured

**Acceptance Criteria:**
- All validation checks pass with zero failures
- Validation report generated same day as mart load completion
- Stakeholder sign-off recorded; M3 board unlocked in Antigravity

---

## 9. Functional Requirements — M3: Report Development

> **Important Note:** Building the dashboard requires ~64 hours of manual GUI work in Streamlit or Plotly Dash. While the data mart and semantic model definitions are automated via code, the `.py` or `.py` dashboard files is fully automated via Python code.

### FR-18 — Data Integration & Semantic Model

**Description:** The BI report shall connect to the data mart and define the full semantic model.

**Connection Mode:**
- Streamlit: SQLAlchemy mode for real-time access to the mart
- Plotly: Live connection to the mart database
- Read-only service account used for all report connections

**Semantic Model Relationships:**

| Relationship | Type | Filter Direction |
|---|---|---|
| dim_fund → fact_nav_history | One-to-many on fund_sk | Single (dim filters fact) |
| dim_index → fact_nav_history | One-to-many on index_sk | Single (dim filters fact) |
| dim_date → fact_nav_history | One-to-many on date_id | Single (dim filters fact) |

**Acceptance Criteria:**
- All four mart tables loaded in the semantic model
- All three relationships defined with correct cardinality and single-direction filtering
- No many-to-many relationships in the model
- Model passes referential integrity check in Streamlit / Plotly

---

### FR-19 — Dynamic Slicers and Cross-Filters

**Description:** The report shall provide four interactive filter controls that drive all visuals simultaneously.

**Slicers:**

| Slicer | Binding | Behaviour |
|---|---|---|
| Date Range | From/to date pickers → `dim_date` | Filters all visuals to selected date window |
| Index Selection | Domain → Sector → Category hierarchy → `dim_index` | Filters all index-related visuals; drives measure context |
| Fund Type | Category field → `dim_fund` | Filters fund list in comparison table and trend chart |
| Exchange Code | Exchange Code → `dim_fund` | Filters fund list |

**Performance requirement:** Any slicer change shall update all visuals within 3 seconds.

**Acceptance Criteria:**
- All four slicers functional and bound to correct dimension fields
- Cross-filter behaviour verified: changing the index slicer updates KPI cards, trend chart, and comparison table simultaneously
- Slicer combinations tested across 10 scenario scripts
- Response time < 3 seconds measured for each slicer change in UAT

---

### FR-20 — Custom Measures (Python/Pandas / Plotly Calculated Fields)

**Description:** The report shall implement six calculated measures that respond dynamically to slicer context.

**Measures:**

| Measure Name | Formula Description |
|---|---|
| `[Fund Return %]` | (Last NAV in range − First NAV in range) / First NAV × 100 |
| `[Index Return %]` | Same formula applied to index price for identical date window |
| `[Deviation %]` | `[Fund Return %]` − `[Index Return %]` |
| `[Avg Daily Deviation]` | Mean of (daily fund return − daily index return) over selected period |
| `[30D Rolling Return]` | Trailing 30-day fund return relative to current date in context |
| `[90D Rolling Return]` | Trailing 90-day fund return relative to current date in context |

**Documentation requirement:** All measures documented in a measure catalogue (name, formula, purpose, expected output, edge cases). Catalogue attached to Antigravity M3 board.

**Acceptance Criteria:**
- All six measures implemented and visible in the semantic model
- Measure output verified against `agg_period_returns` mart values for 5 funds; discrepancy < 0.01%
- Measures respond correctly to all four slicer contexts
- Measure catalogue completed and attached to Antigravity M3 record

---

### FR-21 — Dashboard Page 1: Summary

**Description:** The summary page is the landing page for all users. It shall provide an immediate view of fund performance vs the selected index.

**Visual Components:**

| Visual | Description |
|---|---|
| KPI Card — Fund Return % | Shows `[Fund Return %]` for selected date range |
| KPI Card — Index Return % | Shows `[Index Return %]` for same date range |
| KPI Card — Deviation % | Shows `[Deviation %]`; green if positive, red if negative |
| Trend Line Chart | Dual-axis: fund NAV and index price over selected date range, both normalised to base 100 |
| Drill-down | X-axis supports Year → Quarter → Month → Day via right-click and drill buttons |
| Tooltip | On hover: fund name, date, NAV price, index price, deviation |

**Acceptance Criteria:**
- KPI cards update within 3 seconds of any slicer change
- Trend chart renders correctly for 1M, 1Y, 5Y, and since-inception date ranges
- Drill-down confirmed working at all four levels (Year, Quarter, Month, Day)
- Tooltip displays all five required fields on hover

---

### FR-22 — Dashboard Page 2: Fund Detail (Drill-Through)

**Description:** The fund detail page is accessible via drill-through from the summary page. It provides deep analysis of a single selected fund.

**Visual Components:**

| Visual | Description |
|---|---|
| KPI Cards (6) | All six measures for the drilled-through fund |
| Period Return Bar Chart | Side-by-side bars: fund return vs index return for 1M, 1Y, 3Y, 5Y, inception |
| Expense Ratio Trend | Line chart of expense ratio history over time (SCD Type 2 history) |
| Watch-List Flag | Indicator badge: flagged as underperformer if `watch_list.is_active = TRUE` |

**Acceptance Criteria:**
- Drill-through from summary page navigates to fund detail page with correct fund context retained
- All visuals filter correctly to the drilled-through fund
- Watch-list flag correctly reflects `is_active` from `watch_list` table
- Expense ratio trend reflects full SCD Type 2 history from `dim_fund`

---

### FR-23 — Dashboard Page 3: Multi-Fund Comparison

**Description:** The comparison page provides a matrix of all in-scope funds compared against the selected index across all standard periods.

**Visual Components:**

| Visual | Description |
|---|---|
| Comparison Matrix | Rows = funds; Columns = 1M, 1Y, 3Y, 5Y, inception return and deviation |
| Conditional Formatting | Green background for positive deviation; red for negative |
| Sort | Sortable by any period column (ascending or descending) |
| Export | Export to Excel available for Auditor role; not available for Ad-hoc User role |

**Acceptance Criteria:**
- Comparison table renders all in-scope funds correctly
- Conditional formatting applies correctly for positive and negative deviations across all columns
- Table sorts by any column within 3 seconds
- Export to Excel available and functional for Auditor role; export button absent or disabled for Ad-hoc User role

---

### FR-24 — Drill-Down Navigation

**Description:** All time-axis visuals shall support hierarchical drill-down across four levels.

**Levels:** Year → Quarter → Month → Day

**Interaction methods:**
- Right-click context menu: "Drill Down"
- Dedicated drill-down button in visual header
- Drill-up returns to previous level

**Acceptance Criteria:**
- Drill-down functions at all four levels on all applicable chart visuals
- Drill-up correctly restores previous level without data loss
- Confirmed working in both Streamlit Cloud and Streamlit Cloud environments post-deployment

---

### FR-25 — User Acceptance Testing (UAT)

**Description:** A formal UAT shall be conducted before Milestone 3 is marked complete.

**UAT Requirements:**
- Minimum participants: 2 financial auditors + 1 ad-hoc user representative
- Prepared test script: 10 scenarios covering index selection, date range variation, drill-down, comparison, export, and permission validation
- All Critical and High severity bugs resolved before sign-off
- UAT sign-off document attached to Antigravity M3 milestone record

**Bug Severity Definitions:**

| Severity | Definition | Resolution Requirement |
|---|---|---|
| Critical | Incorrect calculation, data not loading, crash | Must resolve before sign-off |
| High | Visual not responding to slicer, missing required field | Must resolve before sign-off |
| Medium | UX issue, label incorrect | Resolve before deployment or defer to v1.1 |
| Low | Cosmetic, minor formatting | May defer to v1.1 |

**Acceptance Criteria:**
- UAT conducted with minimum required participants; attendance recorded
- Zero open Critical bugs at time of sign-off
- Zero open High bugs at time of sign-off
- UAT sign-off document attached to Antigravity M3 record; M4 unlocked

---

## 10. Functional Requirements — M4: Deployment

### FR-26 — Report Publication

**Description:** The finalized report shall be published to the production Streamlit Cloud workspace or Streamlit Cloud project.

**Details:**
- All data connections must resolve correctly in the server environment using production mart credentials
- All three report pages accessible post-publication
- Antigravity agent pings report URL post-publish and confirms HTTP 200 response

**Acceptance Criteria:**
- Report accessible via production URL
- All three pages load without errors
- Data connections verified against production mart credentials
- HTTP 200 response confirmed via Antigravity post-deploy validation check

---

### FR-27 — Role-Based Access Control (RBAC)

**Description:** The system shall implement two access tiers enforced at the server level.

**Role Definitions:**

| Permission | Auditor Role | Ad-hoc User Role |
|---|---|---|
| Summary page | Full access | Full access |
| Comparison page | Full access | Full access |
| Fund detail page | Full access | No access (hidden) |
| Export to Excel/PDF | Enabled | Disabled |
| Drill-through | Enabled | Disabled |
| Data modification | Not applicable | Not applicable |

**RBAC must be enforced at the Streamlit Cloud / Streamlit Cloud level**, not only at the report level, so that removing a user from a role immediately revokes their access.

**Acceptance Criteria:**
- Auditor test account can access all three pages, use drill-through, and export
- Ad-hoc user test account cannot see fund detail page; no export option visible
- Role assignment documented and confirmed by IT admin
- Access revocation tested: removing a user from the auditor group immediately removes fund detail page access

---

### FR-28 — Portal Embedding (Optional)

**Description:** If required by the client, the report shall be embedded in the company intranet or SharePoint portal.

**Details:**
- Embed via Streamlit embed API or Plotly embed URL
- Authentication via portal's existing identity provider (SSO)
- Functional in Chrome, Edge, and Firefox without requiring separate Streamlit or Plotly credentials

**Acceptance Criteria:**
- Embedded report renders without errors in Chrome, Edge, and Firefox
- SSO authentication works via portal identity provider
- Role-based access enforced in embedded view (auditors see all pages; ad-hoc users see summary + comparison only)

---

### FR-29 — Scheduled Data Refresh

**Description:** The system shall configure fully automated daily data refresh so the dashboard always reflects the previous trading day's data.

**Refresh Schedule:**
- Trigger: daily at 08:00 IST
- Precondition: overnight mart ETL pipeline must complete before refresh triggers
- Gateway: on-premise database gateway (if mart is on-premise) or cloud connector configured with production credentials

**Failure Handling:**
- On refresh failure: email alert to BI admin and data engineer within 5 minutes of failure detection
- Antigravity incident ticket auto-created and assigned to BI admin
- Stakeholders notified of data lag via Antigravity notification

**End-to-End Refresh Cycle:**
```
Mart ETL completes (overnight) → Antigravity triggers refresh → 
Streamlit / Plotly refreshes data → Report updated by 08:30 IST
```

**Acceptance Criteria:**
- Daily refresh runs successfully for 5 consecutive days in the UAT environment
- Failure alert email received within 5 minutes when credentials deliberately broken during testing
- End-to-end cycle time from ETL completion to report updated < 30 minutes
- Refresh history log visible in Antigravity with timestamp, duration, and status

---

### FR-30 — Stakeholder Onboarding & Access Delivery

**Description:** All users shall receive access and onboarding materials on go-live day.

**Onboarding Package:**
- Report URL and login credentials (or SSO instructions)
- One-page Quick Start Guide covering: how to select an index, set a date range, read the deviation metric, use drill-down navigation, and export (auditor role)
- 30-minute live walkthrough session for financial auditors on go-live day

**Scheduled Subscriptions (Optional):**
- Weekly email subscription: summary page snapshot + live report link
- Sent every Monday at 09:00 IST
- Recipient list confirmed with stakeholder before activation

**Acceptance Criteria:**
- All users can log in independently within 24 hours of go-live
- Quick Start Guide covers all five required topics
- Walkthrough session attended by minimum two auditors; attendance recorded in Antigravity
- Weekly subscription emails confirmed active (if opted in)

---

## 11. Non-Functional Requirements

### NFR-01 — Performance

| Metric | Target |
|---|---|
| Report page load time (full production data) | < 5 seconds |
| Slicer interaction / cross-filter update | < 3 seconds |
| Daily incremental mart refresh | < 60 minutes |
| Rolling aggregate recalculation | < 15 minutes post mart load |
| Drill-down level transition | < 2 seconds |

---

### NFR-02 — Availability

| Item | Target |
|---|---|
| Report server uptime (Streamlit Cloud / Plotly Online SLA) | 99.9% |
| ETL pipeline retry on failure | Up to 3 retries with exponential backoff |
| Alert on unrecovered pipeline failure | Within 15 minutes of final retry failure |

---

### NFR-03 — Data Freshness

- Dashboard shall reflect data as of the previous trading day by 08:30 IST on each market day
- Data staleness exceeding 24 hours beyond expected refresh time triggers an automated alert to BI admin
- Staleness indicator visible in report footer showing last successful refresh timestamp

---

### NFR-04 — Data Accuracy

| Metric | Standard |
|---|---|
| KPI decimal precision | 2 decimal places minimum |
| Return calculation accuracy vs hand-calc | < 0.01% discrepancy |
| Average deviation recalculation | Full recalculation on every mart refresh; no accumulative drift |
| NAV price precision in mart | DECIMAL(18,6) |

---

### NFR-05 — Scalability

- Mart schema and pipeline shall support expansion to 500+ funds without schema changes
- Mart schema and pipeline shall support 200+ indices without schema changes
- Fact table partitioned by year from day one to support multi-year data growth
- Aggregate tables designed to recalculate incrementally for new date partitions only

---

### NFR-06 — Security

| Requirement | Standard |
|---|---|
| Data connection credentials | Stored in Antigravity secrets vault; no hardcoding |
| Database access | Dedicated read-only service accounts |
| Principle of least privilege | All accounts granted only minimum permissions required |
| RBAC enforcement | At server level (Streamlit Cloud / Streamlit Cloud) — not report level only |
| Credential rotation | Service account passwords rotatable without pipeline downtime |

---

### NFR-07 — Auditability

Every pipeline run shall produce a log record containing:
- Run timestamp (start and end)
- Records processed (extracted, cleaned, loaded)
- Records rejected (with reason codes)
- Errors encountered (with stack trace if applicable)
- Run status (SUCCESS / FAILURE / PARTIAL)

All data quality imputation actions traceable to: source field, Fund Id, NAV date, original value, imputed value, rule applied, run timestamp.

Pipeline logs and DQ audit logs retained for a minimum of 12 months.

---

### NFR-08 — Maintainability

- All Pandas aggregations and Plotly calculated fields documented in a measure catalogue
- ETL pipeline modular: each stage (extract, clean, transform, load) independently re-runnable without side effects on completed stages
- All mart schema changes version-controlled with migration scripts
- Report `.py` or Plotly workbook files version-controlled in Antigravity file storage

---

## 12. Data Requirements & Schema

### 12.1 Source Data

| Source | Format | Fields |
|---|---|---|
| NSE India historical index data | REST endpoint / CSV | Index Name, Date, Open, High, Low, Close, Volume |
| Fund NAV data feed | CSV, API, or SFTP | Fund Id, NAV price, NAV date, Exchange Code, Currency Code, Expense Ratio, Category, Net Asset, Inception Date |
| Fund ratings | CSV / publication | Fund Id, Rating value, Rating agency, Rating date |
| NSE holiday calendar | Static list (annual) | Date, Holiday name |

### 12.2 Staging Tables

| Table | Purpose |
|---|---|
| `stg_index_raw` | Raw index extraction; includes extraction metadata |
| `stg_fund_raw` | Raw fund NAV records; includes load metadata |

### 12.3 Data Mart Tables

| Table | Type | Purpose |
|---|---|---|
| `dim_index` | Dimension | Index reference; SCD Type 1 |
| `dim_fund` | Dimension | Fund reference; SCD Type 2 on Expense Ratio |
| `dim_date` | Dimension | Date spine; calendar and trading day attributes |
| `fact_nav_history` | Fact | Daily NAV and index price history; partitioned by year |
| `agg_period_returns` | Aggregate | Pre-computed returns for 1M, 1Y, 3Y, 5Y, inception per fund × index |
| `agg_monthly_trends` | Aggregate | Monthly NAV and index price aggregates |
| `agg_rolling_returns` | Aggregate | Trailing 30d, 90d, 365d returns per fund × index |
| `watch_list` | Reference | Persistent underperformer flags |
| `dq_audit_log` | Audit | Data quality imputation and transformation log |

### 12.4 Data Retention

| Data Type | Retention |
|---|---|
| Raw staging data | 90 days; then archived |
| Mart dimension and fact data | Indefinite |
| Aggregate tables | No history; full refresh daily |
| DQ audit logs and pipeline run logs | 12 months minimum |

---

## 13. User Stories

### Milestone 1 — Data Collection

**US-01:** As a data engineer, I want to configure a parameterised NSE India index extraction pipeline so that I can pull all index categories without writing separate scripts for each.

**US-02:** As a data engineer, I want the pipeline to automatically forward-fill missing NAV prices from the last available date so that the clean dataset has no gaps that would break return calculations.

**US-03:** As a data engineer, I want conflicting NAV records (same fund + date, different price) to raise an Antigravity ticket automatically so that I am alerted immediately and no silent data corruption occurs.

### Milestone 2 — Data Mart

**US-04:** As a data engineer, I want the Milestone 2 pipeline to start automatically as soon as the M1 quality gate passes so that there is no manual handoff delay between milestones.

**US-05:** As a portfolio manager, I want the system to automatically flag funds with negative average deviation in two or more periods so that I can identify persistent underperformers without manually scanning the comparison table.

**US-06:** As a project manager, I want the mart validation summary to be auto-generated and delivered to the stakeholder for sign-off so that the approval process is documented without email chains.

### Milestone 3 — Report Development

**US-07:** As a financial auditor, I want to select any NSE index from a Domain → Sector → Category hierarchy so that I can benchmark my fund against the most appropriate index for my audit category.

**US-08:** As a financial auditor, I want to see a side-by-side comparison of all in-scope funds against my selected index across 1M, 1Y, 3Y, 5Y, and since-inception periods in a single matrix table so that I can identify outliers at a glance.

**US-09:** As a financial auditor, I want to export the comparison table to Excel so that I can include it as evidence in my formal audit report.

**US-10:** As an ad-hoc analyst, I want to drill down from annual to monthly and then daily fund vs index trends on the chart so that I can investigate what caused a specific performance spike or dip.

**US-11:** As an ad-hoc analyst, I want tooltips on the trend chart to show the exact NAV price, index price, and deviation on any given date when I hover so that I can get precise numbers without switching pages.

**US-12:** As an ad-hoc analyst, I want the dashboard to open with a sensible default state (a pre-selected index and the last 1-year date range) so that I can immediately see meaningful data without configuration.

### Milestone 4 — Deployment

**US-13:** As a financial auditor, I want to access the dashboard via a web link without installing any software so that I can use it from any device on the company network.

**US-14:** As an IT admin, I want all data source credentials stored in the Antigravity secrets vault and never in report files so that credentials are not exposed when report files are shared.

**US-15:** As a BI admin, I want to receive an automated alert when the daily data refresh fails so that I can take action before stakeholders notice stale data.

---

## 14. Agentic Automation Requirements

The following agentic automations shall be configured in Antigravity IDE across all four milestones.

### 14.1 Scheduled Triggers

| Automation | Trigger | Action |
|---|---|---|
| Index extraction | Daily 07:00 IST | Run `stg_index_raw` extraction pipeline for all index categories |
| Fund data ingestion | On file arrival in drop folder | Run `stg_fund_raw` ingestion pipeline |
| Data cleaning pipeline | On completion of both extractions | Auto-run cleaning, deduplication, and standardisation pipeline |
| KPI recalculation | On completion of mart load | Recalculate all `agg_*` tables; update `watch_list` |
| Report refresh | Daily 08:00 IST | Trigger Streamlit / Plotly data refresh |

### 14.2 Quality Gates

| Gate | Condition | Block |
|---|---|---|
| M1 → M2 gate | Quality score ≥ 95% on critical fields | M2 pipeline blocked until gate passes |
| M2 → M3 gate | Stakeholder sign-off recorded in Antigravity | M3 tasks remain locked |
| M3 → M4 gate | All Critical + High UAT bugs resolved; sign-off recorded | M4 tasks remain locked |

### 14.3 Automated Alerts

| Alert | Trigger | Recipients |
|---|---|---|
| Extraction failure | Zero records returned or HTTP error | Data engineer |
| Conflicting NAV record | Same Fund Id + NAV date, different price | Data engineer + data owner |
| Quality gate failure | Quality score below threshold | Data engineer + PM |
| Fund deviation anomaly | Avg deviation > ±5% in any period | Portfolio manager |
| Mart refresh failure | Daily refresh does not complete by 08:30 IST | BI admin + data engineer |
| Report URL unreachable | Post-deploy HTTP check returns non-200 | BI admin |

### 14.4 Auto-Generated Reports

| Report | Trigger | Destination |
|---|---|---|
| Daily data quality summary | After each cleaning run | Attached to Antigravity M1 board |
| Mart validation summary | After M2 mart load | Attached to Antigravity M2 milestone; sent to stakeholder |
| Measure catalogue | After M3 measure build | Attached to Antigravity M3 board |
| UAT bug tracker digest | Daily during UAT | Sent to BI developer and PM |
| Project closure summary | On M4 milestone complete | Sent to all stakeholders |

---

## 15. Acceptance Criteria Summary

| ID | Requirement | Acceptance Criterion | Priority |
|---|---|---|---|
| FR-01 | Index ingestion | All NSE indices extracted; zero-record response triggers alert | Critical |
| FR-02 | Incremental load | No duplicate records on second run; watermark updated | Critical |
| FR-03 | Fund schema | All 9 fields populated; audit columns present | Critical |
| FR-04 | Fund ingestion | No duplicates; conflicts create Antigravity tickets | Critical |
| FR-05 | Missing values | No null NAV price in clean data; all imputations logged | Critical |
| FR-06 | Deduplication | Zero duplicate (Fund Id, NAV date) in clean output | Critical |
| FR-07 | Format standardisation | Zero non-conforming values in date, currency, category | High |
| FR-08 | Rating normalisation | All rated funds have original + normalized rating | High |
| FR-09 | M1 quality gate | Score ≥ 95%; M2 blocked until gate passes | Critical |
| FR-10 | Index dimension | All NSE indices present; no duplicate index_sk | Critical |
| FR-11 | Fund dimension | All funds present; expense ratio SCD Type 2 history correct | Critical |
| FR-13 | Fact table | Row count matches expected; zero orphaned FKs | Critical |
| FR-14 | Period returns | Verified vs hand-calc for 5 funds × 3 periods; < 0.01% error | Critical |
| FR-17 | Mart sign-off | All validation checks pass; stakeholder sign-off recorded | Critical |
| FR-18 | Semantic model | Star schema correct; no many-to-many relationships | Critical |
| FR-19 | Slicers | All 4 slicers functional; cross-filter < 3 seconds | Critical |
| FR-20 | Measures | All 6 measures match mart values; < 0.01% discrepancy | Critical |
| FR-21 | Summary page | KPI cards < 3s; drill-down at all 4 levels; tooltip complete | Critical |
| FR-22 | Fund detail | Drill-through correct; watch-list flag accurate | High |
| FR-23 | Comparison table | All funds shown; conditional formatting correct; export works for auditor | Critical |
| FR-25 | UAT | Zero Critical/High bugs at sign-off | Critical |
| FR-26 | Publication | Report accessible at production URL; HTTP 200 confirmed | Critical |
| FR-27 | RBAC | Auditor full access; ad-hoc read-only; server-level enforcement | Critical |
| FR-29 | Refresh | 5 consecutive successful daily refreshes; failure alert confirmed | Critical |
| FR-30 | Onboarding | All users logged in within 24 hours; walkthrough attended | High |
| NFR-01 | Performance | Pages < 5s; slicers < 3s | High |
| NFR-06 | Security | No hardcoded credentials; RBAC at server level | Critical |
| NFR-07 | Auditability | Full pipeline logs retained 12 months | High |

---

## 16. Risks and Mitigations

### Risk 1 — NSE India API Instability

**Probability:** Medium | **Impact:** High

The `nseindia.com` endpoint is a public data source with no guaranteed SLA. Rate limiting, IP blocking, or policy changes could disrupt daily extraction.

**Mitigation:**
- Implement retry logic with exponential backoff (3 retries before alert)
- Cache last successful extraction so mart is not empty on failure
- Evaluate alternative licensed NSE data vendors (e.g. NSE data feed subscription) as failover
- Alert data engineer within 5 minutes of extraction failure

---

### Risk 2 — Missing Inception Date for Historical Funds

**Probability:** Medium | **Impact:** Medium

Older funds may not have an Inception Date in their data feed, preventing since-inception calculations.

**Mitigation:**
- Flag affected funds as `DATA_ISSUE` in staging
- Resolve by manual lookup against AMFI fund registration data
- Since-inception metric displayed as N/A for flagged funds; not calculated from incorrect date
- Track open DATA_ISSUE flags in Antigravity; assign resolution to data owner

---

### Risk 3 — Conflicting NAV Records from Multiple Feeds

**Probability:** Low | **Impact:** High

Overlapping data feeds from different providers may deliver different NAV values for the same fund on the same date.

**Mitigation:**
- Automated conflict detection on (Fund Id, NAV date) composite key
- Both conflicting records excluded from clean dataset; Antigravity ticket auto-created
- No silent overwrite; data owner resolves conflict before records enter the mart
- Resolution SLA: 24 hours for data owner response

---

### Risk 4 — Report Performance Degradation at Scale

**Probability:** Medium | **Impact:** High

With 500+ funds and several years of daily NAV history, SQLAlchemy mode may be slow for complex slicer combinations.

**Mitigation:**
- Pre-aggregated tables (`agg_*`) used for all period return and trend visuals
- SQLAlchemy used only for raw detail drill-through page
- Year partitioning on `fact_nav_history` enforced from day one
- Performance test with full production dataset before deployment; optimise Python/Pandas if load time > 5 seconds
- Import mode with scheduled refresh as fallback if SQLAlchemy is too slow

---

### Risk 5 — Stakeholder Sign-off Delays at Milestone Gates

**Probability:** Medium | **Impact:** Medium

Delays in M2 or M3 stakeholder sign-off block subsequent milestones from starting, compressing the project timeline.

**Mitigation:**
- Automated validation reports generated and delivered to stakeholder on the same day as mart load or UAT completion
- Formal 48-hour SLA agreed with stakeholders for sign-off response
- Escalation path defined: PM escalates to product owner if SLA is breached
- M3 tasks can be partially started in parallel (UI wireframing) while awaiting M2 sign-off to reduce timeline risk

---

### Risk 6 — Expense Ratio SCD Type 2 Complexity

**Probability:** Low | **Impact:** Medium

Implementing SCD Type 2 for expense ratio incorrectly could result in duplicated or incorrect historical fund data in the mart.

**Mitigation:**
- SCD logic unit-tested with synthetic data covering: no change (single row), one change (two rows with closed prior), and multiple changes
- Validation check asserts no overlapping effective date ranges per fund in `dim_fund`
- Automated mart validation FR-17 includes effective date range gap and overlap check

---

## 17. Constraints and Assumptions

### Constraints

- Index data is limited to NSE India historical data for v1.0. BSE, global indices (S&P 500, MSCI, etc.) are out of scope.
- The reporting tool is Streamlit or Plotly only. Custom web dashboards or Excel-only delivery are not in scope for v1.0.
- All pipeline and mart work is delivered on the client's existing on-premise or cloud database infrastructure. Cloud migration is not in scope.
- The project timeline is fixed at 6.5 weeks across four milestones as defined in the Antigravity project plan. Timeline changes require product owner approval.
- Data freshness is T+1 (previous trading day) at 08:30 IST. Real-time or intraday data is not supported.
- Fund data must be provided by the client or sourced from AMFI public NAV files; the system does not procure fund data independently.

### Assumptions

- The client has an existing database environment (SQL Server, PostgreSQL, or similar) to host the data mart.
- The client has an active Streamlit Pro/Premium or Streamlit Cloud/Online license for report deployment.
- Financial auditors and ad-hoc users have corporate email accounts for access provisioning.
- The client's IT admin has the permissions required to configure gateway connections and RBAC on Streamlit Cloud or Streamlit Cloud.
- NSE India historical index data is publicly accessible at the time of development.
- The fund master reference table (used for lookups in FR-05 and FR-07) will be provided by the client before Milestone 1 begins.
- The project manager has full administrative access to the Antigravity IDE workspace for milestone and automation configuration.

---

## 18. Milestone Summary & Timeline

| Milestone | Description | Duration | Key Deliverable | Gate |
|---|---|---|---|---|
| **M1** | Data Collection & Pre-processing | 2 weeks | Cleaned, quality-gated staging dataset | Quality score ≥ 95% |
| **M2** | Data Mart Loading | 1.5 weeks | Populated mart with KPIs and aggregates | Stakeholder sign-off |
| **M3** | Report Development | 2 weeks | Interactive 3-page dashboard; UAT passed | UAT sign-off |
| **M4** | Deployment | 1 week | Live report; RBAC active; refresh scheduled | Go-live confirmation |
| **Total** | | **6.5 weeks** | | |

### Milestone Dependency Chain

```
M1 Quality Gate PASS
       |
       v
M2 Mart Load → M2 Validation → Stakeholder Sign-off
                                       |
                                       v
                              M3 Report Development → UAT → UAT Sign-off
                                                                  |
                                                                  v
                                                         M4 Deployment → Go-live
```

---

## 19. Glossary

| Term | Definition |
|---|---|
| **NAV (Net Asset Value)** | The per-unit price of a mutual fund, calculated and published daily after market close |
| **Index** | A market benchmark (e.g. Nifty 50, Nifty Bank) representing the aggregate performance of a group of securities |
| **Benchmark** | The index selected by the user for comparison against a fund's performance |
| **Deviation** | Fund Return % minus Index Return % over the same period. Positive = outperformed; Negative = underperformed |
| **Average Deviation** | The mean of daily (fund return − index return) differences over a selected period |
| **Period Return** | The percentage change in price (NAV or index) over a defined time window (1M, 1Y, 3Y, 5Y, since inception) |
| **Since Inception** | A return period calculated from a fund's official inception date to the current date |
| **Watch-list** | A system-generated list of funds flagged as persistent underperformers based on negative average deviation across two or more standard periods |
| **SCD Type 1** | Slowly Changing Dimension Type 1 — overwrites old value with new value; no history kept |
| **SCD Type 2** | Slowly Changing Dimension Type 2 — preserves full history of attribute changes using effective start/end dates |
| **Python/Pandas** | Data Analysis Expressions — the formula language used in Streamlit for calculated measures and columns |
| **SQLAlchemy** | A Streamlit connection mode that sends live queries to the data source rather than importing data into the model |
| **Watermark** | A stored value (typically the maximum loaded date) used to drive incremental data loads and prevent re-processing |
| **Data Mart** | A subject-specific, structured database designed to serve a particular reporting or analytics domain |
| **KPI** | Key Performance Indicator — a quantifiable metric used to evaluate performance (e.g. Fund Return %, Deviation %) |
| **RBAC** | Role-Based Access Control — a method of restricting system access based on a user's role |
| **ETL** | Extract, Transform, Load — the process of pulling data from sources, transforming it, and loading it into a target store |
| **DQ** | Data Quality — a measure of how well data meets defined standards for completeness, accuracy, consistency, and timeliness |
| **UAT** | User Acceptance Testing — a phase of testing where real users validate that the system meets their requirements |
| **Antigravity IDE** | The integrated development and project management environment used to manage this project's milestones, automations, and pipelines |

---

*Product Requirements Document v1.0 — Fund Index Analysis System*
*Prepared for Antigravity IDE — Academic Submission — April 27, 2026*
