"""
Configuration management for Weather MCP Server
"""

import os
from typing import Optional

# API Configuration
OPENWEATHER_API_KEY: Optional[str] = os.getenv("OPENWEATHER_API_KEY")

# Try to load from .env file if not in environment
if not OPENWEATHER_API_KEY:
    try:
        from dotenv import load_dotenv

        load_dotenv()
        OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
    except ImportError:
        # python-dotenv not available, skip .env loading
        pass

if not OPENWEATHER_API_KEY:
    raise ValueError(
        "OPENWEATHER_API_KEY environment variable is required. "
        "Get a free API key at: https://openweathermap.org/api\n\n"
        "Set it with: export OPENWEATHER_API_KEY='your_api_key_here'\n"
        "Or create a .env file with: OPENWEATHER_API_KEY=your_api_key_here"
    )

OPENWEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5"
REQUEST_TIMEOUT = 30.0
MAX_RETRIES = 3
RETRY_BACKOFF_BASE = 1.0  # seconds

# Rate limiting (OpenWeatherMap free tier: 1,000 calls/day)
DAILY_API_LIMIT = 1000
# For rate limit tracking in production, you'd persist this to a file or database
# For this assignment, we'll use in-memory tracking with warnings

# MCP Server Configuration
SERVER_NAME = "weather-mcp-server"
SERVER_VERSION = "1.0.0"
