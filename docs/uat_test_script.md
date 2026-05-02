# UAT Test Script — Fund Index Analysis Dashboard
## Version: 1.0

Follow these scenarios to verify the dashboard functionality before Milestone 4 (Deployment).

---

### Scenario 1: Data Filtering (Summary Page)
- **Action:** Select 'NIFTY 50' in the Index Category slicer.
- **Expected Result:** The Trend Chart and KPI cards update to show data only for NIFTY 50.
- **Verification:** The "Index Price" card should match the latest price in `stg_index_clean`.

### Scenario 2: Drill-down Capability
- **Action:** Right-click a data point in the Trend Chart and select "Drill Down".
- **Expected Result:** The axis changes from Year to Quarter/Month.
- **Verification:** The chart displays finer granularity without data loss.

### Scenario 3: Period Return Accuracy (Fund Detail Page)
- **Action:** Select a fund and view the "Period Return" bar chart.
- **Expected Result:** Returns for 1M, 1Y, and Inception are displayed.
- **Verification:** Compare values against the `agg_period_returns` table in the database.

### Scenario 4: Watch List Flagging
- **Action:** Locate a fund that has underperformed in 2+ periods.
- **Expected Result:** The "Watch List" card displays "YES" in red.
- **Verification:** Check `watch_list` table for the corresponding `fund_sk`.

### Scenario 5: Multi-Fund Comparison Matrix
- **Action:** Navigate to Page 3 and sort by `fund_id`.
- **Expected Result:** The matrix shows a monthly return heat map.
- **Verification:** Conditional formatting shows Green for positive and Red for negative months.
