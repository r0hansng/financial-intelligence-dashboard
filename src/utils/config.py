import os
from datetime import datetime

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

DATA_DIR = os.path.join(BASE_DIR, "data")
RAW_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")
FEATURE_DIR = os.path.join(DATA_DIR, "features")
MART_DIR = os.path.join(DATA_DIR, "marts")

# Assets
TICKERS = ["AAPL", "MSFT", "GOOGL", "^GSPC"]

# Time
START_DATE = "2015-01-01"
END_DATE = datetime.today().strftime('%Y-%m-%d')

# Risk-free rate (approx)
RISK_FREE_RATE = 0.02
TRADING_DAYS = 252