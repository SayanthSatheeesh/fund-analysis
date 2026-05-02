import pandas as pd
from db.connection import get_engine
import json
from datetime import datetime
import os
from sqlalchemy import text

def run_mart_validation():
    print("Running Milestone 2 Mart Validation...")
    engine = get_engine()
    
    results = {
        "timestamp": datetime.now().isoformat(),
        "milestone": "M2",
        "checks": [],
        "status": "FAIL"
    }
    
    # 1. Referential Integrity (FK check)
    with engine.connect() as conn:
        try:
            # Check for fund_sk orphans
            orphans_fund = pd.read_sql(text("""
                SELECT COUNT(*) as count FROM fact_nav_history 
                WHERE fund_sk NOT IN (SELECT fund_sk FROM dim_fund)
            """), conn).iloc[0]['count']
            
            # Check for index_sk orphans
            orphans_index = pd.read_sql(text("""
                SELECT COUNT(*) as count FROM fact_nav_history 
                WHERE index_sk NOT IN (SELECT index_sk FROM dim_index)
            """), conn).iloc[0]['count']
            
            # Check for date_id orphans
            orphans_date = pd.read_sql(text("""
                SELECT COUNT(*) as count FROM fact_nav_history 
                WHERE date_id NOT IN (SELECT date_id FROM dim_date)
            """), conn).iloc[0]['count']
            
            results["checks"].append({
                "check": "Referential Integrity",
                "details": f"Orphaned: Fund={orphans_fund}, Index={orphans_index}, Date={orphans_date}",
                "status": "PASS" if (orphans_fund == 0 and orphans_index == 0 and orphans_date == 0) else "FAIL"
            })
        except Exception as e:
            print(f"Error checking RI: {e}")
            results["checks"].append({"check": "Referential Integrity", "status": "FAIL", "details": str(e)})

    # 2. Fact Table Null Check
    try:
        df_fact = pd.read_sql("SELECT * FROM fact_nav_history", engine)
        critical_cols = ['fund_sk', 'index_sk', 'date_id', 'nav_price', 'index_price']
        null_count = df_fact[critical_cols].isnull().sum().sum()
        results["checks"].append({
            "check": "Fact Table Nulls",
            "details": f"Found {null_count} nulls in critical columns",
            "status": "PASS" if null_count == 0 else "FAIL"
        })
    except Exception as e:
        results["checks"].append({"check": "Fact Table Nulls", "status": "FAIL", "details": str(e)})
    
    # 3. Aggregate Coverage Check
    try:
        df_agg = pd.read_sql("SELECT COUNT(DISTINCT fund_sk) as count FROM agg_period_returns", engine)
        distinct_funds_in_agg = df_agg.iloc[0]['count']
        df_dim = pd.read_sql("SELECT COUNT(*) as count FROM dim_fund WHERE is_current = TRUE", engine)
        total_funds = df_dim.iloc[0]['count']
        
        results["checks"].append({
            "check": "Aggregate Coverage",
            "details": f"Covered {distinct_funds_in_agg} of {total_funds} funds",
            "status": "PASS" if distinct_funds_in_agg == total_funds else "FAIL"
        })
    except Exception as e:
        results["checks"].append({"check": "Aggregate Coverage", "status": "FAIL", "details": str(e)})

    # Final Status
    if all(c["status"] == "PASS" for c in results["checks"]):
        results["status"] = "PASS"
    
    # Save Reports
    os.makedirs("reports", exist_ok=True)
    report_path = "reports/m2_mart_validation.md"
    with open(report_path, "w") as f:
        f.write(f"# Milestone 2 Mart Validation Report\n\n")
        f.write(f"- **Status:** {results['status']}\n")
        f.write(f"- **Timestamp:** {results['timestamp']}\n\n")
        f.write(f"## Validation Checks\n\n")
        f.write(f"| Check | Status | Details |\n")
        f.write(f"|---|---|---|\n")
        for check in results["checks"]:
            f.write(f"| {check['check']} | {check['status']} | {check['details']} |\n")
    
    print(f"Mart Validation {results['status']}!")
    print(f"Report saved to {report_path}")
    
    return results["status"] == "PASS"

if __name__ == "__main__":
    run_mart_validation()
