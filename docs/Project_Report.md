# Project Report

| Project Detail | Information |
| :--- | :--- |
| **Industry Project Title** | Fund Index Analysis |
| **Name** | Sayanth Satheesh |
| **Name of the Institute** | Lead College (Autonomous) |
| **Start Date / End Date** | [To be filled by student] |
| **Total Effort (hrs.)** | [To be filled by student] |
| **Project Environment** | Windows Desktop, VS Code, Python Environment |
| **Tools Used** | Python, Pandas, PostgreSQL, SQLAlchemy, Streamlit, Power BI, Plotly |

---

## Table of Contents

1. Acknowledgements
2. Objective and Scope
3. Problem Statement
4. Existing Approaches
5. Approach / Methodology - Tools and Technologies Used
6. Workflow
7. Assumptions
8. Implementation
   - Data Collection
   - Processing Steps
   - Diagrams – Charts, Tables
9. Solution Design
10. Challenges & Opportunities
11. Reflections on the Project
12. Recommendations
13. Outcome / Conclusion
14. Enhancement Scope
15. Link to Code and Executable File
16. Research Questions and Responses
17. References

---

## 1. Acknowledgements

I would like to express my sincere gratitude to Lead College (Autonomous) and my project guides for their continuous support and guidance throughout the duration of this industry project. Their expertise and encouragement were instrumental in shaping the architecture and implementation of the Fund Index Analysis system. I also acknowledge the open-source community for providing robust libraries such as Pandas, SQLAlchemy, and Streamlit, which formed the technical foundation of this analytical suite.

## 2. Objective and Scope

The primary objective of the Fund Index Analysis project is to design and develop a fully automated, end-to-end data engineering and business intelligence pipeline. The system tracks the daily Net Asset Value (NAV) of various mutual funds and measures their performance against established market benchmarks (such as NIFTY 50, NIFTY BANK, and NIFTY IT). 

The scope of the project encompasses:
- Automated extraction of market index data and fund NAV data.
- Data cleaning, standardization, and quality gate enforcement.
- Transformation of raw data into a Star Schema data mart (dimension and fact tables) hosted on a PostgreSQL database.
- Calculation of key financial metrics, including period returns, tracking error, and deviation (Alpha).
- Presentation of insights through an interactive, Python-based Streamlit dashboard and Power BI templates.

## 3. Problem Statement

Investors and financial analysts frequently struggle to compare the performance of mutual funds against their respective benchmark indices due to fragmented data sources, inconsistent formatting, and the latency of manual reporting. Without a centralized, automated system to calculate tracking errors, period returns (1M, 3M, 1Y), and rolling returns, stakeholders cannot efficiently identify underperforming funds or assess true risk-adjusted returns (Alpha). There is a critical need for an automated data pipeline that continuously ingests daily market data, processes it into a reliable data warehouse, and serves real-time visualizations for decision-making.

## 4. Existing Approaches

Traditional approaches to fund index analysis generally fall into two categories:
1. **Manual Spreadsheet Analysis:** Financial analysts manually download historical CSV files from stock exchanges and fund houses, compiling them into Excel. This approach is highly prone to human error, lacks scalability, and fails to provide real-time insights.
2. **Proprietary Institutional Software:** Large financial institutions utilize expensive tools like Bloomberg Terminals or Morningstar Direct. While powerful, these systems are cost-prohibitive for individual analysts or small firms and lack the flexibility for custom data engineering pipelines.

## 5. Approach / Methodology - Tools and Technologies Used

This project adopts a modern Data Engineering methodology, utilizing an ELT (Extract, Load, Transform) architecture combined with a customized Business Intelligence semantic layer.

**Tools and Technologies Used:**
- **Programming Language:** Python (Core logic, pipeline orchestration)
- **Data Processing:** Pandas, NumPy (Data cleaning, statistical calculations)
- **Database Architecture:** PostgreSQL (Relational Data Mart), SQLAlchemy (ORM and query execution)
- **Visualization:** Streamlit, Plotly (Automated web dashboard), Power BI (GUI-based reporting)
- **Environment:** dotenv (Configuration management)

