# ----------------------------------------------------
# Step 2: Data Cleaning & Return Calculation
# ----------------------------------------------------
# This script:
# 1. Loads raw price data for QQQ and SPY
# 2. Cleans and standardizes the data
# 3. Calculates daily, log, and cumulative returns
# 4. Saves processed datasets for Power BI
# ----------------------------------------------------

import os
import pandas as pd
import numpy as np

# ----------------------------------------------------
# Resolve project root dynamically (robust path handling)
# ----------------------------------------------------
# __file__  -> src/clean_and_returns.py
# dirname() -> src
# dirname() -> project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RAW_PATH = os.path.join(BASE_DIR, "data", "raw")
PROCESSED_PATH = os.path.join(BASE_DIR, "data", "processed")

# Create processed folder if it doesn't exist
os.makedirs(PROCESSED_PATH, exist_ok=True)

# ----------------------------------------------------
# Load raw data
# ----------------------------------------------------
qqq = pd.read_csv(os.path.join(RAW_PATH, "qqq_prices.csv"))
spy = pd.read_csv(os.path.join(RAW_PATH, "spy_prices.csv"))

# ----------------------------------------------------
# Data cleaning function
# ----------------------------------------------------
def clean_price_data(df):
    """
    Cleans raw OHLCV price data.
    """
    # Convert Date column to datetime
    df["Date"] = pd.to_datetime(df["Date"])

    # Sort by date
    df = df.sort_values("Date")

    # Remove duplicate dates
    df = df.drop_duplicates(subset="Date")

    # Forward-fill missing values (finance standard)
    df = df.ffill()

    return df

qqq = clean_price_data(qqq)
spy = clean_price_data(spy)

# ----------------------------------------------------
# Return calculations
# ----------------------------------------------------
def calculate_returns(df):
    """
    Calculates financial return metrics.
    """
    df["Daily_Return"] = df["Adj Close"].pct_change()
    df["Log_Return"] = np.log(df["Adj Close"] / df["Adj Close"].shift(1))
    df["Cumulative_Return"] = (1 + df["Daily_Return"]).cumprod() - 1
    return df

qqq = calculate_returns(qqq)
spy = calculate_returns(spy)

# ----------------------------------------------------
# Save processed data
# ----------------------------------------------------
qqq.to_csv(os.path.join(PROCESSED_PATH, "qqq_returns.csv"), index=False)
spy.to_csv(os.path.join(PROCESSED_PATH, "spy_returns.csv"), index=False)

# ----------------------------------------------------
# Console output
# ----------------------------------------------------
print("Step 2: Data Cleaning & Return Calculation completed successfully.")
print(f"QQQ processed rows: {len(qqq)}")
print(f"SPY processed rows: {len(spy)}")
print("Files saved in: data/processed/")
