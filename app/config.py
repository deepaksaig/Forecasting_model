"""Application configuration and defaults."""
from pathlib import Path

DATA_DIR = Path("data")
UPLOAD_DIR = DATA_DIR / "uploads"
MODEL_DIR = DATA_DIR / "models"

API_KEY_PLACEHOLDER = "YOUR_API_KEY_HERE"
DEFAULT_FORECAST_HORIZON = 12
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
MODEL_DIR.mkdir(parents=True, exist_ok=True)
