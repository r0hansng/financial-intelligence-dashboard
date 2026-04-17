import yfinance as yf
import pandas as pd
import os
from time import sleep

from src.utils.config import TICKERS, START_DATE, END_DATE, RAW_DIR
from src.utils.logger import get_logger

logger = get_logger("ingestion")

def fetch_ticker(ticker):
    for attempt in range(3):
        try:
            df = yf.download(ticker, start=START_DATE, end=END_DATE)

            # --- CRITICAL FIX: Normalize schema ---
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)

            # Standardize column names (remove spaces, lowercase)
            df.columns = [col.strip() for col in df.columns]

            if df.empty:
                raise ValueError("Empty DataFrame")

            # Add explicit date column (important for downstream)
            df = df.reset_index()

            path = os.path.join(RAW_DIR, f"{ticker}.parquet")
            df.to_parquet(path, index=False)

            logger.info(f"{ticker} fetched successfully with columns: {df.columns.tolist()}")
            return

        except Exception as e:
            logger.error(f"{ticker} attempt {attempt+1} failed: {e}")
            sleep(2 ** attempt)

def run():
    os.makedirs(RAW_DIR, exist_ok=True)
    for ticker in TICKERS:
        fetch_ticker(ticker)

if __name__ == "__main__":
    run()