# Detailed Tableau Development Guide — Fund Index Analysis
## End-to-End PostgreSQL Implementation

This guide provides a comprehensive, step-by-step walkthrough for building the professional Fund Index Analysis dashboard in Tableau using your PostgreSQL database.

---

### 1. Prerequisites & Connection Setup
Before opening Tableau, you must complete the following steps to prepare your environment:

1. **Start PostgreSQL**: Ensure your PostgreSQL database server is running locally or remotely.
2. **Run Data Migration**: Execute the data migration script to move your data from SQLite to PostgreSQL. You can do this by running the following command from the project root:
   ```bash
   python db/migrate_data.py
   ```

1. **Launch Tableau Desktop**: Open the application and look at the "Connect" pane on the left.
2. **Select Database**: Click on **PostgreSQL** under the "To a Server" section. (If you don't see it, click *More* and search for it).
3. **Authentication Dialog**:
   - **Server**: `localhost` (or your server IP)
   - **Port**: `5432`
   - **Database**: `fund_analysis`
   - **Authentication**: Choose `Username and Password`
   - **Username**: `postgres`
   - **Password**: `newpassword`
4. **Data Modeling**: 
   - Once connected, you will see a list of Views. 
   - Drag **v_trend_history**, **v_period_performance**, and **v_monthly_comparison** into the white canvas area.
   - **CRITICAL**: Do NOT join them. Keep them as separate "logical tables" (independent boxes on the canvas).
5. **Connection Type**: In the top-right corner, ensure **Live** is selected. This allows Tableau to query the database in real-time as your Python pipelines update.

---

### 2. Creating Calculated Fields (Financial Logic)
Tableau allows you to create custom formulas. We need these to calculate performance and deviation accurately.

1. In any Worksheet, go to the **Data pane** on the left.
2. Right-click anywhere in the pane and select **Create Calculated Field**.
3. Create the following 4 fields:

| Field Name | Formula | Formatting |
|---|---|---|
| **% Fund Return** | `SUM([fund_return])` | Right-click > Default Properties > Number Format > **Percentage** (2 decimals) |
| **% Index Return** | `SUM([index_return])` | Right-click > Default Properties > Number Format > **Percentage** (2 decimals) |
| **Deviation %** | `[% Fund Return] - [% Index Return]` | Right-click > Default Properties > Number Format > **Percentage** (2 decimals) |
| **Tracking Error** | `STDEV([tracking_error])` | Right-click > Default Properties > Number Format > **Number (Custom)** (4 decimals) |

---

### 3. Step-by-Step Worksheet Construction

#### **A. Page 1: Summary Performance (Trend Analysis)**
This chart shows the primary comparison between the Fund NAV and the Index Price.
1. **Columns**: Drag `full_date` to the Columns shelf. Right-click it and select **Exact Date** (the second one in the list) and then change it to **Continuous**.
2. **Rows**: Drag `nav_price` and `index_price` to the Rows shelf.
3. **Dual Axis**: Right-click the `index_price` pill in the Rows shelf and select **Dual Axis**.
4. **Synchronize**: Right-click the right-side axis (Index Price) and select **Synchronize Axis**. This ensures both lines share the same scale.
5. **Color**: Drag `Measure Names` to the **Color** mark. Set the Fund to a vibrant color (e.g., Blue) and the Index to a neutral color (e.g., Grey).
6. **Filters**: Drag `index_name` and `fund_id` to the Filters shelf. Right-click them and select **Show Filter** to make them interactive.

#### **B. Page 3: Multi-Fund Comparison (Heat Map Matrix)**
This matrix provides an "at-a-glance" view of fund performance over time.
1. **Rows**: Drag `fund_id` to the Rows shelf.
2. **Columns**: Drag `year_month` to the Columns shelf. Right-click and change it to **Discrete** if it shows as a number.
3. **Marks**: In the Marks card, change the dropdown from "Automatic" to **Square**.
4. **Coloring**: Drag `monthly_return` to the **Color** mark.
   - Click **Color > Edit Colors**.
   - Select the **Red-Green Diverging** palette.
   - Check **Use Full Color Range**.
5. **Labeling**: Drag `monthly_return` to the **Label** mark. Right-click it and set the format to **Percentage**. This shows the actual return number inside each colored box.

---

### 4. Interactive Dashboard Actions (Automation)
Actions make the dashboard feel like a custom application.

1. **Create Dashboard**: Create a new Dashboard and drag your worksheets onto it.
2. **Setup Drill-Through**:
   - Go to **Dashboard > Actions**.
   - Click **Add Action > Filter**.
   - **Source Sheets**: Select your Summary Page.
   - **Target Sheets**: Select your Fund Detail Page.
   - **Run action on**: Select **Select** (this triggers when you click a data point).
   - **Target Filters**: Select **Selected Fields** and choose `fund_id`.
3. **Result**: Now, when you click a specific fund on the Summary chart, the entire dashboard (including the detail page) will automatically filter to show data only for that fund.

---

### 5. Advanced Polish & Formatting
- **Tooltips**: Click **Tooltip** on the Marks card. Edit the text to be user-friendly:
  ```text
  Fund Identifier: <fund_id>
  Current Date: <full_date>
  NAV Price: <nav_price>
  Index Value: <index_price>
  ```
- **Modern Look**: Go to **Format > Dashboard** and set the background to a light grey. Ensure all fonts are set to a clean sans-serif like "Benton Sans" or "Arial".
- **Dynamic Title**: Click the Title and insert the `<index_name>` parameter so the title changes based on the user's selection.

---

### 6. Troubleshooting Common Issues
- **Error "Database is Locked"**: This happens if you didn't migrate to PostgreSQL. Ensure you are using the PostgreSQL connector, not SQLite.
- **Null Values**: If data isn't showing, check if your Date Filter range is too small.
- **Incorrect Returns**: Ensure you are using `SUM()` in your calculated fields, not `AVG()`, as returns are pre-calculated per day in the database.
