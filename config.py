from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent

DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
FEATURE_DATA_DIR = DATA_DIR / "features"
SPLIT_DATA_DIR = DATA_DIR / "splits"

ML_DIR = PROJECT_ROOT / "ml"
MODEL_DIR = ML_DIR / "models"

RISK_ENGINE_DIR = PROJECT_ROOT / "risk_engine"

RANDOM_SEED = 42