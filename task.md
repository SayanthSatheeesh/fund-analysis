# Task Breakdown — Fund Index Analysis System
## PRD v1.0 Implementation Plan

---

> [!IMPORTANT]
> **Do NOT begin execution until all BLOCKER decisions (Section 1) are resolved.**
> This document maps every PRD requirement (FR-01 → FR-30, NFR-01 → NFR-08) to actionable tasks.

---

## 0. Technology Stack (Recommended)

| Layer | Technology | Rationale |
|---|---|---|
| **Database** | PostgreSQL 16+ | Native table partitioning, JSONB, window functions, free |
| **ETL / Pipeline** | Python 3.11+ (pandas, sqlalchemy, psycopg2) | Fastest to build; rich data libs |
| **Scheduling** | Python APScheduler / cron | Lightweight; no infra overhead for 6.5-week project |
| **Data Extraction** | `jugaad_data` / `nselib` (NSE), `mftool` (AMFI NAV) | Best available OSS packages for Indian market data |
| **Reporting** | Streamlit (SQLAlchemy) | PRD mandated; Plotly as alternative |
| **Version Control** | Git | Schema migrations + pipeline scripts |
| **Config / Secrets** | python-dotenv + .env file (dev) | Simple; upgrade to vault in production |

---

## 1. Pre-Implementation Decisions (BLOCKERS)

These decisions MUST be made before any task execution begins. They affect the entire architecture.

| ID | Decision | Options | Impact | Status |
|---|---|---|---|---|
| **D-001** | Database engine | PostgreSQL (recommended) / SQLite (prototype) / SQL Server | All schema, partitioning, SCD logic depends on this | ⬜ PENDING |
| **D-002** | NSE data access method | Mock data generator / Manual CSV download | Determines M1 extraction pipeline design | ✅ RESOLVED (Mock Data) |
| **D-003** | Fund NAV data source | AMFI public NAV (`mftool`) / Client-provided CSV / Both | Determines M1 ingestion pipeline design | ⬜ PENDING |
| **D-004** | Reporting tool | Streamlit / Plotly Dash | Affects M3 + M4 entirely | ⬜ PENDING |
| **D-005** | Deployment target | Local dev only / Client server / Cloud (Azure/AWS) | Affects M4 scope | ⬜ PENDING |
| **D-006** | Fund rating data source | Client-provided / Mock data / Web scrape | FR-08 depends on this | ✅ RESOLVED (Mock Data) |

---

## 2. Task Registry

### Legend

| Symbol | Meaning |
|---|---|
| 🔴 | Critical priority |
| 🟠 | High priority |
| 🟡 | Medium priority |
| 🟢 | Low priority |
| ⬜ | Not started |
| 🔲 | Blocked |
| 🔵 | In progress |
| ✅ | Complete |

---

## Milestone 1 — Data Collection & Pre-processing (Weeks 1–2)

### Phase 1A: Environment Setup

| ID | Task | PRD Ref | Priority | Effort | Depends On | Status |
|---|---|---|---|---|---|---|
| **T-001** | Initialize project structure (folders, configs, `requirements.txt`, `.env.example`) | — | 🔴 | 2h | D-001 | ⬜ |
| **T-002** | Set up database server and create `fund_analysis` database | — | 🔴 | 2h | D-001 | ⬜ |
| **T-003** | Create staging table schemas (`stg_index_raw`, `stg_fund_raw`) | FR-01, FR-03 | 🔴 | 3h | T-002 | ⬜ |
| **T-004** | Create `dq_audit_log` table schema | FR-05 | 🔴 | 1h | T-002 | ⬜ |
| **T-005** | Create `pipeline_run_log` table for pipeline execution tracking | NFR-07 | 🟠 | 2h | T-002 | ⬜ |
| **T-006** | Create `watermark` table for incremental load state | FR-02, FR-04 | 🔴 | 1h | T-002 | ⬜ |
| **T-007** | Build database connection utility module (`db.py`) | — | 🔴 | 2h | T-002 | ⬜ |

**Acceptance Criteria — Phase 1A:**
- [ ] All tables created and verified via `\dt` or equivalent
- [ ] Connection utility connects and executes a test query
- [ ] `.env.example` documents all required environment variables

