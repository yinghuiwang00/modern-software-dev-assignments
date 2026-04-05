#!/usr/bin/env python3
"""Quick test of MCP server functionality."""

import asyncio
import json

from main import handle_call_tool


async def test_all_tools():
    """Test all MCP tools."""
    print("🧪 Testing MCP Server Tools")
    print("=" * 50)

    # Test 1: Create a note
    print("\n1. Creating a test note...")
    result = await handle_call_tool(
        "create_note",
        {
            "content": "这是一个MCP server测试笔记\n包含多个行动项：\n- 完成代码审查\n- 更新文档\n- 准备发布"
        },
    )

    if result and result[0].text:
        data = json.loads(result[0].text)
        note_id = data.get("id")
        print(f"✅ Created note with ID: {note_id}")
    else:
        print("❌ Failed to create note")
        return

    # Test 2: List notes
    print("\n2. Listing all notes...")
    result = await handle_call_tool("list_notes", {})

    if result and result[0].text:
        data = json.loads(result[0].text)
        print(f"✅ Found {len(data)} notes")
    else:
        print("❌ Failed to list notes")

    # Test 3: Extract action items
    print("\n3. Extracting action items...")
    result = await handle_call_tool(
        "extract_action_items",
        {
            "text": "今天的任务：\n- 修复bug #123\n- 编写测试用例\n- 部署到生产环境",
            "use_llm": False,
            "save_note": True,
        },
    )

    if result and result[0].text:
        data = json.loads(result[0].text)
        print(f"✅ Extracted {data.get('count', 0)} action items")
        if data.get("items"):
            for item in data["items"]:
                print(f"  - {item['text']}")
    else:
        print("❌ Failed to extract action items")

    # Test 4: List action items
    print("\n4. Listing action items...")
    result = await handle_call_tool("list_action_items", {})

    if result and result[0].text:
        data = json.loads(result[0].text)
        print(f"✅ Found {len(data)} action items")
        if data:
            for item in data[:3]:  # Show first 3
                status = "✓" if item.get("done") else "○"
                print(f"  {status} {item['text']}")
    else:
        print("❌ Failed to list action items")

    print("\n" + "=" * 50)
    print("✅ All tests completed!")


if __name__ == "__main__":
    asyncio.run(test_all_tools())
