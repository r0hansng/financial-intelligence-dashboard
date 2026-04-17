import sys
from pathlib import Path

# Add parent directory to path so src module can be imported
sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
import numpy as np
from src.quant.portfolio_optimization import optimize_portfolio
from src.utils.config import TICKERS

weights, mean_returns, cov = optimize_portfolio()

df = pd.DataFrame({
    "ticker": TICKERS,
    "weight": weights,
    "expected_return": mean_returns,
    "volatility": np.sqrt(np.diag(cov))
})

df.to_csv("data/marts/portfolio_summary.csv", index=False)

df = pd.read_parquet("data/marts/fact_returns.parquet")
df.to_csv("data/marts/fact_returns.csv", index=False)