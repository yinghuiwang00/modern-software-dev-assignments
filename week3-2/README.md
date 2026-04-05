# Weather MCP Server

A Model Context Protocol (MCP) server that provides access to OpenWeatherMap API through standard MCP tools.

## Overview

This MCP server exposes two tools for weather information:

- **get_current_weather**: Get current weather conditions for any city
- **get_weather_forecast**: Get weather forecast (1-5 days) for any city

The server implements proper error handling, rate limiting awareness, and resilient API integration.

## Prerequisites

- **Python 3.9+**
- **pip** (Python package manager)
- **OpenWeatherMap API Key** (free tier: 1,000 calls/day)

### Getting an OpenWeatherMap API Key

1. Visit https://openweathermap.org/api
2. Sign up for a free account
3. Navigate to API keys section
4. Copy your API key

## Setup Instructions

### 1. Install Dependencies

```bash
cd week3-2
pip install -r requirements.txt
```

### 2. Set Environment Variable

Set your OpenWeatherMap API key as an environment variable:

**Linux/Mac:**
```bash
export OPENWEATHER_API_KEY="your_api_key_here"
```

**Windows (PowerShell):**
```powershell
$env:OPENWEATHER_API_KEY="your_api_key_here"
```

**Windows (Command Prompt):**
```cmd
set OPENWEATHER_API_KEY=your_api_key_here
```

### 3. Run the Server

**For local development/testing:**
```bash
python server/main.py
```

The server will start and wait for MCP client connections via STDIO.

## Claude Desktop Configuration

To use this MCP server with Claude Desktop:

### 1. Edit Claude Desktop Config

Locate and edit the Claude Desktop configuration file:

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

### 2. Add Server Configuration

Add the following configuration:

```json
{
  "mcpServers": {
    "weather": {
      "command": "python",
      "args": [
        "/path/to/week3-2/server/main.py"
      ],
      "env": {
        "OPENWEATHER_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

**Replace:**
- `/path/to/week3-2/server/main.py` with the absolute path to `main.py`
- `your_api_key_here` with your actual OpenWeatherMap API key

### 3. Restart Claude Desktop

Restart Claude Desktop to load the new MCP server.

## Tool Reference

### Tool 1: get_current_weather

Get current weather conditions for a city.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| city | string | Yes | City name (e.g., "Beijing", "London", "New York") |
| units | string | No | Units system: "metric" (°C), "imperial" (°F), "kelvin" (default: "metric") |

**Example Usage:**

```python
# Get current weather in Beijing with metric units (Celsius)
get_current_weather(city="Beijing", units="metric")

# Get current weather in New York with imperial units (Fahrenheit)
get_current_weather(city="New York", units="imperial")
```

**Example Output:**

```json
{
  "success": true,
  "data": {
    "city": "Beijing",
    "country": "CN",
    "temperature": 15.5,
    "feels_like": 14.2,
    "humidity": 65,
    "pressure": 1015,
    "description": "clear sky",
    "wind_speed": 3.5,
    "units": "metric"
  },
  "warning": null
}
```

### Tool 2: get_weather_forecast

Get weather forecast for a city (1-5 days).

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| city | string | Yes | City name (e.g., "Beijing", "London", "New York") |
| units | string | No | Units system: "metric" (°C), "imperial" (°F), "kelvin" (default: "metric") |
| days | integer | No | Number of days: 1-5 (default: 3) |

**Example Usage:**

```python
# Get 3-day forecast for London
get_weather_forecast(city="London")

# Get 5-day forecast for Tokyo with imperial units
get_weather_forecast(city="Tokyo", units="imperial", days=5)

