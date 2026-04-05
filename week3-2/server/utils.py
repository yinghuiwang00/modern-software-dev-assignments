"""
Utility functions for error handling, retry logic, and logging
"""

import asyncio
import logging
from typing import Any, Awaitable, Callable, Dict, Optional

# Configure logging to stderr (not stdout) as per MCP best practices
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


class WeatherAPIError(Exception):
    """Base exception for Weather API errors"""

    pass


class InvalidAPIKeyError(WeatherAPIError):
    """Raised when API key is invalid"""

    pass


class CityNotFoundError(WeatherAPIError):
    """Raised when city is not found"""

    pass


class RateLimitError(WeatherAPIError):
    """Raised when API rate limit is exceeded"""

    pass


class NetworkError(WeatherAPIError):
    """Raised for network-related errors"""

    pass


class ValidationError(WeatherAPIError):
    """Raised for input validation errors"""

    pass


def validate_city_name(city: str) -> str:
    """
    Validate and sanitize city name.

    Args:
        city: Raw city name input

    Returns:
        Sanitized city name

    Raises:
        ValidationError: If city name is invalid
    """
    if not city or not isinstance(city, str):
        raise ValidationError("City name must be a non-empty string")

    city = city.strip()
    if len(city) < 2:
        raise ValidationError("City name must be at least 2 characters")
    if len(city) > 100:
        raise ValidationError("City name must not exceed 100 characters")

    return city


def validate_units(units: Optional[str]) -> str:
    """
    Validate units parameter.

    Args:
        units: Units system (metric, imperial, or kelvin)

    Returns:
        Validated units string (default: metric)

    Raises:
        ValidationError: If units are invalid
    """
    if units is None:
        return "metric"

    valid_units = ["metric", "imperial", "kelvin"]
    if units not in valid_units:
        raise ValidationError(f"Units must be one of: {', '.join(valid_units)}")

    return units


def validate_days(days: Optional[int]) -> int:
    """
    Validate days parameter for forecast.

    Args:
        days: Number of days (1-5)

    Returns:
        Validated number of days (default: 3)

    Raises:
        ValidationError: If days are out of range
    """
    if days is None:
        return 3

    if not isinstance(days, int) or days < 1 or days > 5:
        raise ValidationError("Days must be an integer between 1 and 5")

    return days


def format_error_message(error: Exception, context: str = "") -> Dict[str, Any]:
    """
    Format error message for user-friendly response.

    Args:
        error: The exception that occurred
        context: Additional context about the operation

    Returns:
        Formatted error dictionary
    """
    error_type = type(error).__name__
    error_msg = str(error)

    # Map to user-friendly messages
    if isinstance(error, InvalidAPIKeyError):
        user_msg = "Invalid OpenWeatherMap API key. Please check your OPENWEATHER_API_KEY environment variable."
    elif isinstance(error, CityNotFoundError):
        user_msg = "City not found. Please check the city name and try again."
    elif isinstance(error, RateLimitError):
        user_msg = "API rate limit exceeded. Please try again later."
    elif isinstance(error, ValidationError):
        user_msg = f"Invalid input: {error_msg}"
    elif isinstance(error, NetworkError):
        user_msg = "Network error occurred. Please check your internet connection and try again."
    else:
        user_msg = f"An unexpected error occurred: {error_msg}"

    return {
        "success": False,
        "error": {"type": error_type, "message": user_msg, "context": context},
    }


def rate_limit_warning(call_count: int, limit: int = 1000) -> Optional[str]:
    """
    Check if rate limit warning should be shown.

    Args:
        call_count: Number of API calls made
        limit: Daily API call limit

    Returns:
        Warning message or None
    """
    if call_count >= limit:
        return f"WARNING: Daily API limit ({limit}) reached!"

    if call_count >= limit * 0.8:
        return f"WARNING: Approaching daily API limit ({call_count}/{limit} calls used)"

    return None


async def retry_with_backoff(
    func: Callable[..., Awaitable[Any]],
    max_retries: int = 3,
    base_backoff: float = 1.0,
    *args,
    **kwargs,
) -> Any:
    """
    Execute a function with exponential backoff retry logic.

    Args:
        func: Async function to execute
        max_retries: Maximum number of retry attempts
        base_backoff: Base backoff time in seconds
        *args: Positional arguments for func
        **kwargs: Keyword arguments for func

    Returns:
        Result from func

    Raises:
        WeatherAPIError: If all retries fail
    """
    last_error = None

    for attempt in range(max_retries + 1):
        try:
            return await func(*args, **kwargs)
        except asyncio.TimeoutError as e:
            last_error = e
            logger.warning(f"Timeout on attempt {attempt + 1}/{max_retries + 1}")
        except Exception as e:
            last_error = e
            # Don't retry on validation errors, API key errors, or city not found
            if isinstance(e, (ValidationError, InvalidAPIKeyError, CityNotFoundError)):
                raise
            logger.warning(f"Error on attempt {attempt + 1}/{max_retries + 1}: {e}")

        # Don't sleep after the last attempt
        if attempt < max_retries:
            backoff_time = base_backoff * (2**attempt)
            logger.info(f"Retrying in {backoff_time:.1f} seconds...")
            await asyncio.sleep(backoff_time)

    raise NetworkError(f"Operation failed after {max_retries + 1} attempts: {last_error}")
