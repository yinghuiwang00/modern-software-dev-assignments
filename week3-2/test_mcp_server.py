#!/usr/bin/env python3
"""
Test script for Weather MCP Server
Tests the server functionality using environment variable for API key
"""
import asyncio
import os
import sys
from pathlib import Path

# Add project directory to path to allow absolute imports
project_dir = Path(__file__).parent
sys.path.insert(0, str(project_dir))

from server.utils import CityNotFoundError, InvalidAPIKeyError, ValidationError
from server.weather_service import WeatherService


async def test_api_key_from_env():
    """Test that API key is loaded from environment variable"""
    print("=" * 60)
    print("Test 1: API Key from Environment Variable")
    print("=" * 60)

    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        print("❌ FAILED: OPENWEATHER_API_KEY environment variable not set")
        print("   Set it with: export OPENWEATHER_API_KEY='your_api_key_here'")
        return False

    print(f"✅ API key found: {api_key[:10]}...")
    return True


async def test_current_weather():
    """Test getting current weather for a city"""
    print("\n" + "=" * 60)
    print("Test 2: Get Current Weather")
    print("=" * 60)

    try:
        async with WeatherService() as weather_service:
            print("Fetching weather for Beijing...")
            data = await weather_service.get_current_weather(city="Beijing", units="metric")

            print(f"✅ Successfully fetched weather for {data['city']}, {data['country']}")
            print(f"   Temperature: {data['temperature']}°C (feels like {data['feels_like']}°C)")
            print(f"   Description: {data['description']}")
            print(f"   Humidity: {data['humidity']}%")
            print(f"   Wind Speed: {data['wind_speed']} m/s")
            return True

    except InvalidAPIKeyError:
        print("❌ FAILED: Invalid API key")
        return False
    except CityNotFoundError:
        print("❌ FAILED: City not found")
        return False
    except Exception as e:
        print(f"❌ FAILED: {type(e).__name__}: {e}")
        return False


async def test_weather_forecast():
    """Test getting weather forecast for a city"""
    print("\n" + "=" * 60)
    print("Test 3: Get Weather Forecast")
    print("=" * 60)

    try:
        async with WeatherService() as weather_service:
            print("Fetching 3-day forecast for London...")
            data = await weather_service.get_weather_forecast(city="London", units="metric", days=3)

            print(f"✅ Successfully fetched forecast for {data['city']}, {data['country']}")
            for day in data["forecast"]:
                print(
                    f"   Day {day['day']} ({day['date']}): "
                    f"{day['temperature_avg']}°C - {day['description']}"
                )
            return True

    except InvalidAPIKeyError:
        print("❌ FAILED: Invalid API key")
        return False
    except CityNotFoundError:
        print("❌ FAILED: City not found")
        return False
    except Exception as e:
        print(f"❌ FAILED: {type(e).__name__}: {e}")
        return False


async def test_error_handling():
    """Test error handling for invalid inputs"""
    print("\n" + "=" * 60)
    print("Test 4: Error Handling")
    print("=" * 60)

    tests_passed = 0
    tests_total = 3

    # Test invalid city
    try:
        async with WeatherService() as weather_service:
            await weather_service.get_current_weather(city="", units="metric")
        print("❌ FAILED: Should have raised ValidationError for empty city")
    except ValidationError as e:
        print(f"✅ Correctly raised ValidationError for empty city: {e}")
        tests_passed += 1

    # Test invalid units
    try:
        async with WeatherService() as weather_service:
            await weather_service.get_current_weather(city="Tokyo", units="invalid")
        print("❌ FAILED: Should have raised ValidationError for invalid units")
    except ValidationError as e:
        print(f"✅ Correctly raised ValidationError for invalid units: {e}")
        tests_passed += 1

    # Test city not found
    try:
        async with WeatherService() as weather_service:
            await weather_service.get_current_weather(city="InvalidCityName12345")
        print("❌ FAILED: Should have raised CityNotFoundError")
    except CityNotFoundError as e:
        print(f"✅ Correctly raised CityNotFoundError: {e}")
        tests_passed += 1

    print(f"\n   Passed {tests_passed}/{tests_total} error handling tests")
    return tests_passed == tests_total


async def test_rate_limit_tracking():
    """Test that API call count is tracked"""
    print("\n" + "=" * 60)
    print("Test 5: Rate Limit Tracking")
    print("=" * 60)

    try:
        async with WeatherService() as weather_service:
            initial_count = weather_service.get_api_call_count()
            print(f"Initial API call count: {initial_count}")

            await weather_service.get_current_weather(city="New York")
            await weather_service.get_current_weather(city="Paris")

            final_count = weather_service.get_api_call_count()
            print(f"Final API call count: {final_count}")

            if final_count == initial_count + 2:
                print("✅ API call count increased correctly by 2")
                return True
            else:
                print(f"❌ FAILED: Expected {initial_count + 2}, got {final_count}")
                return False

    except Exception as e:
        print(f"❌ FAILED: {type(e).__name__}: {e}")
        return False


async def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("Weather MCP Server - Test Suite")
    print("=" * 60)

    # Check API key first
    api_key_test = await test_api_key_from_env()
    if not api_key_test:
        print("\n❌ ABORTING: API key not configured")
        print("Please set the OPENWEATHER_API_KEY environment variable:")
        print("  export OPENWEATHER_API_KEY='your_api_key_here'")
        sys.exit(1)

    # Run all tests
    results = []

    results.append(await test_current_weather())
    results.append(await test_weather_forecast())
    results.append(await test_error_handling())
    results.append(await test_rate_limit_tracking())

    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)

    total_tests = len(results)
    passed_tests = sum(results)

    print(f"Total tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {total_tests - passed_tests}")

    if all(results):
        print("\n✅ ALL TESTS PASSED!")
        return 0
    else:
        print("\n❌ SOME TESTS FAILED")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
