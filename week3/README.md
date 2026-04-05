# Note Action MCP Server

基于week2 API（运行在localhost:8000）的MCP (Model Context Protocol) Server，用于笔记管理和行动项提取。

## 功能

这个MCP server暴露了4个工具：

1. **`extract_action_items`** - 从文本中提取行动项
   - 支持使用启发式算法或LLM进行提取
   - 可选择是否将文本保存为笔记
   
2. **`list_notes`** - 列出所有保存的笔记
   - 显示笔记ID、内容和创建时间
   
3. **`list_action_items`** - 列出行动项（支持过滤）
   - 可按笔记ID过滤
   - 可按完成状态过滤
   
4. **`create_note`** - 创建新笔记
   - 直接创建包含指定内容的笔记

## 前提条件

- week2的API必须在localhost:8000运行
- Python 3.8+

## 安装

1. 进入week3-2目录：
```bash
cd week3-2
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

## 运行

```bash
python main.py
```

或者使用mcp-inspector进行测试：
```bash
mcp-inspector python main.py
```

## 使用示例

### 提取行动项
```json
{
  "name": "extract_action_items",
  "arguments": {
    "text": "今天需要完成以下任务：\n- 完成项目报告\n- 回复客户邮件\n- 准备明天的会议",
    "use_llm": false,
    "save_note": true
  }
}
```

### 列出所有笔记
```json
{
  "name": "list_notes",
  "arguments": {}
}
```

### 列出行动项
```json
{
  "name": "list_action_items",
  "arguments": {
    "note_id": 1,
    "done": false
  }
}
```

### 创建笔记
```json
{
  "name": "create_note",
  "arguments": {
    "content": "这是一个新的笔记内容"
  }
}
```

## Claude Code配置

$ claude mcp add action-item-extractor -- python /home/ericwang/workspace/AI_Coding/College_Application_03.08/modern-software-dev-assignments/week3/main.py
Added stdio MCP server action-item-extractor with command: python /home/ericwang/workspace/AI_Coding/College_Application_03.08/modern-software-dev-assignments/week3/main.py to local config
File modified: /home/ericwang/.claude.json [project: /home/ericwang/workspace/AI_Coding/College_Application_03.08]

$ claude mcp list

❯ /mcp
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
  Manage MCP servers
  2 servers

    Local MCPs (/home/ericwang/.claude.json [project: /home/ericwang/workspace/AI_Coding/College_Application_03.08])
  ❯ action-item-extractor · ✔ connected


$ Claude mcp list

$ vi /home/ericwang/.claude.json

```json
    "/home/ericwang/workspace/AI_Coding/College_Application_03.08": {
      "allowedTools": [],
      "mcpContextUris": [],
      "mcpServers": {
        "action-item-extractor": {
          "type": "stdio",
          "command": "python",
          "args": [
            "/home/ericwang/workspace/AI_Coding/College_Application_03.08/modern-software-dev-assignments/week3/main.py"
          ],
          "env": {}
        }
      },
```


**注意**：将路径替换为你实际的week3/main.py文件路径。

配置完成后，在Claude中可以直接说：
- "请帮我提取这段文本中的行动项"
- "列出我所有的笔记"
- "显示所有未完成的任务"
- "创建一个新笔记"

例子

❯ 请从下面的会议纪要中提取出action items
这个是后面要做的内容来运行测试脚本验证server功能：
# 验证与week2 API的连接
# 运行功能测试
# 快速测试所有功能


● Let me add these action items using the MCP server:

● action-item-extractor - extract_action_items (MCP)(text: "这个是后面要做的内容来运行测试脚本验证server功能：\n\n#
                                                    验证与week2 API的连接\n# 运行功能测试\n# 快速测试所有功能",
                                                    save_note: true)

● The automatic extraction didn't pick up these items. Let me create them as explicit action items:

● action-item-extractor - create_note (MCP)(content: "Meeting Notes - Testing
                                           Tasks\n\n这个是后面要做的内容来运行测试脚本验证server功能：\n1. 验证与week2
                                           API的连接\n2. 运行功能测试\n3. 快速测试所有功能")

● action-item-extractor - extract_action_items (MCP)(save_note: true, text:
                                                    "这个是后面要做的内容来运行测试脚本验证server功能：\n1. 验证与week2
                                                    API的连接\n2. 运行功能测试\n3. 快速测试所有功能", use_llm: true)

● Action items extracted successfully using LLM! Here's what was extracted:

● action-item-extractor - list_action_items (MCP)

● Successfully extracted 3 action items from your meeting notes:

  ┌─────┬───────────────────────┬────────────┐
  │ ID  │      Action Item      │   Status   │
  ├─────┼───────────────────────┼────────────┤
  │ 63  │ 验证与week2 API的连接 │ ⏳ Pending │
  ├─────┼───────────────────────┼────────────┤
  │ 64  │ 运行功能测试          │ ⏳ Pending │
  ├─────┼───────────────────────┼────────────┤
  │ 65  │ 快速测试所有功能      │ ⏳ Pending │
  └─────┴───────────────────────┴────────────┘

  The action-item-extractor MCP server is working correctly. These items are now tracked and ready for you to mark as
  complete when you finish each testing task.



## 工作原理

这个MCP server通过HTTP请求与运行中的week2 API通信：
- 所有工具调用都会转换为对应的API端点调用
- 数据在MCP server和week2 API之间传递
- 保持了week2的所有业务逻辑和数据完整性

## 故障排除

### 连接问题
如果MCP server无法连接：
1. 确保week2 API正在运行：
   ```bash
   python verify_connection.py
   ```
2. 检查Claude Desktop日志：
   - macOS: `~/Library/Logs/Claude/`
   - Windows: `%APPDATA%\Claude\Logs\`
   - Linux: `~/.config/Claude/logs/`

### 路径问题
在Windows上，确保使用正确的路径格式：
```json
"args": ["C:\\path\\to\\week3-2\\main.py"]
```

## 测试

运行测试脚本验证server功能：
```bash
# 验证与week2 API的连接
python verify_connection.py

# 运行功能测试
python test_mcp.py

# 快速测试所有功能
python quick_test.py
```