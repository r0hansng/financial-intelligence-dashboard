import pandas as pd
import os

from src.utils.config import RAW_DIR, PROCESSED_DIR, TICKERS
from src.utils.logger import get_logger

logger = get_logger("cleaning")

def clean_ticker(ticker):
    path = os.path.join(RAW_DIR, f"{ticker}.parquet")
    df = pd.read_parquet(path)

    # --- FIX 1: Ensure 'date' column exists properly ---
    if "Date" in df.columns:
        df = df.rename(columns={"Date": "date"})
    elif "date" not in df.columns:
        raise ValueError(f"No date column found in {ticker}")

    # Avoid duplicate reset_index
    if df.index.name == "Date":
        df = df.reset_index()

    # --- FIX 2: Robust price selection ---
    if "Adj Close" in df.columns:
        df["price"] = df["Adj Close"]
    elif "Close" in df.columns:
        df["price"] = df["Close"]
    else:
        raise ValueError(f"No valid price column in {ticker}")

    # --- FIX 3: Standard cleaning ---
    df = df.sort_values("date")

    # Forward fill only numeric columns
    numeric_cols = df.select_dtypes(include=["float64", "int64"]).columns
    df[numeric_cols] = df[numeric_cols].ffill()

    # Remove duplicates
    df = df.drop_duplicates(subset=["date"])

    # --- FIX 4: Strong validation ---
    if df["price"].isna().sum() > 0:
        raise ValueError(f"Missing prices in {ticker}")

    if (df["price"] <= 0).any():
        raise ValueError(f"Invalid price values in {ticker}")

    # Ensure datetime format
    df["date"] = pd.to_datetime(df["date"])

    out_path = os.path.join(PROCESSED_DIR, f"{ticker}.parquet")
    df.to_parquet(out_path, index=False)

    logger.info(f"{ticker} cleaned | rows={len(df)}")

def run():
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    for ticker in TICKERS:
        clean_ticker(ticker)

if __name__ == "__main__":
    run()