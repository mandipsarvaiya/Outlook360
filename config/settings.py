"""
OmniPulse AI - Global Application Settings
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Ensure project root is in python path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

load_dotenv(BASE_DIR / ".env")


class AppSettings:
    """Centralized application configuration."""
    APP_NAME: str = os.getenv("APP_NAME", "Outlook360")
    APP_TAGLINE: str = "Universal Enterprise BI & Predictive Analytics Platform"
    APP_VERSION: str = "1.0.0"
    APP_ENV: str = os.getenv("APP_ENV", "development")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() in ("true", "1", "yes")

    # Paths
    BASE_DIR: Path = BASE_DIR
    DATABASE_DIR: Path = BASE_DIR / "database"
    REPORTS_DIR: Path = BASE_DIR / "reports"
    DOCS_DIR: Path = BASE_DIR / "docs"

    # Default Domain
    ACTIVE_DOMAIN: str = os.getenv("ACTIVE_DOMAIN", "supermarket").lower()

    # Supported Domains
    SUPPORTED_DOMAINS = {
        "supermarket": "🛒 Supermarket & Grocery",
        "pharmacy": "💊 Pharmacy & Healthcare",
        "restaurant": "🍽️ Restaurant & Cafe",
        "fashion": "👗 Fashion & Apparel",
        "electronics": "📱 Electronics & Mobile",
        "ecommerce": "📦 E-Commerce Direct"
    }

    # Data Science Defaults
    RANDOM_SEED: int = 42
    DEFAULT_FORECAST_DAYS: int = 30
    DEFAULT_RFM_CLUSTERS: int = 4
    DEFAULT_MIN_SUPPORT: float = 0.02
    DEFAULT_MIN_CONFIDENCE: float = 0.20
    DEFAULT_OUTLIER_CONTAMINATION: float = 0.03
