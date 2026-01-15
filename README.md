# NASDAQ ETF Performance & Risk Analysis (QQQ vs SPY)

## Project Overview

This project delivers an **end-to-end financial data analytics solution** comparing the performance and risk characteristics of two major ETFs:

- **QQQ** – NASDAQ-100 ETF (growth-oriented)
- **SPY** – S&P 500 ETF (market benchmark)

The workflow combines **Python for data processing and metric computation** with **Power BI for interactive dashboards and business intelligence reporting**.  
The project is designed to reflect **industry-standard analytical practices** suitable for data analyst and BI roles.

---

## Objectives

- Compare long-term performance using CAGR and cumulative returns  
- Analyze volatility, drawdowns, and risk-adjusted returns  
- Evaluate consistency of performance across market cycles  
- Build professional Power BI dashboards for decision-making  

---


## Tools & Technologies

- **Python**
  - pandas, numpy
  - yfinance (historical market data)
- **Power BI**
  - Data modeling (star schema)
  - DAX measures
  - Interactive dashboards
- **GitHub**
  - Version control
  - Documentation and reporting

---

## Repository Structure
```
nasdaq-fund-analysis/
│
├── data/
│ ├── raw/
│ │ ├── qqq_prices.csv
│ │ └── spy_prices.csv
│ └── processed/
│ ├── qqq_returns.csv
│ ├── spy_returns.csv
│ └── risk_metrics.csv
│
├── src/
│ ├── fetch_data.py
│ ├── clean_and_returns.py
│ └── risk_metrics.py
│
├── powerbi/
│ └── nasdaq_fund_analysis.pbix
│
├── report/
│ └── NASDAQ_ETF_Analysis_Report.pdf
│
├── requirements.txt
└── README.md
```


---

## Power BI Dashboards

### 1. Executive Overview
- CAGR comparison (QQQ vs SPY)
- Cumulative return trend
- Interactive year slicer

### 2. Risk Analysis
- Annualized volatility comparison
- Sharpe ratio (risk-adjusted return)
- Maximum drawdown (downside risk)
- Consolidated risk metrics table

### 3. Performance Breakdown
- Rolling 12-month returns
- Daily return distribution (histogram)
- Best vs worst monthly returns

---

## Key Insights

- QQQ delivers **higher long-term returns** than SPY  
- Higher returns come with **higher volatility and deeper drawdowns**  
- QQQ shows **stronger risk-adjusted performance**  
- SPY offers **greater stability and lower downside risk**

---


