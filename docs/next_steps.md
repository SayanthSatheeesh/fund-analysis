# Project Roadmap — Future Enhancements
## Milestone 5 & Beyond

The current implementation provides a solid foundation. Here are the recommended next steps to scale the system.

---

### 1. Phase 5: Real-time Data Integration
- **NSE Real Data:** Replace the mock generator with a professional data provider (e.g., Zerodha Kite API, Upstox API, or Alpha Vantage).
- **Intraday Support:** Modify the pipeline to run every hour during market sessions.

### 2. Phase 6: Advanced Analytics
- **Portfolio Backtesting:** Allow users to upload their own holdings and compare against the benchmark.
- **Risk Metrics:** Implement Sortino Ratio, Sharpe Ratio, and Maximum Drawdown in the `agg_builder.py`.
- **Predictive Modeling:** Integrate a Python-based forecasting model to project future NAV trends based on historical index correlation.

### 3. Phase 7: Infrastructure Upgrades
- **PostgreSQL Migration:** Move from SQLite to a dedicated PostgreSQL server for better concurrency and partitioning.
- **Cloud Hosting:** Deploy the pipeline to AWS (Lambda + RDS) or Azure (Functions + SQL Database).
- **Web Interface:** Replace the BI Dashboard with a custom React/Next.js frontend for a tailored user experience.

### 4. Phase 8: Alerting & Notifications
- **Email Alerts:** Send an automated summary report every morning.
- **Critical Alerts:** Notify users via Telegram/Slack if a fund enters the "Watch List".
