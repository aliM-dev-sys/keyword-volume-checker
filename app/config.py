import os
from typing import Dict

# Supported countries
SUPPORTED_COUNTRIES = ["US", "UK", "CA", "SA"]

# Open-source data source configuration
DATA_SOURCES = {
    "google_trends": {
        "enabled": os.getenv("GOOGLE_TRENDS_ENABLED", "true").lower() == "true",
        "timeout": int(os.getenv("GOOGLE_TRENDS_TIMEOUT", "10")),
        "rate_limit_delay": float(os.getenv("GOOGLE_TRENDS_DELAY", "1.0"))
    },
    "amazon_autocomplete": {
        "enabled": os.getenv("AMAZON_AUTOCOMPLETE_ENABLED", "true").lower() == "true",
        "timeout": int(os.getenv("AMAZON_AUTOCOMPLETE_TIMEOUT", "10")),
        "rate_limit_delay": float(os.getenv("AMAZON_AUTOCOMPLETE_DELAY", "0.5"))
    }
}

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

# Estimation method configuration
ESTIMATION_METHODS = {
    "combined": {
        "description": "Combines Google Trends and Amazon autocomplete data",
        "enabled": True
    },
    "google_trends": {
        "description": "Uses Google Trends data for volume estimation",
        "enabled": DATA_SOURCES["google_trends"]["enabled"]
    },
    "amazon_autocomplete": {
        "description": "Uses Amazon autocomplete data for volume estimation",
        "enabled": DATA_SOURCES["amazon_autocomplete"]["enabled"]
    },
    "fallback": {
        "description": "Uses keyword analysis patterns for volume estimation",
        "enabled": True
    }
}
