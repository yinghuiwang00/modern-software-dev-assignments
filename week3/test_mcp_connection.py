#!/usr/bin/env python3
"""
测试 MCP server 的正确初始化流程
"""
import asyncio
import json
import sys


async def test_mcp_server():
    """测试 MCP server 的初始化流程"""
    process = await asyncio.create_subprocess_exec(
        sys.executable,
        "/home/ericwang/workspace/AI_Coding/College_Application_03.08/modern-software-dev-assignments/week3/simple_mcp_test.py",
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    print("MCP Server 进程已启动")

    # 发送初始化请求
    init_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "test-client", "version": "1.0.0"},
        },
    }

    print("发送初始化请求...")
    process.stdin.write(json.dumps(init_request).encode())
    process.stdin.write(b"\n")
    await process.stdin.drain()

    # 等待响应
    try:
        response = await asyncio.wait_for(process.stdout.readline(), timeout=5.0)
        if response:
            response_data = json.loads(response.decode())
            print(f"收到响应: {json.dumps(response_data, indent=2)}")
        else:
            print("没有收到响应")
    except asyncio.TimeoutError:
        print("等待响应超时")

    # 发送 initialized 通知
    initialized = {"jsonrpc": "2.0", "method": "notifications/initialized"}

    print("发送 initialized 通知...")
    process.stdin.write(json.dumps(initialized).encode())
    process.stdin.write(b"\n")
    await process.stdin.drain()

    # 现在可以发送其他请求了
    tools_list_request = {"jsonrpc": "2.0", "id": 2, "method": "tools/list"}

    print("发送 tools/list 请求...")
    process.stdin.write(json.dumps(tools_list_request).encode())
    process.stdin.write(b"\n")
    await process.stdin.drain()

    try:
        response = await asyncio.wait_for(process.stdout.readline(), timeout=5.0)
        if response:
            response_data = json.loads(response.decode())
            print(f"收到工具列表: {json.dumps(response_data, indent=2)}")
        else:
            print("没有收到响应")
    except asyncio.TimeoutError:
        print("等待响应超时")

    # 清理
    process.terminate()
    await process.wait()


if __name__ == "__main__":
    asyncio.run(test_mcp_server())