The methodology focuses on modularity, utilizing distinct scripts for extraction (`nse_index.py`, `fund_nav.py`), transformation (`fact_loader.py`, `dim_loader.py`), and visualization (`app.py`), ensuring that each component can be scaled or modified independently.

## 6. Workflow

1. **Orchestration:** The master script (`run_all.py`) triggers the daily execution cycle.
2. **Data Extraction:** Mock data generators simulate daily closing prices and volumes for major indices (NIFTY 50) and fund NAVs, tracking watermarks to ensure only incremental data is loaded.
3. **Data Quality Gate:** Extracted data passes through a quality validation layer. Records failing validation (e.g., missing prices) are logged to `dq_audit_log`.
4. **Data Mart Loading:** Cleaned data is upserted into a PostgreSQL Star Schema. Slowly Changing Dimensions (SCD) are handled in `dim_fund` and `dim_index`, while daily prices populate `fact_nav_history`.
5. **Aggregation:** SQL views and Python scripts calculate rolling returns, watch list status, and period performance.
6. **Visualization:** The Streamlit dashboard queries the PostgreSQL views in real-time to render dual-axis charts, KPI cards, and performance matrices.

## 7. Assumptions

- **Data Availability:** It is assumed that simulated data accurately reflects the statistical behavior (random walk volatility) of actual NSE/BSE stock indices.
- **Trading Days:** The system assumes a standard 5-day business week for index trading, handling missing weekend dates via forward-fill techniques if necessary.
- **Database Concurrency:** PostgreSQL is assumed to be running locally on the standard port (5432) to facilitate the Streamlit application's real-time queries.

## 8. Implementation

### Data Collection
Data collection is handled via Python extraction scripts. For the purpose of this project environment, realistic OHLCV (Open, High, Low, Close, Volume) data is generated dynamically using Numpy's random normal distribution to simulate market volatility (`nse_index.py`). The pipeline implements a "watermark" table to track the `last_processed_date` for each entity, ensuring that subsequent pipeline runs only extract and append new daily records rather than reprocessing historical data.

### Processing Steps
1. **Staging:** Raw data is loaded into `stg_index_raw` and `stg_fund_raw`.
2. **Cleaning:** Null values are handled, and currencies are standardized.
3. **Dimension Loading:** Data is inserted into `dim_index`, `dim_fund`, and a pre-generated `dim_date` table.
4. **Fact Loading:** The `fact_nav_history` table joins funds, indices, and dates, calculating the precise `daily_return` and `index_daily_return`.
5. **Business Logic:** The `watch_list` table is populated by flagging funds that exhibit consecutive periods of negative Alpha against their benchmark.

### Diagrams – Charts, Tables
*(Note: In the final PDF submission, insert actual screenshots of the Streamlit dashboard here)*
- **Figure 1:** Dual-Axis Line Chart comparing Fund NAV vs. Index Price over the 1-year time period.
- **Figure 2:** Clustered Bar Chart illustrating 1M, 3M, and 1Y period returns.
- **Table 1:** Multi-Fund Matrix showcasing conditionally formatted (Red/Green) monthly returns.

## 9. Solution Design

The solution is designed around a strict Star Schema database model to optimize read performance for the BI layer. 

- **Central Fact Table:** `fact_nav_history` (Stores daily prices and tracking errors).
- **Dimension Tables:** `dim_fund` (Stores fund metadata and expense ratios), `dim_index` (Stores benchmark details), and `dim_date` (Stores year, quarter, and month hierarchies).
- **Semantic Views:** To decouple the BI layer from the raw tables, three SQL views were created: `v_trend_history`, `v_period_performance`, and `v_monthly_comparison`. The Streamlit application queries only these views, ensuring that structural changes to the fact tables do not break the dashboard.

