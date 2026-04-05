#!/usr/bin/env python3
"""
简单的 MCP server 测试
这个 server 不依赖外部 API，只返回固定的数据
"""
import asyncio
import logging

from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

server = Server("simple-test-server")


@server.list_tools()
async def list_tools() -> list[Tool]:
    """返回一个简单的测试工具"""
    return [
        Tool(
            name="test_tool",
            description="简单的测试工具",
            inputSchema={
                "type": "object",
                "properties": {"message": {"type": "string", "description": "测试消息"}},
            },
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict | None) -> list[TextContent]:
    """处理工具调用"""
    if name == "test_tool":
        message = (
            arguments.get("message", "Hello from simple MCP server!")
            if arguments
            else "Hello from simple MCP server!"
        )
        return [TextContent(type="text", text=f"测试成功: {message}")]
    raise ValueError(f"Unknown tool: {name}")


async def main():
    """主函数"""
    logger.info("Simple MCP Server 启动中...")

    async with stdio_server() as (read_stream, write_stream):
        init_options = InitializationOptions(
            server_name="simple-test-server",
            server_version="1.0.0",
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