---

### Phase 1B: NSE Index Data Pipeline

| ID | Task | PRD Ref | Priority | Effort | Depends On | Status |
|---|---|---|---|---|---|---|
| **T-008** | Build mock data generator for NSE index data | FR-01 | 🔴 | 4h | D-002, T-007 | ⬜ |
| **T-009** | Parameterize mock data generation for all index categories | FR-01 | 🔴 | 2h | T-008 | ⬜ |
| **T-010** | (Removed due to mock data approach) | FR-01 | 🟢 | 0h | — | ✅ |
| **T-011** | Write mock data to `stg_index_raw` with generated timestamps | FR-01 | 🔴 | 2h | T-009, T-003 | ⬜ |
| **T-012** | Implement watermark-based incremental mock load | FR-02 | 🔴 | 2h | T-011, T-006 | ⬜ |
| **T-013** | (Removed due to mock data approach) | FR-01 | 🟢 | 0h | — | ✅ |

**Acceptance Criteria — Phase 1B:**
- [ ] Mock generator creates realistic index data for at least 3 categories
- [ ] `stg_index_raw` populated with generated timestamps and source identifiers
- [ ] Second run with same parameters inserts zero duplicate records

---

### Phase 1C: Fund NAV Data Pipeline

| ID | Task | PRD Ref | Priority | Effort | Depends On | Status |
|---|---|---|---|---|---|---|
| **T-014** | Research fund data source — prototype extraction for 1 fund | FR-03 | 🔴 | 4h | D-003, T-007 | ⬜ |
| **T-015** | Build fund data ingestion pipeline (support CSV + API) | FR-03 | 🔴 | 6h | T-014, T-003 | ⬜ |
| **T-016** | Populate all 9 required business fields + audit columns (`load_id`, `load_timestamp`) | FR-03 | 🔴 | 2h | T-015 | ⬜ |
| **T-017** | Implement watermark-based incremental fund load per Fund Id | FR-04 | 🔴 | 4h | T-015, T-006 | ⬜ |
| **T-018** | Implement conflict detection (same Fund Id + NAV date, different NAV price) | FR-04 | 🔴 | 4h | T-017 | ⬜ |
| **T-019** | Create fund master reference table (for lookups in cleaning phase) | FR-05, FR-07 | 🟠 | 3h | T-002 | ⬜ |

**Acceptance Criteria — Phase 1C:**
- [ ] All 9 business fields populated for every fund record
- [ ] Surrogate key (`load_id`) and `load_timestamp` present on every row
- [ ] Duplicate fund records not inserted on incremental runs
- [ ] Conflicting records detected and logged as data issues

---

### Phase 1D: Data Cleaning & Standardization

| ID | Task | PRD Ref | Priority | Effort | Depends On | Status |
|---|---|---|---|---|---|---|
| **T-020** | Implement missing value handler: NAV forward-fill, Exchange/Currency lookup, Inception date flagging | FR-05 | 🔴 | 6h | T-015, T-019 | ⬜ |
| **T-021** | Implement DQ audit logging for all imputation actions | FR-05 | 🔴 | 4h | T-020, T-004 | ⬜ |
| **T-022** | Implement duplicate detection and resolution (identical vs conflicting) | FR-06 | 🔴 | 4h | T-020 | ⬜ |
| **T-023** | Implement format standardization (dates, currencies, categories, Fund IDs, NAV price) | FR-07 | 🟠 | 5h | T-020 | ⬜ |
| **T-024** | Generate mock fund ratings (1–5 scale from CRISIL/Morningstar/SEBI) | FR-08 | 🟠 | 2h | D-006, T-019 | ⬜ |
| **T-025** | Create `stg_fund_clean` and `stg_index_clean` output tables | FR-05, FR-06, FR-07 | 🔴 | 2h | T-020 | ⬜ |

**Acceptance Criteria — Phase 1D:**
- [ ] Zero null NAV price values in cleaned output
- [ ] All imputation actions in `dq_audit_log` with original + imputed values
- [ ] Zero duplicate (Fund Id, NAV date) in cleaned output
- [ ] Zero non-conforming date/currency/category values
- [ ] Rated funds have both `original_rating` and `normalized_rating`