## 10. Challenges & Opportunities

**Challenges:**
- **Database Migration:** Initially built on SQLite, the system faced file-locking constraints when attempting to run the ETL pipeline and the visualization dashboard concurrently. This was resolved by migrating the entire schema and data to PostgreSQL, which natively supports high concurrency.
- **Calculation Complexity:** Accurately calculating rolling returns and standard deviation (Tracking Error) required complex SQL window functions and Pandas aggregations.

**Opportunities:**
- The current architecture is highly scalable. The mock data generators can be seamlessly replaced with live API integrations (e.g., NSE API, Yahoo Finance) without altering the downstream data mart or dashboard.

## 11. Reflections on the Project

Developing the Fund Index Analysis system provided profound insights into the intersection of software engineering and financial analytics. Building the data pipeline underscored the importance of robust data modeling—specifically the implementation of Star Schemas and SCD Type 2 dimensions. Transitioning from a manual Power BI methodology to a fully automated Streamlit web application highlighted the immense efficiency gains of "Dashboard-as-Code," allowing for instant, reproducible deployments.

## 12. Recommendations

For institutions looking to adopt this framework, it is recommended to:
1. Deploy the PostgreSQL database to a managed cloud instance (e.g., AWS RDS) to ensure high availability.
2. Implement Airflow or cron jobs to trigger the `run_all.py` script automatically at the close of trading hours.
3. Integrate live financial APIs to replace the staging mock data generators for real-world trading utility.

## 13. Outcome / Conclusion

The project successfully delivered a robust, automated Fund Index Analysis suite. By replacing manual spreadsheet exports with a Python-driven ELT pipeline, the system guarantees accurate, daily updates to fund performance metrics. The implementation of a PostgreSQL data mart integrated with a custom Streamlit dashboard provides stakeholders with immediate, actionable insights into fund deviation, tracking errors, and historical trends. The final product successfully tracks mock NIFTY indices with high precision, demonstrating the viability of the architecture.

## 14. Enhancement Scope

Future iterations of this project could incorporate:
- **Machine Learning Integration:** Applying ARIMA or LSTM models to predict short-term NAV trends based on historical index momentum.
- **Automated Alerting:** Configuring SMTP integrations to email stakeholders automatically when a fund is added to the "Watch List" due to severe underperformance.
- **Multi-Currency Support:** Expanding the `dim_fund` logic to handle international ETFs requiring currency conversion rates.

## 15. Link to Code and Executable File

- **Local Repository:** `c:\MERN PROJECTS\tcs-fund-analysis`
- **Execution Command:** `python pipeline/run_all.py` (ETL) followed by `streamlit run dashboard/app.py` (Dashboard)
- *(Add GitHub URL here before final submission)*

## 16. Research Questions and Responses

**Q1: Why was PostgreSQL chosen over the initial SQLite implementation?**
*Response:* SQLite relies on file-level locks during write operations. When the data pipeline was updating historical records while the Business Intelligence dashboard was concurrently querying data, it caused database locking errors. PostgreSQL, being a true client-server RDBMS, handles high-volume concurrent reads and writes efficiently.

**Q2: How does the system calculate the Tracking Error of a fund?**
*Response:* Tracking Error is calculated by taking the standard deviation of the daily differences in returns between the mutual fund and its benchmark index over a specific period, demonstrating how closely the fund mimics the index's volatility.

## 17. References

1. McKinney, W. (2012). *Python for Data Analysis*. O'Reilly Media.
2. Kimball, R., & Ross, M. (2013). *The Data Warehouse Toolkit: The Definitive Guide to Dimensional Modeling*. Wiley.
3. Streamlit Documentation. (2026). *Streamlit library for Python*. Retrieved from streamlit.io.
4. PostgreSQL Global Development Group. (2026). *PostgreSQL 16 Documentation*.
5. National Stock Exchange of India (NSE) Documentation on Index Calculations.
