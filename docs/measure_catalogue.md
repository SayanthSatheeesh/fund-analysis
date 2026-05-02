# Measure Catalogue — Fund Index Analysis
## Version: 1.0

This document defines the semantic measures to be implemented in Streamlit or Plotly.

---

### 1. Core Performance Measures

| Measure Name | Logic / Formula | Description |
|---|---|---|
| **% Fund Return** | `(SUM(v_period_performance[fund_return]))` | Returns the percentage growth of the fund for the selected period. |
| **% Index Return** | `(SUM(v_period_performance[index_return]))` | Returns the percentage growth of the benchmark index. |
| **Deviation (%)** | `[% Fund Return] - [% Index Return]` | Calculates the alpha (outperformance/underperformance) against the benchmark. |
| **Tracking Error** | `STDEV.P(v_trend_history[tracking_error])` | Measures the volatility of the deviation from the index. |

---

### 2. Formatting Rules

- **Return Percentages:** Display as Percentage with 2 decimal places.
- **NAV / Index Price:** Display as Decimal with 2 decimal places, use thousand separators.
- **Conditional Formatting:** 
  - `Deviation (%) > 0`: Green Text / Icon
  - `Deviation (%) < 0`: Red Text / Icon

---

### 3. Slicer Mappings

| Slicer Name | Column | Table |
|---|---|---|
| Date Range | `full_date` | `v_trend_history` |
| Index Category | `index_name` | `v_trend_history` |
| Fund Category | `fund_category` | `v_period_performance` |
| Period Selector | `period` | `v_period_performance` |

---

### 4. Watch List Logic

- Use the `is_watch_listed` column from `v_period_performance`.
- Visual: "Watch List" status card or icon on the Fund Detail page.
