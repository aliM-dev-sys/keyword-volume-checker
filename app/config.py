import os
from typing import Dict

# Supported countries
SUPPORTED_COUNTRIES = ["US", "UK", "CA", "SA"]

# Data source configuration
GOOGLE_TRENDS_ENABLED = os.getenv("GOOGLE_TRENDS_ENABLED", "true").lower() == "true"
AMAZON_AUTOCOMPLETE_ENABLED = os.getenv("AMAZON_AUTOCOMPLETE_ENABLED", "true").lower() == "true"

# API configuration for external data sources
API_CONFIG = {
    "timeout": int(os.getenv("API_TIMEOUT", "30")),
    "max_retries": int(os.getenv("API_MAX_RETRIES", "3")),
    "rate_limit_delay": float(os.getenv("API_RATE_LIMIT_DELAY", "0.1"))
}

# Cache configuration
CACHE_CONFIG = {
    "enabled": os.getenv("CACHE_ENABLED", "true").lower() == "true",
    "ttl": int(os.getenv("CACHE_TTL", "86400")),  # 24 hours in seconds
    "db_path": os.getenv("CACHE_DB_PATH", "data/keyword_volumes.db")
}

# Available estimation methods
AVAILABLE_METHODS = ["combined", "google_trends", "amazon_autocomplete", "fallback"]
