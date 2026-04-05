"""
Weather service - Handles interaction with OpenWeatherMap API
"""
import asyncio
import httpx
from typing import Any, Dict, Optional

from .config import (
    OPENWEATHER_API_KEY,
    OPENWEATHER_BASE_URL,
    REQUEST_TIMEOUT,
    MAX_RETRIES,
    RETRY_BACKOFF_BASE,
)
from .utils import (
    validate_city_name,
    validate_units,
    validate_days,
    retry_with_backoff,
    InvalidAPIKeyError,
    CityNotFoundError,
    RateLimitError,
    NetworkError,
    ValidationError,
)


class WeatherService:
    """Service for interacting with OpenWeatherMap API"""

    def __init__(self):
        self.client: Optional[httpx.AsyncClient] = None
        self.api_call_count = 0

    async def __aenter__(self):
        """Initialize HTTP client"""
        self.client = httpx.AsyncClient(timeout=REQUEST_TIMEOUT)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Close HTTP client"""
        if self.client:
            await self.client.aclose()

    def _handle_api_error(self, status_code: int, response_text: str) -> None:
        """
        Handle API error responses and raise appropriate exceptions.

        Args:
            status_code: HTTP status code
            response_text: Response body text

        Raises:
            InvalidAPIKeyError: For 401/403 status codes
            CityNotFoundError: For 404 status code
            RateLimitError: For 429 status code
            NetworkError: For other error status codes
        """
        if status_code in [401, 403]:
            raise InvalidAPIKeyError("Invalid API key")
        elif status_code == 404:
            raise CityNotFoundError("City not found")
        elif status_code == 429:
            raise RateLimitError("API rate limit exceeded")
        else:
            raise NetworkError(f"API request failed with status {status_code}: {response_text}")

    async def get_current_weather(
        self,
        city: str,
        units: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get current weather for a city.

        Args:
            city: City name
            units: Units system (metric/imperial/kelvin)

        Returns:
            Current weather data

        Raises:
            ValidationError: If input is invalid
            InvalidAPIKeyError: If API key is invalid
            CityNotFoundError: If city is not found
            RateLimitError: If rate limit is exceeded
            NetworkError: If network error occurs
        """
        # Validate input
        city = validate_city_name(city)
        units = validate_units(units)

        # Make API request with retry logic
        async def _make_request():
            params = {
                "q": city,
                "appid": OPENWEATHER_API_KEY,
                "units": units
            }

            response = await self.client.get(
                f"{OPENWEATHER_BASE_URL}/weather",
                params=params
            )

            self.api_call_count += 1

            if response.status_code != 200:
                self._handle_api_error(response.status_code, response.text)

            return response.json()

        try:
            data = await retry_with_backoff(
                _make_request,
                max_retries=MAX_RETRIES,
                base_backoff=RETRY_BACKOFF_BASE
            )
        except Exception as e:
            raise

        # Format and return response
        return {
            "city": data.get("name"),
            "country": data.get("sys", {}).get("country"),
            "temperature": data.get("main", {}).get("temp"),
            "feels_like": data.get("main", {}).get("feels_like"),
            "humidity": data.get("main", {}).get("humidity"),
            "pressure": data.get("main", {}).get("pressure"),
            "description": data.get("weather", [{}])[0].get("description"),
            "wind_speed": data.get("wind", {}).get("speed"),
            "units": units
        }

    async def get_weather_forecast(
        self,
        city: str,
        units: Optional[str] = None,
        days: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Get weather forecast for a city.

        Args:
            city: City name
            units: Units system (metric/imperial/kelvin)
            days: Number of days (1-5)

        Returns:
            Weather forecast data

        Raises:
            ValidationError: If input is invalid
            InvalidAPIKeyError: If API key is invalid
            CityNotFoundError: If city is not found
            RateLimitError: If rate limit is exceeded
            NetworkError: If network error occurs
        """
        # Validate input
        city = validate_city_name(city)
        units = validate_units(units)
        days = validate_days(days)

        # Make API request with retry logic
        async def _make_request():
            params = {
                "q": city,
                "appid": OPENWEATHER_API_KEY,
                "units": units,
                "cnt": days * 8  # OpenWeather returns 3-hour intervals (8 per day)
            }

            response = await self.client.get(
                f"{OPENWEATHER_BASE_URL}/forecast",
                params=params
            )

            self.api_call_count += 1

            if response.status_code != 200:
                self._handle_api_error(response.status_code, response.text)

            return response.json()

        try:
            data = await retry_with_backoff(
                _make_request,
                max_retries=MAX_RETRIES,
                base_backoff=RETRY_BACKOFF_BASE
            )
        except Exception as e:
            raise

        # Process forecast data into daily summaries
        forecasts = data.get("list", [])
        daily_forecasts = []

        for day in range(days):
            day_start = day * 8
            day_end = min(day_start + 8, len(forecasts))

            if day_start >= len(forecasts):
                break

            day_data = forecasts[day_start:day_end]

            # Calculate daily averages
            temps = [item.get("main", {}).get("temp") for item in day_data]
            feels_like = [item.get("main", {}).get("feels_like") for item in day_data]
            humidity = [item.get("main", {}).get("humidity") for item in day_data]
            descriptions = [
                item.get("weather", [{}])[0].get("description")
                for item in day_data
            ]

            daily_forecasts.append({
                "day": day + 1,
                "date": day_data[0].get("dt_txt", "").split(" ")[0],
                "temperature_avg": round(sum(temps) / len(temps), 2) if temps else None,
                "feels_like_avg": round(sum(feels_like) / len(feels_like), 2) if feels_like else None,
                "humidity_avg": round(sum(humidity) / len(humidity), 2) if humidity else None,
                "description": max(set(descriptions), key=descriptions.count) if descriptions else None,
                "units": units
            })

        return {
            "city": data.get("city", {}).get("name"),
            "country": data.get("city", {}).get("country"),
            "forecast": daily_forecasts,
            "units": units
        }

    def get_api_call_count(self) -> int:
        """Get the number of API calls made"""
        return self.api_call_count