---

### Phase 1E: M1 Quality Gate

| ID | Task | PRD Ref | Priority | Effort | Depends On | Status |
|---|---|---|---|---|---|---|
| **T-026** | Build automated quality gate checks (null rate, dup rate, format conformance, DATA_ISSUE flags) | FR-09 | 🔴 | 4h | T-025 | ⬜ |
| **T-027** | Generate quality score report (auto-generated, exportable) | FR-09 | 🔴 | 3h | T-026 | ⬜ |
| **T-028** | Implement gate pass/fail logic (blocks M2 if FAIL) | FR-09 | 🟠 | 2h | T-027 | ⬜ |

**Acceptance Criteria — Phase 1E:**
- [ ] Automated quality score generated after each cleaning run
- [ ] Gate status (PASS / FAIL) clearly reported
- [ ] M2 pipeline does not execute if gate status is FAIL
- [ ] Quality report saved as downloadable file

---

## Milestone 2 — Data Mart Loading (Weeks 3–4.5)

### Phase 2A: Dimension Tables

| ID | Task | PRD Ref | Priority | Effort | Depends On | Status |
|---|---|---|---|---|---|---|
| **T-029** | Create and populate `dim_index` table (all NSE indices, SCD Type 1) | FR-10 | 🔴 | 4h | T-028 (gate PASS) | ⬜ |
| **T-030** | Create and populate `dim_fund` table with SCD Type 2 logic for `expense_ratio` | FR-11 | 🔴 | 8h | T-028 (gate PASS) | ⬜ |
| **T-031** | Source NSE holiday calendar data (static annual list) | FR-12 | 🟠 | 3h | — | ⬜ |
| **T-032** | Generate `dim_date` table (full date spine, `is_trading_day`, `is_holiday` flags) | FR-12 | 🔴 | 4h | T-031 | ⬜ |

**Acceptance Criteria — Phase 2A:**
- [ ] All NSE indices present in `dim_index` with no gaps in hierarchy
- [ ] All funds have at least one current row (`is_current = TRUE`) in `dim_fund`
- [ ] Expense ratio SCD Type 2 history has no gaps or overlaps in effective dates
- [ ] `dim_date` covers full range from earliest inception date to today with zero gaps
- [ ] `is_trading_day` correctly excludes weekends and NSE holidays

---

### Phase 2B: Fact Table

| ID | Task | PRD Ref | Priority | Effort | Depends On | Status |
|---|---|---|---|---|---|---|
| **T-033** | Create `fact_nav_history` table with year-based partitioning | FR-13 | 🔴 | 4h | T-029, T-030, T-032 | ⬜ |
| **T-034** | Build ETL to populate fact table from cleaned staging data | FR-13 | 🔴 | 6h | T-033 | ⬜ |
| **T-035** | Create performance indexes on (`fund_sk`, `date_id`) and (`index_sk`, `date_id`) | FR-13 | 🟠 | 1h | T-034 | ⬜ |
| **T-036** | Validate referential integrity (all FKs resolve to dimension tables) | FR-13 | 🔴 | 2h | T-034 | ⬜ |

**Acceptance Criteria — Phase 2B:**
- [ ] Row count = expected fund × trading day combinations
- [ ] Zero orphaned foreign keys
- [ ] Year partitioning confirmed in database schema
- [ ] Query performance acceptable with indexes in place

---

### Phase 2C: Aggregate & KPI Tables

| ID | Task | PRD Ref | Priority | Effort | Depends On | Status |
|---|---|---|---|---|---|---|
| **T-037** | Build `agg_period_returns` pipeline (1M, 1Y, 3Y, 5Y, inception for all fund × index) | FR-14 | 🔴 | 8h | T-034 | ⬜ |
| **T-038** | Build `agg_monthly_trends` pipeline (avg NAV, month-end NAV, monthly returns) | FR-15 | 🟠 | 4h | T-034 | ⬜ |
| **T-039** | Build `agg_rolling_returns` pipeline (trailing 30d, 90d, 365d) | FR-15 | 🟠 | 5h | T-034 | ⬜ |
| **T-040** | Build `watch_list` logic (negative avg deviation in 2+ periods → flag) | FR-16 | 🟠 | 4h | T-037 | ⬜ |
| **T-041** | Verify KPI accuracy: hand-calculate for 5 funds × 3 periods; discrepancy < 0.01% | FR-14 | 🔴 | 4h | T-037 | ⬜ |

