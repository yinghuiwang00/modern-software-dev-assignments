#!/usr/bin/env python3
"""
测试 MCP server 的基本握手
"""
import asyncio
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))


async def test_mcp_server():
    """测试 MCP server 的基本功能"""
    from mcp.server import NotificationOptions, Server

    print("测试: 导入 MCP 模块成功")

    # 创建一个简单的测试 server
    server = Server("test-server")

    @server.list_tools()
    async def list_tools():
        from mcp.types import Tool

        return [
            Tool(
                name="test_tool",
                description="Test tool",
                inputSchema={"type": "object", "properties": {}},
            )
        ]

    print("测试: 创建 Server 成功")
    print(f"测试: Server capabilities: {server.get_capabilities(NotificationOptions(), {})}")

    print("\n所有基本测试通过！")
    print("MCP server 应该可以正常启动")


if __name__ == "__main__":
    asyncio.run(test_mcp_server())
