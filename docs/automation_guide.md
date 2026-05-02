# Automation & Scheduling Guide — Fund Index Analysis
## How to automate your data updates

This document explains how to set up the system to refresh your dashboard data every morning automatically.

---

### 1. The Master Script
The system uses a single master script to run the entire pipeline:
- **Location:** `pipeline/run_all.py`
- **What it does:** Extracts fresh data, cleans it, updates the Data Mart, and validates the results.
- **Manual Run:** `$env:PYTHONPATH="."; python -m pipeline.run_all`

---

### 2. Setting up Windows Task Scheduler
To run the update daily at 8:00 AM:

1. **Open Task Scheduler:** Press `Win + R`, type `taskschd.msc`, and press Enter.
2. **Create Basic Task:**
   - **Name:** Fund Index Analysis Update
   - **Trigger:** Daily
   - **Time:** 08:00 AM
3. **Action:** Start a Program
   - **Program/script:** `python.exe` (Provide the full path, e.g., `C:\Python312\python.exe`)
   - **Add arguments:** `-m pipeline.run_all`
   - **Start in (Optional):** `C:\MERN PROJECTS\tcs-fund-analysis`
4. **Environment Variables:**
   - You must ensure `PYTHONPATH` is set to the project root.
   - Alternatively, create a `.bat` file (see below) and schedule that instead.

---

### 3. Using a Batch File (Recommended for Windows)
Create a file named `update_data.bat` in your project root with this content:

```batch
@echo off
cd /d "C:\MERN PROJECTS\tcs-fund-analysis"
set PYTHONPATH=.
python -m pipeline.run_all
pause
```

Now, simply schedule this `.bat` file in Task Scheduler.

---

### 4. Monitoring Updates
- **Logs:** Check the `logs/` directory for daily log files (e.g., `pipeline_20260427_080000.log`).
- **Quality Reports:** Check `reports/` for the latest validation results.
- **Failures:** If the script fails, the log file will contain a "CRITICAL FAILURE" message with the exact error.
