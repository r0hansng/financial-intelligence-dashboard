import pandas as pd
import os

from src.utils.config import PROCESSED_DIR, TICKERS
from src.utils.logger import get_logger

logger = get_logger("validation")

REQUIRED_COLUMNS = ["date", "price"]

def validate_schema(df, ticker):
    missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_cols:
        raise ValueError(f"{ticker}: Missing columns {missing_cols}")

def validate_dtypes(df, ticker):
    if not pd.api.types.is_datetime64_any_dtype(df["date"]):
        raise ValueError(f"{ticker}: 'date' is not datetime")

    if not pd.api.types.is_numeric_dtype(df["price"]):
        raise ValueError(f"{ticker}: 'price' is not numeric")

def validate_nulls(df, ticker):
    if df["price"].isna().sum() > 0:
        raise ValueError(f"{ticker}: Null values in price")

def validate_price_values(df, ticker):
    if (df["price"] <= 0).any():
        raise ValueError(f"{ticker}: Non-positive prices detected")

def validate_duplicates(df, ticker):
    if df.duplicated(subset=["date"]).any():
        raise ValueError(f"{ticker}: Duplicate dates found")

def validate_time_continuity(df, ticker):
    df = df.sort_values("date")

    # Check gaps in business days
    expected = pd.date_range(start=df["date"].min(),
                             end=df["date"].max(),
                             freq="B")

    missing = set(expected) - set(df["date"])

    # Allow small gaps (market holidays), flag large gaps
    if len(missing) > 10:
        logger.warning(f"{ticker}: Large gaps in time series ({len(missing)} missing days)")

def validate_ticker(ticker):
    path = os.path.join(PROCESSED_DIR, f"{ticker}.parquet")

    if not os.path.exists(path):
        raise FileNotFoundError(f"{ticker}: Processed file not found")

    df = pd.read_parquet(path)

    validate_schema(df, ticker)
    validate_dtypes(df, ticker)
    validate_nulls(df, ticker)
    validate_price_values(df, ticker)
    validate_duplicates(df, ticker)
    validate_time_continuity(df, ticker)

    logger.info(f"{ticker} validation passed")

def run():
    for ticker in TICKERS:
        validate_ticker(ticker)

if __name__ == "__main__":
    run()