from src.ingestion.fetch_market_data import run as ingest
from src.processing.clean_data import run as clean
from src.features.feature_engineering import run as features
from src.data_mart.build_marts import run as mart
from src.processing.validate_data import run as validate

if __name__ == "__main__":
    ingest()
    clean()
    validate()  
    features()
    mart()