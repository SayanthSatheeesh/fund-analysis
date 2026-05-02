# BI Development Guide — Power BI (Beginner Edition)
## Complete Step-by-Step Instructions

This guide is written for a complete beginner. Follow these exact steps to build your Power BI dashboard from scratch using your PostgreSQL database.

---

### Phase 1: Connect Power BI to Your Database

1. **Open Power BI Desktop** on your computer. If a "Welcome" pop-up appears, close it by clicking the "X" in the top right corner.
2. Look at the top ribbon menu (Home tab) and click the **Get Data** button (it has an icon of a database cylinder).
3. A menu will drop down. Click **More...** at the very bottom.
4. In the new window, type `PostgreSQL` in the search box on the left.
5. Click on **PostgreSQL database** in the list, then click the yellow **Connect** button.
6. A connection window will pop up:
   - **Server:** Type `localhost`
   - **Database:** Type `fund_analysis`
   - **Data Connectivity mode:** Leave it as "Import"
   - Click **OK**.
7. *Note: If it asks for credentials, click on the "Database" tab on the left, enter your PostgreSQL username (usually `postgres`) and your password, then click Connect.*
8. The "Navigator" window will open, showing a list of tables. Check the boxes next to these three views:
   - `v_trend_history`
   - `v_period_performance`
   - `v_monthly_comparison`
9. Click the yellow **Load** button at the bottom. Wait a few moments while Power BI imports your data. You will see the tables appear on the far right side of your screen in the **"Data" pane**.

---

### Phase 2: Create the Required Math (Measures)

We need to tell Power BI how to calculate returns and deviations.

1. Go to the **Data pane** on the far right.
2. **Right-click** on the table named `v_period_performance` and select **New Measure**.
3. A formula bar will appear at the top of the screen (similar to Excel).
4. Copy and paste the following text exactly into the formula bar, then press **Enter**:
   ```dax
   % Fund Return = SUM(v_period_performance[fund_return])
   ```
5. **Right-click** `v_period_performance` again, select **New Measure**, paste this, and press **Enter**:
   ```dax
   % Index Return = SUM(v_period_performance[index_return])
   ```
6. **Right-click** `v_period_performance` one more time, select **New Measure**, paste this, and press **Enter**:
   ```dax
   Deviation (%) = [% Fund Return] - [% Index Return]
   ```

---

### Phase 3: Build Page 1 — Market Summary

1. Look at the bottom left of your screen. You will see "Page 1". Right-click it and select **Rename**. Name it `Market Summary`.

**Add a Date Filter (Slicer):**
2. In the **Visualizations pane** (middle right), click the **Slicer** icon (it looks like a small table with a funnel next to it). A blank square will appear on your canvas.
3. In the **Data pane** (far right), click the little arrow next to `v_trend_history` to expand it.
4. Drag the `full_date` field and drop it directly inside that blank square on your canvas. It will turn into a date slider.

**Add an Index Filter (Slicer):**
5. Click anywhere on the blank white canvas so nothing is selected.
6. Click the **Slicer** icon again.
7. From `v_trend_history`, drag `index_name` into the new blank square.

**Add KPI Cards (The big numbers):**
8. Click on the blank canvas.
9. In the Visualizations pane, click the **Card** visual (it has a "123" icon).
10. Drag `nav_price` from `v_trend_history` into the card. It might say "Sum of nav_price". In the Visualizations pane, under the "Fields" bucket, right-click `nav_price`, and change it to **Average**.
11. Repeat steps 8-10 to create a second Card, but use `index_price` instead.
12. Repeat steps 8-9 to create a third Card, and drag your new measure `Deviation (%)` (from `v_period_performance`) into it.

**Add the Dual-Axis Trend Chart:**
13. Click on the blank canvas.
14. In the Visualizations pane, click the **Line Chart** icon. Resize the blank box to make it large.
15. Drag `full_date` from `v_trend_history` into the **X-axis** bucket (in the Visualizations pane).
16. Drag `nav_price` into the **Y-axis** bucket. Right-click it and change it to **Average**.
17. Drag `index_price` into the **Secondary Y-axis** bucket. Right-click it and change it to **Average**.

---

### Phase 4: Build Page 2 — Fund Detail

1. Look at the bottom of the screen and click the **green "+" button** next to "Market Summary" to create a new page. Rename it `Fund Detail`.

**Set up Drill-through:**
2. Make sure you are clicking on the blank canvas of the Fund Detail page.
3. In the Visualizations pane, look for the section at the bottom called **"Drill-through"**.
4. Drag `fund_id` from `v_period_performance` into the box that says "Add drill-through fields here". This allows you to right-click a fund on Page 1 and jump to this page.

**Add the Bar Chart:**
5. Click on the blank canvas. Click the **Clustered Column Chart** icon (vertical bars).
6. Drag `period` from `v_period_performance` into the **X-axis**.
7. Drag `% Fund Return` into the **Y-axis**.
8. Drag `% Index Return` into the **Y-axis** (right below Fund Return).

---

### Phase 5: Build Page 3 — Multi-Fund Comparison

1. Click the **green "+" button** to create a third page. Rename it `Comparison`.

**Add the Matrix:**
2. Click the **Matrix** visual icon (it looks like an Excel pivot table with blue borders).
3. Expand `v_monthly_comparison` in the Data pane.
4. Drag `fund_id` into the **Rows** bucket.
5. Drag `year_month` into the **Columns** bucket.
6. Drag `monthly_return` into the **Values** bucket.

**Add Conditional Formatting (Colors):**
7. Look at the **Values** bucket where you just dropped `monthly_return`. Click the small down arrow next to it.
8. Select **Conditional formatting** -> **Background color**.
9. In the window that pops up, change "Format style" to **Rules**.
10. Create Rule 1: If value is greater than or equal to 0, choose a **Green** color.
11. Click "New rule". Rule 2: If value is less than 0, choose a **Red** color.
12. Click **OK**.

---

### Phase 6: Final Polish & Saving

1. **Make it look Premium:** Go to the **View** tab at the top of Power BI. Click the drop-down arrow in the **Themes** box and select one of the dark themes (like "Innovate" or "Executive").
2. **Save your work:** Go to **File** -> **Save As**, and save it as `tcs_fund_dashboard.pbix` in your `c:\MERN PROJECTS\tcs-fund-analysis\reports\` folder.

You are completely done! You have built a professional Power BI dashboard.
