import pandas as pd
import numpy as np
import os

# ----------------------------
# FILE UTILITIES
# ----------------------------

def load_parquet_safe(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
    return pd.read_parquet(path)

def save_parquet_safe(df, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_parquet(path, index=False)

# ----------------------------
# DATE UTILITIES
# ----------------------------

def ensure_datetime(df, column="date"):
    df[column] = pd.to_datetime(df[column], errors="coerce")
    if df[column].isna().sum() > 0:
        raise ValueError(f"Invalid datetime values in {column}")
    return df

def sort_by_date(df, column="date"):
    return df.sort_values(column)

# ----------------------------
# DATA ALIGNMENT (CRITICAL FOR QUANT)
# ----------------------------

def align_dataframes_on_date(dfs):
    """
    Align multiple DataFrames on common date index.
    Returns a single aligned DataFrame.
    """
    for i in range(len(dfs)):
        dfs[i] = dfs[i].set_index("date")

    aligned = pd.concat(dfs, axis=1, join="inner")

    return aligned.dropna()

# ----------------------------
# RETURNS UTILITIES
# ----------------------------

def compute_log_returns(series):
    return np.log(series / series.shift(1))

def compute_simple_returns(series):
    return series.pct_change()

# ----------------------------
# ROLLING UTILITIES
# ----------------------------

def rolling_volatility(returns, window=30, trading_days=252):
    return returns.rolling(window).std() * np.sqrt(trading_days)

# ----------------------------
# SANITY CHECKS
# ----------------------------

def check_no_nan(df, columns):
    for col in columns:
        if df[col].isna().sum() > 0:
            raise ValueError(f"NaN values found in {col}")

def check_positive(series, name="value"):
    if (series <= 0).any():
        raise ValueError(f"Non-positive values in {name}")