# Fund Index Analysis System

An automated ELT (Extract, Load, Transform) pipeline and Business Intelligence suite for tracking mutual fund performance against market benchmarks.

## 📊 Overview
This system automates the daily ingestion of mutual fund NAV data and market index prices (NIFTY 50, etc.), processes them into a PostgreSQL Star Schema, and serves insights via an interactive Streamlit dashboard and Power BI reports.

### Key Features
- **Automated ELT Pipeline**: Incremental loading with watermark tracking.
- **Data Quality Gates**: Automated validation of incoming data before mart loading.
- **Star Schema Data Mart**: Optimized PostgreSQL schema for analytical queries.
- **Financial Metrics**: Calculation of rolling returns, tracking error, and Alpha.
- **Interactive Dashboards**: Real-time visualization using Streamlit and Plotly.
- **Power BI Integration**: Pre-defined views for professional reporting.

## 🛠️ Tech Stack
- **Language**: Python 3.x
- **Data Processing**: Pandas, NumPy
- **Database**: PostgreSQL, SQLAlchemy
- **Visualization**: Streamlit, Plotly, Power BI
- **Environment**: Dotenv, VS Code

## 📁 Project Structure
- `pipeline/`: Core ELT logic (Extract, Clean, Transform, Validate).
- `db/`: Database connection and migration scripts.
- `dashboard/`: Streamlit application code.
- `docs/`: Technical documentation and BI development guides.
- `reports/`: Generated quality and validation reports.

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.x
- PostgreSQL installed and running.
- Power BI Desktop (optional, for .pbix reports).

### 2. Installation
```bash
# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration
Copy `.env.example` to `.env` and configure your PostgreSQL credentials:
```bash
DB_USER=your_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=fund_analysis
```

### 4. Running the Pipeline
```bash
# Execute the full ELT cycle
python pipeline/run_all.py
```

### 5. Launching the Dashboard
```bash
# Start the Streamlit app
streamlit run dashboard/app.py
```

## 📜 Documentation
- [BI Development Guide](docs/bi_dev_guide.md)
- [Measure Catalogue](docs/measure_catalogue.md)
- [Progress Tracker](progress.md)

## 👤 Author
**Sayanth Satheesh**  
Lead College (Autonomous)

---
*Note: This project uses mock data generators for NSE indices and fund ratings to demonstrate functionality without requiring proprietary API keys.*
