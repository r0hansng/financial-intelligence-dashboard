# Financial Intelligence Dashboard

<div align="center">

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg?style=flat-square)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg?style=flat-square)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/psf/black)
[![Pandas](https://img.shields.io/badge/pandas-2.3.3-purple.svg?style=flat-square)](https://pandas.pydata.org/)
[![NumPy](https://img.shields.io/badge/numpy-2.0.2-blue.svg?style=flat-square)](https://numpy.org/)
[![SciPy](https://img.shields.io/badge/scipy-1.13.1-orange.svg?style=flat-square)](https://scipy.org/)

A comprehensive quantitative finance platform for portfolio analysis, risk assessment, and market intelligence.

[Features](#features) • [Installation](#installation) • [Quick Start](#quick-start) • [Architecture](#architecture) • [Contributing](#contributing)

</div>

---

## Overview

The **Financial Intelligence Dashboard** is an end-to-end data pipeline for quantitative analysis and portfolio optimization. It combines real-time market data ingestion, feature engineering, advanced statistical modeling, and interactive visualizations to deliver actionable financial insights.

**Built for:** Portfolio managers, quantitative analysts, risk officers, and financial data scientists.

---

## Features

### Market Data Management
- **Automated Data Ingestion**: Fetch live market data for multiple tickers (AAPL, MSFT, GOOGL, ^GSPC)
- **Data Validation Pipeline**: Multi-layer validation to ensure data integrity
- **Parquet Storage**: Efficient columnar storage format for fast analytics

### Quantitative Analysis
- **Risk Metrics Calculation**
  - Sharpe Ratio (risk-adjusted returns)
  - Maximum Drawdown (downside risk)
  - Volatility and Correlation Analysis
- **Monte Carlo Simulations**: 1000+ path simulations for scenario analysis
- **Portfolio Optimization**: Mean-variance optimization using SLSQP algorithm
- **Correlation Matrix Analysis**: Inter-asset relationship insights

### Data Mart Layer
- **Fact Tables**: Central repository for returns data
- **Feature Engineering**: Technical indicators and derived metrics
- **Long-format Data**: Tableau and PowerBI-friendly output formats
- **Correlation Matrices**: Pivot tables for visual analysis

### Visualization and Reporting
- **Interactive Dashboards**: PowerBI and Tableau integration
- **Portfolio Allocation Charts**: Optimized weight visualization
- **Efficient Frontier Analysis**: Risk-return trade-off visualization
- **Correlation Heatmaps**: Asset relationship visualization

### Data Quality and Logging
- **Comprehensive Logging**: Debug and error tracking
- **Data Validation**: Ensure clean, consistent data
- **Error Handling**: Robust exception management

---

## Architecture

```
financial-intelligence-dashboard/
├── data/
│   ├── raw/                    # Raw market data
│   ├── processed/              # Cleaned, validated data
│   ├── features/               # Feature engineering outputs
│   └── marts/                  # Analysis-ready datasets
├── src/
│   ├── ingestion/              # Market data fetching
│   ├── processing/             # Data cleaning & validation
│   ├── features/               # Feature engineering
│   ├── quant/                  # Quantitative models
│   │   ├── risk_metrics.py     # Risk analysis
│   │   ├── portfolio_optimization.py
│   │   └── monte_carlo.py      # Simulation engine
│   └── utils/                  # Config, logging, helpers
├── notebooks/                  # Interactive analysis
├── dashboards/                 # BI tool configs
└── scripts/                    # Automation scripts
```

### Data Flow
```
Market Data → Ingestion → Processing → Features → Analytics → Dashboards
```

---

## Installation

### Prerequisites
- **Python 3.9+**
- **pip** or **conda**

### Clone Repository
```bash
git clone https://github.com/yourusername/financial-intelligence-dashboard.git
cd financial-intelligence-dashboard
```

### Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Configure Environment
Edit `src/utils/config.py` to customize:
- Tickers: `TICKERS = ["AAPL", "MSFT", "GOOGL", "^GSPC"]`
- Date Range: `START_DATE`, `END_DATE`
- Risk-free Rate: `RISK_FREE_RATE`

---

## Quick Start

### 1. Fetch Market Data
```bash
python src/ingestion/fetch_market_data.py
```
Downloads OHLCV data for configured tickers and stores in `data/raw/`.

### 2. Process & Validate Data
```bash
python src/processing/clean_data.py
python src/processing/validate_data.py
```
Cleans outliers, handles missing values, and validates data integrity.

### 3. Generate Features
```bash
python src/features/feature_engineering.py
```
Creates returns, technical indicators, and derived metrics.

### 4. Calculate Risk Metrics
```bash
python -c "from src.quant.risk_metrics import compute_metrics; print(compute_metrics())"
```
Outputs Sharpe ratio, maximum drawdown, and volatility by ticker.

### 5. Optimize Portfolio
```bash
python -c "from src.quant.portfolio_optimization import optimize_portfolio; weights, _, _ = optimize_portfolio(); print(dict(zip(['AAPL', 'MSFT', 'GOOGL', '^GSPC'], weights)))"
```
Returns optimal allocation weights for the portfolio.

### 6. Generate Reports
```bash
python scripts/portfolio_summary.py
python scripts/pivot_table.py
```
Creates CSV outputs for BI tools.

### 7. Interactive Analysis
```bash
jupyter notebook notebooks/storytelling_dashboard.ipynb
```
Open Jupyter for exploratory analysis and visualization.

---

## Key Modules

### src/quant/risk_metrics.py
Calculates financial risk indicators:
- **Sharpe Ratio**: Risk-adjusted return metric (annualized excess return / volatility)
- **Maximum Drawdown**: Peak-to-trough decline during the analysis period
- **Volatility**: Annualized standard deviation of returns

```python
from src.quant.risk_metrics import compute_metrics

metrics = compute_metrics()
print(metrics[['ticker', 'sharpe', 'max_drawdown']])
```

### src/quant/portfolio_optimization.py
Performs mean-variance portfolio optimization:
- Aligns returns across tickers
- Calculates correlation matrix
- Optimizes weights using SLSQP algorithm

```python
from src.quant.portfolio_optimization import optimize_portfolio

weights, mean_returns, cov = optimize_portfolio()
tickers = ["AAPL", "MSFT", "GOOGL", "^GSPC"]

for ticker, weight in zip(tickers, weights):
    print(f"{ticker}: {weight:.2%}")
```

### src/quant/monte_carlo.py
Runs stochastic simulations:
- 1000+ price paths per simulation
- 252-day forecasts (1 trading year)
- Used for scenario analysis and stress testing

```python
from src.quant.monte_carlo import simulate

sim = simulate("AAPL", days=252, sims=1000)
# Returns: (1000, 252) array of simulated price paths
```

### src/processing/
Data quality pipeline:
- `clean_data.py`: Outlier detection, missing value handling
- `validate_data.py`: Schema and business logic validation

---

## Dashboard Visualizations

### Portfolio Allocation Chart
The dashboard displays optimized portfolio weights across selected assets, showing the capital allocation that minimizes portfolio risk while achieving target returns.

[Screenshot: Portfolio allocation bar chart showing weights by ticker]

### Efficient Frontier
Visualizes the risk-return trade-off for individual assets and the optimal portfolio, highlighting the efficient frontier where no portfolio can achieve higher returns with the same risk.

[Screenshot: Scatter plot with efficient frontier curve and capital allocation line]

### Correlation Heatmap
Shows inter-asset correlations across the portfolio, helping identify diversification benefits and concentration risks.

[Screenshot: Correlation matrix heatmap with color scale]

### Monte Carlo Simulation Results
Displays 1000+ simulated price paths for stress testing and scenario analysis, with confidence intervals and distribution of outcomes.

[Screenshot: Multiple line plot of simulated price paths with 95% confidence bounds]

---

## Usage Examples

### Calculate Risk Metrics
```python
from src.quant.risk_metrics import compute_metrics

metrics = compute_metrics()
print(metrics[['ticker', 'sharpe', 'max_drawdown', 'volatility']])
```

**Output:**
```
  ticker   sharpe  max_drawdown  volatility
0  AAPL     0.89        -0.38      0.0182
1  MSFT     0.92        -0.42      0.0170
2  GOOGL    0.87        -0.45      0.0181
3  ^GSPC    0.71        -0.34      0.0114
```

### Optimize Portfolio
```python
from src.quant.portfolio_optimization import optimize_portfolio

weights, mean_returns, cov = optimize_portfolio()
tickers = ["AAPL", "MSFT", "GOOGL", "^GSPC"]

allocation = dict(zip(tickers, weights))
print("Optimal Allocation:", allocation)
```

### Run Monte Carlo Simulation
```python
from src.quant.monte_carlo import simulate
import matplotlib.pyplot as plt

sim = simulate("AAPL", days=252, sims=1000)
plt.figure(figsize=(12, 6))
plt.plot(sim[:, :].T, alpha=0.1, color='blue')
plt.title("AAPL Price Simulation (1000 paths, 252 days)")
plt.xlabel("Trading Days")
plt.ylabel("Normalized Price")
plt.show()
```

### Access Logger
```python
from src.utils.logger import get_logger

logger = get_logger("my_analysis")
logger.info("Starting portfolio analysis...")
logger.error("Data validation failed")
```

---

## Output Data Formats

### Correlation Matrix (Long Format)
```
ticker_1,ticker_2,correlation
AAPL,AAPL,1.0
AAPL,GOOGL,0.603
AAPL,MSFT,0.658
...
```

### Portfolio Summary
```
ticker,weight,expected_return,volatility
AAPL,0.00,0.0009,0.0182
MSFT,0.00,0.0009,0.0170
GOOGL,0.00,0.0009,0.0181
^GSPC,1.00,0.0005,0.0114
```

---

## Configuration

All configuration is centralized in `src/utils/config.py`:

```python
# Assets to analyze
TICKERS = ["AAPL", "MSFT", "GOOGL", "^GSPC"]

# Analysis period
START_DATE = "2015-01-01"
END_DATE = "2026-04-17"

# Risk-free rate (annual)
RISK_FREE_RATE = 0.04

# Trading days per year
TRADING_DAYS = 252
```

---

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| pandas | 2.3.3 | Data manipulation and analysis |
| numpy | 2.0.2 | Numerical computing |
| scipy | 1.13.1 | Optimization algorithms |
| matplotlib | 3.9.4 | Static visualizations |
| seaborn | 0.13.2 | Statistical graphics |
| pyarrow | 21.0.0 | Parquet file I/O |

See `requirements.txt` for complete dependency list.

---

## Testing

Run data validation:
```bash
python src/processing/validate_data.py
```

Test logger functionality:
```bash
python -c "from src.utils.logger import get_logger; logger = get_logger('test'); logger.info('Logger working')"
```

---

## Data Pipeline

1. **Ingestion** - Raw OHLCV data stored as Parquet files
2. **Cleaning** - Remove duplicates and handle missing values
3. **Validation** - Verify data schema and business rules
4. **Features** - Calculate returns and technical indicators
5. **Analytics** - Compute risk metrics and optimizations
6. **Marts** - Create BI-ready output tables
7. **Visualization** - Generate dashboards and reports

---

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-analysis`
3. Commit changes: `git commit -m "Add new quantitative metric"`
4. Push to branch: `git push origin feature/new-analysis`
5. Submit a pull request

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Support and Questions

- **Documentation**: See `notebooks/` for examples
- **Issues**: Open an issue on GitHub
- **Discussions**: Start a discussion for feature requests

---

## Performance Metrics

Based on historical data (2015-2026):

| Metric | AAPL | MSFT | GOOGL | ^GSPC |
|--------|------|------|-------|-------|
| Sharpe Ratio | 0.89 | 0.92 | 0.87 | 0.71 |
| Max Drawdown | -38% | -42% | -45% | -34% |
| Volatility | 1.82% | 1.70% | 1.81% | 1.14% |
| Correlation with ^GSPC | 0.75 | 0.79 | 0.72 | 1.00 |

*Metrics update based on current market data.*

---

<div align="center">

Made with care by the Financial Intelligence Team

[Back to top](#financial-intelligence-dashboard)

</div>