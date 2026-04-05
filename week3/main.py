#!/usr/bin/env python3
"""
MCP Server for Note and Action Item Management
Based on week2 API running at localhost:8000
"""

import asyncio
import json
import logging
from typing import Any, Dict, List

import httpx
from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    EmbeddedResource,
    ImageContent,
    Resource,
    TextContent,
    Tool,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# API base URL
API_BASE_URL = "http://localhost:8000"

# Create MCP server
server = Server("note-action-server")

# HTTP client
client = httpx.AsyncClient(base_url=API_BASE_URL, timeout=30.0)


@server.list_resources()
async def handle_list_resources() -> List[Resource]:
    """List available resources."""
    return [
        Resource(
            uri="note://list",
            name="All Notes",
            description="List all saved notes",
            mimeType="application/json",
        ),
        Resource(
            uri="action-item://list",
            name="All Action Items",
            description="List all action items",
            mimeType="application/json",
        ),
    ]


@server.list_tools()
async def handle_list_tools() -> List[Tool]:
    """List available tools."""
    return [
        Tool(
            name="extract_action_items",
            description="Extract action items from text using heuristics or LLM",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "Text to extract action items from",
                    },
                    "use_llm": {
                        "type": "boolean",
                        "description": "Whether to use LLM for extraction (default: false)",
                        "default": False,
                    },
                    "save_note": {
                        "type": "boolean",
                        "description": "Whether to save the text as a note (default: false)",
                        "default": False,
                    },
                },
                "required": ["text"],
            },
        ),
        Tool(
            name="list_notes",
            description="List all saved notes",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        Tool(
            name="list_action_items",
            description="List action items with optional filtering",
            inputSchema={
                "type": "object",
                "properties": {
                    "note_id": {
                        "type": "integer",
                        "description": "Optional note ID to filter action items",
                    },
                    "done": {
                        "type": "boolean",
                        "description": "Optional done status to filter action items",
                    },
                },
            },
        ),
        Tool(
            name="create_note",
            description="Create a new note",
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "description": "Content of the note",
                    },
                },
                "required": ["content"],
            },
        ),
    ]


@server.call_tool()
async def handle_call_tool(
    name: str, arguments: Dict[str, Any] | None
) -> List[TextContent | ImageContent | EmbeddedResource]:
    """Handle tool calls."""
    try:
        if name == "extract_action_items":
            text = arguments.get("text", "") if arguments else ""
            use_llm = arguments.get("use_llm", False) if arguments else False
            save_note = arguments.get("save_note", False) if arguments else False

            logger.info(f"Extracting action items (LLM: {use_llm})")

            # Call the extract endpoint
            endpoint = "/action-items/extract-llm" if use_llm else "/action-items/extract"

            response = await client.post(endpoint, json={"text": text, "save_note": save_note})

            if response.status_code != 200:
                raise Exception(f"API error: {response.status_code} - {response.text}")

            data = response.json()

            # Format the result
            result = {
                "note_id": data.get("note_id"),
                "items": data.get("items", []),
                "count": len(data.get("items", [])),
            }

            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        elif name == "list_notes":
            logger.info("Listing all notes")

            response = await client.get("/notes")

            if response.status_code != 200:
                raise Exception(f"API error: {response.status_code} - {response.text}")

            data = response.json()

            return [TextContent(type="text", text=json.dumps(data, indent=2))]

        elif name == "list_action_items":
            note_id = arguments.get("note_id") if arguments else None
            done = arguments.get("done") if arguments else None

            logger.info(f"Listing action items (note_id: {note_id}, done: {done})")

            # Build query parameters
            params = {}
            if note_id is not None:
                params["note_id"] = note_id

            response = await client.get("/action-items", params=params)

            if response.status_code != 200:
                raise Exception(f"API error: {response.status_code} - {response.text}")

            data = response.json()

            # Filter by done status if specified
            if done is not None:
                data = [item for item in data if item.get("done") == done]

            return [TextContent(type="text", text=json.dumps(data, indent=2))]

        elif name == "create_note":
            content = arguments.get("content", "") if arguments else ""

            logger.info("Creating new note")

            response = await client.post("/notes", json={"content": content})

            if response.status_code != 201:
                raise Exception(f"API error: {response.status_code} - {response.text}")

            data = response.json()

            return [TextContent(type="text", text=json.dumps(data, indent=2))]

        else:
            raise ValueError(f"Unknown tool: {name}")

    except Exception as e:
        error_msg = f"Error: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return [TextContent(type="text", text=error_msg)]


async def main():
    """Main entry point."""
    try:
        # Test API connection
        logger.info(f"Testing connection to {API_BASE_URL}")
        async with httpx.AsyncClient() as test_client:
            response = await test_client.get(f"{API_BASE_URL}/")
            if response.status_code == 200:
                logger.info("Successfully connected to week2 API")
            else:
                logger.warning(f"API test returned status {response.status_code}")
    except Exception as e:
        logger.error(f"Failed to connect to API at {API_BASE_URL}: {e}")
        logger.error("Please ensure week2 API is running on localhost:8000")
        return

    # Run MCP server
    async with stdio_server() as (read_stream, write_stream):
        init_options = InitializationOptions(
            server_name="note-action-server",
            server_version="0.1.0",
            capabilities=server.get_capabilities(
                notification_options=NotificationOptions(),
                experimental_capabilities={},
            ),
        )

        await server.run(
            read_stream,
            write_stream,
            init_options,
            raise_exceptions=True,
        )


if __name__ == "__main__":
    asyncio.run(main())