**Acceptance Criteria — Phase 2C:**
- [ ] All 5 periods × all fund × index combinations in `agg_period_returns`
- [ ] Funds with null inception_date show NULL for since-inception fields
- [ ] Monthly aggregates cover all fund × year/month with no gaps
- [ ] Rolling returns updated within 15 minutes of daily mart refresh
- [ ] Watch-list correctly flags funds with negative deviation in 2+ periods
- [ ] Manual verification < 0.01% discrepancy for sampled calculations

---

### Phase 2D: Mart Validation & Sign-off

| ID | Task | PRD Ref | Priority | Effort | Depends On | Status |
|---|---|---|---|---|---|---|
| **T-042** | Implement automated validation suite (row count, null, range, date gap, RI, aggregate coverage) | FR-17 | 🔴 | 5h | T-037, T-038, T-039, T-040 | ⬜ |
| **T-043** | Generate mart validation summary report | FR-17 | 🔴 | 3h | T-042 | ⬜ |

**Acceptance Criteria — Phase 2D:**
- [ ] All 7 validation checks pass with zero failures
- [ ] Validation report generated as downloadable document
- [ ] Stakeholder sign-off recorded before M3 begins

---

## Milestone 3 — Report Development (Weeks 4.5–6.5)

### Phase 3A: Semantic Model & Measures

| ID | Task | PRD Ref | Priority | Effort | Depends On | Status |
|---|---|---|---|---|---|---|
| **T-044** | Create Streamlit / Plotly connection to data mart (SQLAlchemy / Live) | FR-18 | 🔴 | 3h | T-043, D-004 | ⬜ |
| **T-045** | Define semantic model relationships (dim→fact, star schema) | FR-18 | 🔴 | 2h | T-044 | ⬜ |
| **T-046** | Implement all 6 Pandas aggregations / Plotly calculated fields | FR-20 | 🔴 | 6h | T-045 | ⬜ |
| **T-047** | Create measure catalogue documentation | FR-20 | 🟠 | 3h | T-046 | ⬜ |

**Acceptance Criteria — Phase 3A:**
- [ ] Star schema with 3 relationships, single-direction filtering, no many-to-many
- [ ] All 6 measures implemented and responsive to slicer context
- [ ] Measure catalogue complete with formula, purpose, edge cases

---

### Phase 3B: Dashboard Pages (Manual GUI Work)

> [!NOTE]
> Tasks T-048 to T-052 require manual effort within the Streamlit / Plotly Dash GUI and cannot be code-generated.

| ID | Task | PRD Ref | Priority | Effort | Depends On | Status |
|---|---|---|---|---|---|---|
| **T-048** | [AUTOMATED] Build Page 1: Summary (KPI cards, dual-axis trend chart, drill-down, tooltips) | FR-21 | 🔴 | 8h | T-046 | ⬜ |
| **T-049** | [AUTOMATED] Build Page 2: Fund Detail (drill-through, 6 KPIs, period return bars, expense ratio trend, watch-list flag) | FR-22 | 🔴 | 8h | T-046 | ⬜ |
| **T-050** | [AUTOMATED] Build Page 3: Multi-Fund Comparison (matrix, conditional formatting, sort, export) | FR-23 | 🔴 | 6h | T-046 | ⬜ |
| **T-051** | [AUTOMATED] Configure 4 interactive slicers (date range, index hierarchy, fund type, exchange) | FR-19 | 🔴 | 4h | T-048 | ⬜ |
| **T-052** | [AUTOMATED] Implement drill-down navigation (Year → Quarter → Month → Day) on all time-axis visuals | FR-24 | 🟠 | 3h | T-048 | ⬜ |

