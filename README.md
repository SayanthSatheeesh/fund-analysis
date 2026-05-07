# Fund Index Analysis Dashboard 📊

A professional, production-ready Streamlit application for analyzing mutual fund performance against benchmark indices.

## Features
- **Summary Trend Analysis**: Interactive Plotly charts comparing NAV vs. Benchmark.
- **Period Performance**: Comprehensive breakdown of returns across 1M, 3M, 6M, 1Y, and YTD.
- **Heatmap Visualization**: Matrix view of monthly returns for quick pattern recognition.
- **Premium UI**: Custom CSS with glassmorphism effects, dark mode, and responsive layout.

## Setup Instructions

### 1. Prerequisites
- Python 3.11+
- PostgreSQL (Optional, fallback to sample data available)

### 2. Local Installation
```bash
# Clone the repository
git clone <your-repo-url>
cd tcs-fund-analysis

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

### 3. Database Configuration
To connect to a live PostgreSQL database, create a `.streamlit/secrets.toml` file:
```toml
[postgres]
host = "localhost"
port = 5432
dbname = "fund_analysis"
user = "postgres"
password = "yourpassword"
```

## Deployment
This app is ready for deployment on **Streamlit Community Cloud**, **Render**, or **Railway**.
- **Procfile** included for Render/Heroku.
- **runtime.txt** included for Python version specification.
- **requirements.txt** included for automated environment setup.

---
*Developed for professional financial analysis.*
