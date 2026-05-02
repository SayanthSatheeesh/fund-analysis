import sys
import os
import logging
from datetime import datetime
from sqlalchemy import text
from db.connection import get_engine

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import all modules
from pipeline.extract.nse_index import run_nse_extraction
from pipeline.extract.fund_nav import run_fund_extraction
from pipeline.clean.cleaner import clean_index_data, clean_fund_data
from pipeline.validate.quality_gate import run_quality_gate
from pipeline.transform.dim_loader import load_dim_date, load_dim_index, load_dim_fund
from pipeline.transform.fact_loader import load_fact_nav
from pipeline.transform.agg_builder import build_agg_period_returns, build_agg_monthly_trends, build_agg_rolling_returns, build_watch_list
from pipeline.validate.mart_validator import run_mart_validation

# Setup logging
os.makedirs("logs", exist_ok=True)
log_file = f"logs/pipeline_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stdout)
    ]
)

def run_end_to_end():
    logging.info("==========================================")
    logging.info("Starting End-to-End Fund Analysis Pipeline")
    logging.info("==========================================")
    start_time = datetime.now()
    
    try:
        # Phase 1: Extraction
        logging.info("STEP 1: Data Extraction (Index & Funds)")
        run_nse_extraction()
        run_fund_extraction()
        
        # Phase 2: Cleaning
        logging.info("STEP 2: Data Cleaning & Standardization")
        clean_index_data()
        clean_fund_data()
        
        # Phase 3: Quality Gate
        logging.info("STEP 3: Running Milestone 1 Quality Gate")
        if not run_quality_gate():
            logging.error("Quality Gate Failed! Data does not meet threshold (95%).")
            return False
            
        # Phase 4: Transformation (Dimensions)
        logging.info("STEP 4: Loading Dimension Tables")
        load_dim_date()
        load_dim_index()
        load_dim_fund()
        
        # Phase 5: Transformation (Fact)
        logging.info("STEP 5: Loading Fact Table")
        load_fact_nav()
        
        # Phase 6: Aggregation
        logging.info("STEP 6: Building Aggregate & KPI Tables")
        build_agg_period_returns()
        build_agg_monthly_trends()
        build_agg_rolling_returns()
        build_watch_list()
        
        # Phase 7: Validation
        logging.info("STEP 7: Running Milestone 2 Mart Validation")
        if not run_mart_validation():
            logging.warning("Mart Validation Failed! Check reports for details.")
            # We continue even if validation fails, but log it
            
        # Phase 8: Optimization
        logging.info("STEP 8: Database Optimization (VACUUM)")
        engine = get_engine()
        with engine.connect() as conn:
            # SQLite VACUUM cannot be run within a transaction
            # We set execution_options to isolation_level='AUTOCOMMIT'
            conn.execution_options(isolation_level="AUTOCOMMIT").execute(text("VACUUM"))
            logging.info("SQLite VACUUM complete.")
            
        duration = datetime.now() - start_time
        logging.info("==========================================")
        logging.info(f"Pipeline completed successfully in {duration}")
        logging.info("==========================================")
        return True
        
    except Exception as e:
        logging.exception("Pipeline CRITICAL FAILURE")
        return False

if __name__ == "__main__":
    success = run_end_to_end()
    if not success:
        sys.exit(1)
