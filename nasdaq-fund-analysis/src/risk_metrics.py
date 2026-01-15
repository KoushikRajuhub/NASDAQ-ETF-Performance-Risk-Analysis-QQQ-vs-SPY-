# ----------------------------------------------------
# Step 3: Risk & Performance Metrics
# ----------------------------------------------------
# This script calculates:
# - Annualized Volatility
# - Sharpe Ratio
# - Maximum Drawdown
# - Beta and Alpha (QQQ vs SPY)
# ----------------------------------------------------

import os
import pandas as pd
import numpy as np

# ----------------------------------------------------
# Resolve project root dynamically
# ----------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PROCESSED_PATH = os.path.join(BASE_DIR, "data", "processed")
OUTPUT_PATH = os.path.join(BASE_DIR, "data", "metrics")

os.makedirs(OUTPUT_PATH, exist_ok=True)

# ----------------------------------------------------
# Load processed return data
# ----------------------------------------------------
qqq = pd.read_csv(os.path.join(PROCESSED_PATH, "qqq_returns.csv"))
spy = pd.read_csv(os.path.join(PROCESSED_PATH, "spy_returns.csv"))

# Convert Date to datetime
qqq["Date"] = pd.to_datetime(qqq["Date"])
spy["Date"] = pd.to_datetime(spy["Date"])

# Align datasets by date
data = pd.merge(
    qqq[["Date", "Daily_Return"]],
    spy[["Date", "Daily_Return"]],
    on="Date",
    how="inner",
    suffixes=("_QQQ", "_SPY")
)

# Drop first row (NaN returns)
data = data.dropna()

# ----------------------------------------------------
# Risk-free rate assumption (annual)
# ----------------------------------------------------
RISK_FREE_RATE = 0.04  # 4%

TRADING_DAYS = 252

# ----------------------------------------------------
# Volatility (Annualized)
# ----------------------------------------------------
volatility_qqq = data["Daily_Return_QQQ"].std() * np.sqrt(TRADING_DAYS)
volatility_spy = data["Daily_Return_SPY"].std() * np.sqrt(TRADING_DAYS)

# ----------------------------------------------------
# Sharpe Ratio
# ----------------------------------------------------
sharpe_qqq = (
    (data["Daily_Return_QQQ"].mean() * TRADING_DAYS - RISK_FREE_RATE)
    / volatility_qqq
)

sharpe_spy = (
    (data["Daily_Return_SPY"].mean() * TRADING_DAYS - RISK_FREE_RATE)
    / volatility_spy
)

# ----------------------------------------------------
# Maximum Drawdown
# ----------------------------------------------------
def max_drawdown(returns):
    cumulative = (1 + returns).cumprod()
    peak = cumulative.cummax()
    drawdown = (cumulative - peak) / peak
    return drawdown.min()

max_dd_qqq = max_drawdown(data["Daily_Return_QQQ"])
max_dd_spy = max_drawdown(data["Daily_Return_SPY"])

# ----------------------------------------------------
# Beta & Alpha (CAPM)
# ----------------------------------------------------
covariance = np.cov(
    data["Daily_Return_QQQ"],
    data["Daily_Return_SPY"]
)[0][1]

market_variance = data["Daily_Return_SPY"].var()

beta_qqq = covariance / market_variance

annual_return_qqq = data["Daily_Return_QQQ"].mean() * TRADING_DAYS
annual_return_spy = data["Daily_Return_SPY"].mean() * TRADING_DAYS

alpha_qqq = annual_return_qqq - (
    RISK_FREE_RATE + beta_qqq * (annual_return_spy - RISK_FREE_RATE)
)

# ----------------------------------------------------
# Save metrics
# ----------------------------------------------------
metrics = pd.DataFrame({
    "Metric": [
        "Annualized Volatility",
        "Sharpe Ratio",
        "Maximum Drawdown",
        "Beta (vs SPY)",
        "Alpha"
    ],
    "QQQ": [
        volatility_qqq,
        sharpe_qqq,
        max_dd_qqq,
        beta_qqq,
        alpha_qqq
    ],
    "SPY": [
        volatility_spy,
        sharpe_spy,
        max_dd_spy,
        1.0,
        0.0
    ]
})

metrics.to_csv(os.path.join(OUTPUT_PATH, "risk_metrics.csv"), index=False)

# ----------------------------------------------------
# Console output
# ----------------------------------------------------
print("Step 3: Risk & Performance Metrics completed successfully.")
print(metrics)
print("Metrics saved in: data/metrics/risk_metrics.csv")
