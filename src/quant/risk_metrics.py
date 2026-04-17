import pandas as pd
import numpy as np
import os

from src.utils.config import FEATURE_DIR, TICKERS, RISK_FREE_RATE, TRADING_DAYS

def sharpe_ratio(returns):
    mean = returns.mean() * TRADING_DAYS
    std = returns.std() * np.sqrt(TRADING_DAYS)
    return (mean - RISK_FREE_RATE) / std

def max_drawdown(series):
    cum = (1 + series).cumprod()
    peak = cum.cummax()
    drawdown = (cum - peak) / peak
    return drawdown.min()

def compute_metrics():
    results = []

    for ticker in TICKERS:
        df = pd.read_parquet(os.path.join(FEATURE_DIR, f"{ticker}.parquet"))

        sr = sharpe_ratio(df["returns"])
        mdd = max_drawdown(df["returns"])

        results.append({
            "ticker": ticker,
            "sharpe": sr,
            "max_drawdown": mdd
        })

    return pd.DataFrame(results)

if __name__ == "__main__":
    df = compute_metrics()
    print(df)