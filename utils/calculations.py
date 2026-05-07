import numpy as np
import pandas as pd

def active_return(fund_return, index_return):
    """Calculates the deviation between fund and index returns."""
    return fund_return - index_return

def tracking_error(fund_returns, index_returns):
    """Calculates the standard deviation of the return differences."""
    differences = fund_returns - index_returns
    return np.std(differences)

def calculate_period_performance(df):
    """Aggregates returns for different periods (1M, 3M, 6M, 1Y, YTD)."""
    # Simplified logic for demo purposes
    periods = ['1M', '3M', '6M', '1Y', 'YTD']
    results = []
    for period in periods:
        # Mocking logic: in a real app, this would slice the dataframe by date
        fund_ret = np.random.uniform(-0.05, 0.15)
        index_ret = np.random.uniform(-0.03, 0.12)
        results.append({
            'Period': period,
            'Fund Return': fund_ret,
            'Index Return': index_ret,
            'Deviation': active_return(fund_ret, index_ret)
        })
    return pd.DataFrame(results)