**Acceptance Criteria — Phase 3B:**
- [ ] All 3 pages functional with correct data
- [ ] KPI cards update < 3 seconds on slicer change
- [ ] Drill-down works at all 4 levels
- [ ] Tooltips display fund name, date, NAV, index price, deviation
- [ ] Conditional formatting: green positive / red negative deviations
- [ ] Export to Excel functional for Auditor role

---

### Phase 3C: UAT

| ID | Task | PRD Ref | Priority | Effort | Depends On | Status |
|---|---|---|---|---|---|---|
| **T-053** | Prepare UAT test script (10 scenarios) | FR-25 | 🟠 | 4h | T-050 | ⬜ |
| **T-054** | Execute UAT with minimum 2 auditors + 1 ad-hoc user | FR-25 | 🔴 | 8h | T-053 | ⬜ |
| **T-055** | Resolve all Critical and High severity bugs | FR-25 | 🔴 | 8h | T-054 | ⬜ |
| **T-056** | Obtain UAT sign-off document | FR-25 | 🔴 | 1h | T-055 | ⬜ |

**Acceptance Criteria — Phase 3C:**
- [ ] UAT conducted with required participants
- [ ] Zero open Critical or High bugs at sign-off
- [ ] UAT sign-off document generated

---

## Milestone 4 — Deployment (Week 7)

### Phase 4A: Publication & Access

| ID | Task | PRD Ref | Priority | Effort | Depends On | Status |
|---|---|---|---|---|---|---|
| **T-057** | Publish report to Streamlit Cloud / Streamlit Cloud | FR-26 | 🔴 | 3h | T-056 | ⬜ |
| **T-058** | Verify report accessible at production URL (HTTP 200) | FR-26 | 🔴 | 1h | T-057 | ⬜ |
| **T-059** | Configure RBAC: Auditor role (full access + export) and Ad-hoc User role (read-only, no drill-through) | FR-27 | 🔴 | 4h | T-057 | ⬜ |
| **T-060** | Test access revocation (remove user from role → verify access removed) | FR-27 | 🟠 | 2h | T-059 | ⬜ |

**Acceptance Criteria — Phase 4A:**
- [ ] Report loads at production URL with all 3 pages
- [ ] Auditor can access all pages, drill-through, and export
- [ ] Ad-hoc user cannot see fund detail page or export
- [ ] Access revocation removes access immediately

---

### Phase 4B: Scheduling & Alerts

| ID | Task | PRD Ref | Priority | Effort | Depends On | Status |
|---|---|---|---|---|---|---|
| **T-061** | Configure daily data refresh at 08:00 IST | FR-29 | 🔴 | 3h | T-057 | ⬜ |
| **T-062** | Set up failure alert emails (BI admin + data engineer) | FR-29 | 🟠 | 3h | T-061 | ⬜ |
| **T-063** | Verify 5 consecutive successful daily refreshes | FR-29 | 🔴 | 5d | T-061 | ⬜ |
| **T-064** | Test failure alert (deliberately break credentials → verify alert within 5 min) | FR-29 | 🟠 | 1h | T-062 | ⬜ |

**Acceptance Criteria — Phase 4B:**
- [ ] Daily refresh runs at 08:00 IST automatically
- [ ] 5 consecutive successful refreshes confirmed
- [ ] Failure alert received within 5 minutes of deliberately broken refresh

---

### Phase 4C: Onboarding & Go-Live

| ID | Task | PRD Ref | Priority | Effort | Depends On | Status |
|---|---|---|---|---|---|---|
| **T-065** | Create Quick Start Guide (index selection, date range, deviation, drill-down, export) | FR-30 | 🟠 | 4h | T-057 | ⬜ |
| **T-066** | Conduct 30-minute live walkthrough for financial auditors | FR-30 | 🟠 | 2h | T-065 | ⬜ |
| **T-067** | Distribute access credentials / SSO instructions to all users | FR-30 | 🔴 | 1h | T-059 | ⬜ |
| **T-068** | Configure weekly email subscription (optional — if stakeholder opts in) | FR-30 | 🟢 | 2h | T-057 | ⬜ |
| **T-069** | Go-live verification: all users logged in within 24 hours | FR-30 | 🔴 | 1h | T-067 | ⬜ |

