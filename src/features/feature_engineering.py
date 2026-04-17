import pandas as pd
import numpy as np
import os

from src.utils.config import PROCESSED_DIR, FEATURE_DIR, TICKERS, TRADING_DAYS
from src.utils.helpers import compute_log_returns, rolling_volatility

def compute_features(ticker):
    df = pd.read_parquet(os.path.join(PROCESSED_DIR, f"{ticker}.parquet"))

    df = df.sort_values("date")

    # Returns
    df["returns"] = compute_log_returns(df["price"])
    df["vol_30"] = rolling_volatility(df["returns"])

    # Rolling volatility
    df["vol_30"] = df["returns"].rolling(30).std() * np.sqrt(TRADING_DAYS)

    # Moving averages
    df["ma_50"] = df["price"].rolling(50).mean()
    df["ma_200"] = df["price"].rolling(200).mean()

    df = df.dropna()

    df.to_parquet(os.path.join(FEATURE_DIR, f"{ticker}.parquet"))

def run():
    os.makedirs(FEATURE_DIR, exist_ok=True)
    for ticker in TICKERS:
        compute_features(ticker)

if __name__ == "__main__":
    run()