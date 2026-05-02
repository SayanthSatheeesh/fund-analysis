from pipeline.extract.nse_index import run_nse_extraction
from pipeline.extract.fund_nav import run_fund_extraction
from pipeline.clean.cleaner import clean_index_data, clean_fund_data
from pipeline.validate.quality_gate import run_quality_gate

# Milestone 2 Imports
from pipeline.transform.dim_loader import load_dim_date, load_dim_index, load_dim_fund
from pipeline.transform.fact_loader import load_fact_nav
from pipeline.transform.agg_builder import build_agg_period_returns, build_agg_monthly_trends, build_agg_rolling_returns, build_watch_list
from pipeline.validate.mart_validator import run_mart_validation

def main():
    print("Starting Fund Index Analysis Pipeline...")
    
    # --- MILESTONE 1 ---
    print("\n--- Phase 1B: NSE Index Extraction (MOCK) ---")
    run_nse_extraction()
    print("\n--- Phase 1C: Fund NAV Extraction (LIVE) ---")
    run_fund_extraction()
    print("\n--- Phase 1D: Data Cleaning & Standardization ---")
    clean_index_data()
    clean_fund_data()
    print("\n--- Phase 1E: Quality Gate ---")
    if not run_quality_gate():
        print("\nMilestone 1 FAILED Quality Gate. Aborting.")
        return

    # --- MILESTONE 2 ---
    print("\n--- Phase 2A: Dimension Tables ---")
    load_dim_date()
    load_dim_index()
    load_dim_fund()
    
    print("\n--- Phase 2B: Fact Table ---")
    load_fact_nav()
    
    print("\n--- Phase 2C: Aggregate & KPI Tables ---")
    build_agg_period_returns()
    build_agg_monthly_trends()
    build_agg_rolling_returns()
    build_watch_list()
    
    print("\n--- Phase 2D: Mart Validation ---")
    if run_mart_validation():
        print("\nMilestone 2 Complete. Data Mart is ready for Reporting.")
    else:
        print("\nMilestone 2 FAILED Mart Validation. Check reports/m2_mart_validation.md")

if __name__ == "__main__":
    main()
