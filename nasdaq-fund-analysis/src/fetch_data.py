# ----------------------------------------------------
# Step 1: Data Collection
# Objective:
# - Fetch historical price data for:
#   1. NASDAQ fund (QQQ)
#   2. Benchmark ETF (SPY)
# - Save raw data as CSV for further processing
# ----------------------------------------------------

# ------------------------
# Import required libraries
# ------------------------
import os                      # For directory creation and file handling
import yfinance as yf           # For fetching financial market data
import pandas as pd             # For data manipulation
from datetime import datetime   # For dynamic date handling

# ------------------------
# Configuration section
# ------------------------

# NASDAQ fund ticker
FUND_TICKER = "QQQ"

# Benchmark ticker (S&P 500 ETF)
BENCHMARK_TICKER = "SPY"

# Historical data start date
START_DATE = "2015-01-01"

# End date set to today's date
END_DATE = datetime.today().strftime("%Y-%m-%d")

# Directory to store raw data
RAW_DATA_PATH = "data/raw"

# ------------------------
# Create required directories
# ------------------------
os.makedirs(RAW_DATA_PATH, exist_ok=True)

# ------------------------
# Function to download price data
# ------------------------
def download_price_data(ticker, start, end):
    """
    Downloads historical OHLCV price data for a given ticker
    and returns a clean pandas DataFrame.
    """
    df = yf.download(
        tickers=ticker,     # yfinance requires 'tickers' (plural)
        start=start,
        end=end,
        progress=False,
        auto_adjust=False
    )

    # Convert Date index into a column
    df.reset_index(inplace=True)

    return df

# ------------------------
# Fetch data
# ------------------------
qqq_data = download_price_data(FUND_TICKER, START_DATE, END_DATE)
spy_data = download_price_data(BENCHMARK_TICKER, START_DATE, END_DATE)

# ------------------------
# Handle MultiIndex columns (yfinance behavior)
# ------------------------
# Sometimes yfinance returns columns like ('Open', 'QQQ')
# We flatten them to standard column names

if isinstance(qqq_data.columns, pd.MultiIndex):
    qqq_data.columns = qqq_data.columns.get_level_values(0)

if isinstance(spy_data.columns, pd.MultiIndex):
    spy_data.columns = spy_data.columns.get_level_values(0)

# ------------------------
# Data validation
# ------------------------
required_columns = {
    "Date",
    "Open",
    "High",
    "Low",
    "Close",
    "Adj Close",
    "Volume"
}

missing_qqq = required_columns - set(qqq_data.columns)
missing_spy = required_columns - set(spy_data.columns)

if missing_qqq:
    raise ValueError(f"QQQ missing columns: {missing_qqq}")

if missing_spy:
    raise ValueError(f"SPY missing columns: {missing_spy}")

# ------------------------
# Save raw data to CSV
# ------------------------
qqq_data.to_csv(os.path.join(RAW_DATA_PATH, "qqq_prices.csv"), index=False)
spy_data.to_csv(os.path.join(RAW_DATA_PATH, "spy_prices.csv"), index=False)

# ------------------------
# Console confirmation
# ------------------------
print("Step 1: Data Collection completed successfully.")
print(f"QQQ records fetched: {len(qqq_data)}")
print(f"SPY records fetched: {len(spy_data)}")
print("Files saved in: data/raw/")
