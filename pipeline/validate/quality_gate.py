import pandas as pd
from db.connection import get_engine
import json
from datetime import datetime
import os

def run_quality_gate():
    print("Running Milestone 1 Quality Gate...")
    engine = get_engine()
    
    results = {
        "timestamp": datetime.now().isoformat(),
        "milestone": "M1",
        "checks": [],
        "overall_score": 0,
        "status": "FAIL"
    }
    
    # 1. Index Data Checks
    try:
        df_index = pd.read_sql("SELECT * FROM stg_index_clean", engine)
        index_total = len(df_index)
        index_nulls = df_index[['index_name', 'index_date', 'close_price']].isnull().sum().sum()
        index_dups = df_index.duplicated(subset=['index_name', 'index_date']).sum()
        
        index_score = 100 * (1 - (index_nulls + index_dups) / max(index_total, 1))
        
        results["checks"].append({
            "entity": "stg_index_clean",
            "total_records": index_total,
            "null_count": int(index_nulls),
            "duplicate_count": int(index_dups),
            "score": round(index_score, 2)
        })
    except Exception as e:
        print(f"Error checking index data: {e}")
        index_score = 0

    # 2. Fund Data Checks
    try:
        df_fund = pd.read_sql("SELECT * FROM stg_fund_clean", engine)
        fund_total = len(df_fund)
        fund_nulls = df_fund[['fund_id', 'nav_price', 'nav_date']].isnull().sum().sum()
        fund_dups = df_fund.duplicated(subset=['fund_id', 'nav_date']).sum()
        
        fund_score = 100 * (1 - (fund_nulls + fund_dups) / max(fund_total, 1))
        
        results["checks"].append({
            "entity": "stg_fund_clean",
            "total_records": fund_total,
            "null_count": int(fund_nulls),
            "duplicate_count": int(fund_dups),
            "score": round(fund_score, 2)
        })
    except Exception as e:
        print(f"Error checking fund data: {e}")
        fund_score = 0
    
    # Calculate Overall Score
    results["overall_score"] = round((index_score + fund_score) / 2, 2)
    
    if results["overall_score"] >= 95:
        results["status"] = "PASS"
    
    # Ensure reports directory exists
    os.makedirs("reports", exist_ok=True)
    
    # Save Report
    report_path = "reports/m1_quality_report.json"
    with open(report_path, "w") as f:
        json.dump(results, f, indent=4)
    
    # Generate Markdown summary for easy viewing
    md_report_path = "reports/m1_quality_report.md"
    with open(md_report_path, "w") as f:
        f.write(f"# Milestone 1 Quality Gate Report\n\n")
        f.write(f"- **Status:** {results['status']}\n")
        f.write(f"- **Overall Score:** {results['overall_score']}%\n")
        f.write(f"- **Timestamp:** {results['timestamp']}\n\n")
        f.write(f"## Entity Breakdown\n\n")
        f.write(f"| Entity | Records | Nulls | Dups | Score |\n")
        f.write(f"|---|---|---|---|---|\n")
        for check in results["checks"]:
            f.write(f"| {check['entity']} | {check['total_records']} | {check['null_count']} | {check['duplicate_count']} | {check['score']}% |\n")
    
    print(f"Quality Gate {results['status']}! Score: {results['overall_score']}%")
    print(f"Reports saved to reports/")
    
    return results["status"] == "PASS"

if __name__ == "__main__":
    run_quality_gate()
