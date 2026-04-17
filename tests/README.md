# Test Suite

Simple unit tests for the Financial Intelligence Dashboard project.

## Running Tests

### Run all tests
```bash
pytest
```

### Run tests with verbose output
```bash
pytest -v
```

### Run specific test file
```bash
pytest tests/test_risk_metrics.py
```

### Run specific test class
```bash
pytest tests/test_risk_metrics.py::TestSharpeRatio
```

### Run specific test
```bash
pytest tests/test_risk_metrics.py::TestSharpeRatio::test_sharpe_ratio_positive_returns
```

### Run tests with coverage report
```bash
pytest --cov=src tests/
```

### Run tests with output capture disabled (to see print statements)
```bash
pytest -s
```

## Test Coverage

### test_risk_metrics.py
Tests for risk metric calculations:
- Sharpe ratio computation
- Maximum drawdown calculation
- Edge cases (zero volatility, negative returns, etc.)

### test_config.py
Tests for configuration values:
- TICKERS list
- TRADING_DAYS constant
- RISK_FREE_RATE setting

### test_data_validation.py
Tests for data quality:
- DataFrame structure validation
- Missing value detection
- Return value ranges
- Data point requirements

### test_helpers.py
Tests for utility functions:
- DateTime handling
- Date sorting
- DataFrame alignment
- Multi-ticker data handling

## Test Fixtures

Pytest fixtures are defined in `conftest.py`:
- `sample_returns`: Series of random returns (252 periods)
- `sample_dataframe`: DataFrame with AAPL data
- `sample_multi_ticker_dataframe`: DataFrame with multiple tickers

## Dependencies

Tests require:
- pytest
- pandas
- numpy
- scipy

All dependencies are in `requirements.txt`.