**Acceptance Criteria — Phase 4C:**
- [ ] Quick Start Guide covers all 5 required topics
- [ ] Walkthrough attended by minimum 2 auditors
- [ ] All users logged in independently within 24 hours

---

## 3. Critical Path

```
D-001 (DB Choice) → T-002 (Setup DB) → T-003 (Staging Schema) → T-011 (Load Index) ─┐
D-002 (NSE Access) → T-008 (Prototype NSE) → T-009 (Build Extraction) → T-011 ────────┤
D-003 (Fund Source) → T-014 (Prototype Fund) → T-015 (Load Fund) ──────────────────────┤
                                                                                        │
T-020 (Clean Data) ← ──────────────────────────────────────────────────────────── ←──────┘
        │
        v
T-026 (Quality Gate) → T-029/T-030 (Dimensions) → T-034 (Fact ETL) → T-037 (KPIs)
        │
        v
T-042 (Mart Validation) → T-044 (BI Connection) → T-046 (Measures) → T-048 (Dashboard)
        │
        v
T-054 (UAT) → T-057 (Publish) → T-069 (Go-Live)
```

**Critical path duration:** ~6.5 weeks (matching PRD timeline)

---

## 4. Effort Summary

| Milestone | Phase | Est. Hours |
|---|---|---|
| **M1** | 1A: Environment Setup | 13h |
| **M1** | 1B: NSE Index Pipeline | 21h |
| **M1** | 1C: Fund NAV Pipeline | 23h |
| **M1** | 1D: Cleaning & Standardization | 25h |
| **M1** | 1E: Quality Gate | 9h |
| | **M1 Total** | **91h** |
| **M2** | 2A: Dimension Tables | 19h |
| **M2** | 2B: Fact Table | 13h |
| **M2** | 2C: Aggregates & KPIs | 25h |
| **M2** | 2D: Mart Validation | 8h |
| | **M2 Total** | **65h** |
| **M3** | 3A: Semantic Model | 14h |
| **M3** | 3B: Dashboard Pages | 29h |
| **M3** | 3C: UAT | 21h |
| | **M3 Total** | **64h** |
| **M4** | 4A: Publication & Access | 10h |
| **M4** | 4B: Scheduling & Alerts | 12h |
| **M4** | 4C: Onboarding & Go-Live | 10h |
| | **M4 Total** | **32h** |
| | **GRAND TOTAL** | **252h** |

---

## 5. PRD Requirement → Task Traceability

| PRD Req | Tasks |
|---|---|
| FR-01 | T-008, T-009, T-010, T-011, T-013 |
| FR-02 | T-006, T-012 |
| FR-03 | T-003, T-015, T-016 |
| FR-04 | T-006, T-017, T-018 |
| FR-05 | T-004, T-019, T-020, T-021 |
| FR-06 | T-022 |
| FR-07 | T-023 |
| FR-08 | T-024 |
| FR-09 | T-026, T-027, T-028 |
| FR-10 | T-029 |
| FR-11 | T-030 |
| FR-12 | T-031, T-032 |
| FR-13 | T-033, T-034, T-035, T-036 |
| FR-14 | T-037, T-041 |
| FR-15 | T-038, T-039 |
| FR-16 | T-040 |
| FR-17 | T-042, T-043 |
| FR-18 | T-044, T-045 |
| FR-19 | T-051 |
| FR-20 | T-046, T-047 |
| FR-21 | T-048 |
| FR-22 | T-049 |
| FR-23 | T-050 |
| FR-24 | T-052 |
| FR-25 | T-053, T-054, T-055, T-056 |
| FR-26 | T-057, T-058 |
| FR-27 | T-059, T-060 |
| FR-29 | T-061, T-062, T-063, T-064 |
| FR-30 | T-065, T-066, T-067, T-068, T-069 |
| NFR-01 | T-035 (indexes), T-037–T-039 (pre-aggregation) |
| NFR-06 | T-004 (secrets handling), T-059 (RBAC) |
| NFR-07 | T-005, T-021 (audit logging) |
