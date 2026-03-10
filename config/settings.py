# config/settings.py

SCAN_INTERVAL = 300  # seconds

TOP_PAIRS_LIMIT = 20

TIMEFRAMES = {
    "trend_tf": "4h",
    "entry_tf": "15m"
}

CANDLE_LIMITS = {
    "trend": 200,
    "entry": 300
}

DATABASE_URL = "sqlite:///signals.db"

LOG_LEVEL = "INFO"