# Get 1-day forecast for Paris
get_weather_forecast(city="Paris", days=1)
```

**Example Output:**

```json
{
  "success": true,
  "data": {
    "city": "London",
    "country": "GB",
    "units": "metric",
    "forecast": [
      {
        "day": 1,
        "date": "2026-04-05",
        "temperature_avg": 12.5,
        "feels_like_avg": 11.8,
        "humidity_avg": 70,
        "description": "light rain"
      },
      {
        "day": 2,
        "date": "2026-04-06",
        "temperature_avg": 14.2,
        "feels_like_avg": 13.5,
        "humidity_avg": 65,
        "description": "partly cloudy"
      },
      {
        "day": 3,
        "date": "2026-04-07",
        "temperature_avg": 15.8,
        "feels_like_avg": 15.1,
        "humidity_avg": 60,
        "description": "clear sky"
      }
    ]
  },
  "warning": null
}
```

## Error Handling

The server implements comprehensive error handling:

| Error Type | Cause | Response |
|------------|-------|----------|
| ValidationError | Invalid input (empty city, invalid units, etc.) | User-friendly error message |
| InvalidAPIKeyError | Missing or invalid API key | Prompt to check environment variable |
| CityNotFoundError | City not found in OpenWeatherMap | Suggest checking city name |
| RateLimitError | API rate limit exceeded (1,000 calls/day) | Warning to try again later |
| NetworkError | Network failures, timeouts | Suggest checking internet connection |

**Example Error Response:**

```json
{
  "success": false,
  "error": {
    "type": "CityNotFoundError",
    "message": "City not found. Please check the city name and try again.",
    "context": "Tool: get_current_weather"
  }
}
```

## Rate Limiting

- **Free Tier Limit**: 1,000 API calls per day
- **Tracking**: The server tracks API calls and shows warnings when approaching the limit
- **Warnings**:
  - At 80% of limit: "WARNING: Approaching daily API limit (800/1000 calls used)"
  - At 100% of limit: "WARNING: Daily API limit (1000) reached!"

## Logging

The server uses Python's logging module with output to **stderr** (following MCP best practices for STDIO transport).

**Log Format:**
```
2026-04-05 12:00:00 - weather-mcp-server - INFO - Starting weather-mcp-server v1.0.0
2026-04-05 12:00:00 - weather-mcp-server - INFO - API key configured: abc1234567...
2026-04-05 12:00:01 - weather-mcp-server - INFO - MCP server ready, waiting for connections...
2026-04-05 12:01:00 - weather-mcp-server - INFO - Getting current weather for: Beijing
```

## Troubleshooting

### Server won't start

**Problem**: `Configuration error: OPENWEATHER_API_KEY environment variable is required`

**Solution**: Set the `OPENWEATHER_API_KEY` environment variable with your API key.

### "City not found" error

**Problem**: API returns city not found even for valid cities

**Solution**:
- Check the spelling of the city name
- Try using the city name with country code: "London,GB"
- OpenWeatherMap database may not include small towns

### Rate limit errors

**Problem**: "API rate limit exceeded" errors

**Solution**:
- Free tier is limited to 1,000 calls per day
- Wait 24 hours for the limit to reset
- Consider upgrading to a paid plan at OpenWeatherMap.org

### Connection timeout

**Problem**: Network timeouts or connection errors

**Solution**:
- Check your internet connection
- The server implements automatic retry with exponential backoff
- If persistent, check if OpenWeatherMap API is experiencing outages

## Architecture

```
week3-2/
├── server/
│   ├── main.py              # MCP server entry point (STDIO transport)
│   ├── weather_service.py   # Weather API integration layer
│   ├── config.py            # Configuration and constants
│   └── utils.py             # Error handling and utilities
├── requirements.txt          # Python dependencies
├── assignment.md            # Assignment requirements
└── README.md               # This file
```

### Key Components

- **config.py**: Manages configuration including API key, URLs, timeouts
- **utils.py**: Provides error handling, input validation, and retry logic
- **weather_service.py**: Encapsulates OpenWeatherMap API interaction
- **main.py**: MCP server implementation with tool definitions

## Testing

To test the server manually:

```bash
# Install dependencies
pip install -r requirements.txt

# Set API key
export OPENWEATHER_API_KEY="your_api_key_here"

# Test with MCP inspector (optional)
# Requires: pip install mcp-cli
mcp-inspect python server/main.py

# Or use with Claude Desktop as configured above
```

## Extra Credit Features

### Implemented (Assignment Requirements)

- ✅ Two MCP tools with proper schemas
- ✅ Comprehensive error handling
- ✅ Rate limiting awareness with warnings
- ✅ Input validation for all parameters
- ✅ Retry logic with exponential backoff
- ✅ Proper logging to stderr
- ✅ Environment variable configuration

### Future Enhancements

- HTTP transport for remote deployment
- OAuth2 authentication
- Persistent rate limit tracking across sessions
- Additional weather tools (historical data, alerts)

## Resources

- [MCP Server Quickstart](https://modelcontextprotocol.io/quickstart/server)
- [OpenWeatherMap API Documentation](https://openweathermap.org/api)
- [MCP Authorization Spec](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)

## License

This project is created for educational purposes as part of the Week 3-2 assignment.
