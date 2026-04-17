import pandas as pd
import os

from src.utils.config import FEATURE_DIR, MART_DIR, TICKERS

def build_returns_mart():
    dfs = []

    for t in TICKERS:
        df = pd.read_parquet(os.path.join(FEATURE_DIR, f"{t}.parquet"))
        df["ticker"] = t
        dfs.append(df)

    final = pd.concat(dfs)
    final.to_parquet(os.path.join(MART_DIR, "fact_returns.parquet"))

def run():
    os.makedirs(MART_DIR, exist_ok=True)
    build_returns_mart()

if __name__ == "__main__":
    run()