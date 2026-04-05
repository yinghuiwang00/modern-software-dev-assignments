#!/usr/bin/env python3
"""
Weather MCP Server
Provides access to OpenWeatherMap API through Model Context Protocol
"""
import asyncio
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

# Add parent directory to path for absolute imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from server.config import SERVER_NAME, SERVER_VERSION
from server.utils import (
    format_error_message,
    logger,
    rate_limit_warning,
)
from server.weather_service import WeatherService

# Configure logging to stderr (MCP best practice for STDIO transport)
# Note: logging.basicConfig() is already called in utils.py

# Create MCP server
server = Server(SERVER_NAME)


@server.list_tools()
async def handle_list_tools() -> List[Tool]:
    """List available tools."""
    return [
        Tool(
            name="get_current_weather",
            description="Get current weather for a city",
            inputSchema={
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "City name (e.g., 'Beijing', 'London', 'New York')",
                        "minLength": 2,
                        "maxLength": 100,
                    },
                    "units": {
                        "type": "string",
                        "description": "Units system for temperature",
                        "enum": ["metric", "imperial", "kelvin"],
                        "default": "metric",
                    },
                },
                "required": ["city"],
            },
        ),
        Tool(
            name="get_weather_forecast",
            description="Get weather forecast for a city (1-5 days)",
            inputSchema={
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "City name (e.g., 'Beijing', 'London', 'New York')",
                        "minLength": 2,
                        "maxLength": 100,
                    },
                    "units": {
                        "type": "string",
                        "description": "Units system for temperature",
                        "enum": ["metric", "imperial", "kelvin"],
                        "default": "metric",
                    },
                    "days": {
                        "type": "integer",
                        "description": "Number of days (1-5)",
                        "minimum": 1,
                        "maximum": 5,
                        "default": 3,
                    },
                },
                "required": ["city"],
            },
        ),
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any] | None) -> List[TextContent]:
    """Handle tool calls."""
    try:
        # Initialize weather service
        async with WeatherService() as weather_service:
            if name == "get_current_weather":
                city = arguments.get("city") if arguments else None
                units = arguments.get("units") if arguments else None

                logger.info(f"Getting current weather for: {city}")

                data = await weather_service.get_current_weather(city=city, units=units)

                # Check rate limit
                call_count = weather_service.get_api_call_count()
                warning = rate_limit_warning(call_count)
                if warning:
                    logger.warning(warning)

                result = {"success": True, "data": data, "warning": warning}

                return [TextContent(type="text", text=json.dumps(result, indent=2))]

            elif name == "get_weather_forecast":
                city = arguments.get("city") if arguments else None
                units = arguments.get("units") if arguments else None
                days = arguments.get("days") if arguments else None

                logger.info(f"Getting {days or 3} day forecast for: {city}")

                data = await weather_service.get_weather_forecast(city=city, units=units, days=days)

                # Check rate limit
                call_count = weather_service.get_api_call_count()
                warning = rate_limit_warning(call_count)
                if warning:
                    logger.warning(warning)

                result = {"success": True, "data": data, "warning": warning}

                return [TextContent(type="text", text=json.dumps(result, indent=2))]

            else:
                raise ValueError(f"Unknown tool: {name}")

    except Exception as e:
        # Format error for user-friendly response
        error_response = format_error_message(e, f"Tool: {name}")
        logger.error(f"Tool '{name}' failed: {e}", exc_info=True)
        return [TextContent(type="text", text=json.dumps(error_response, indent=2))]


async def main():
    """Main entry point."""
    logger.info(f"Starting {SERVER_NAME} v{SERVER_VERSION}")
    logger.info("OpenWeatherMap MCP Server - STDIO Transport")

    # Verify API key is set
    try:
        from server.config import OPENWEATHER_API_KEY

        logger.info(f"API key configured: {OPENWEATHER_API_KEY[:10]}...")
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        logger.error("Please set the OPENWEATHER_API_KEY environment variable")
        logger.error("Get a free API key at: https://openweathermap.org/api")
        return

    # Run MCP server with STDIO transport
    async with stdio_server() as (read_stream, write_stream):
        init_options = InitializationOptions(
            server_name=SERVER_NAME,
            server_version=SERVER_VERSION,
            capabilities=server.get_capabilities(
                notification_options=NotificationOptions(),
                experimental_capabilities={},
            ),
        )

        logger.info("MCP server ready, waiting for connections...")
        await server.run(
            read_stream,
            write_stream,
            init_options,
            raise_exceptions=True,
        )


if __name__ == "__main__":
    asyncio.run(main())
