## 1) ✅ Enable pre-commit and fix the repo **[COMPLETED]**
- ✅ Install hooks: `pre-commit install`
- ✅ Run: `pre-commit run --all-files`
- ✅ Fix any formatting/lint issues (black/ruff)

### How completed:
- Used command: `/pre-commit-all` to run pre-commit hooks
- Used command: `/format-lint` to fix formatting and linting issues
- Verified: `pre-commit run --files backend/**/*.py` → All checks passed
- Note: Project-wide pre-commit checks still show errors in other week directories (week1, week2, week3-2, week6), but week4-1 directory is clean

```
  步骤 3: 运行所有预提交检查

  使用命令：/pre-commit-all
  （这会运行 pre-commit run --all-files）

  步骤 4: 如果有格式化/lint问题

  使用命令：/format-lint
  （这会运行 make format 和 make lint）

  步骤 5: 重复步骤 3-4 直到通过

  确保所有检查都通过后，任务完成。
```

## 2) Add search endpoint for notes
- Add/extend `GET /notes/search?q=...` (case-insensitive) using SQLAlchemy filters
- Update `frontend/app.js` to use the search query
- Add tests in `backend/tests/test_notes.py`

---
现在完成第二个task，先做一个计划，让我知道你想怎么做。在计划中要先加上任务的需求, 尽量使用command和subagent，如果用subagent，要按照docs里面的AGENT_WORKFLOW.md, 要尽量使用已经存在的command。

现在按照我们align的计划执行，将中间步骤都显示出来

---


● 任务 2 完成计划（更新版 - 包含现有命令）

  ---
  📋 任务需求

  根据 docs/TASKS.md：

  任务： Add search endpoint for notes

  具体要求：
  1. 后端 API：
    - Add/extend GET /notes/search?q=...
    - 使用 SQLAlchemy filters 实现
    - Case-insensitive 搜索（不区分大小写）
  2. 前端：
    - Update frontend/app.js to use the search query
    - 添加搜索 UI（输入框 + 按钮）
  3. 测试：
    - Add tests in backend/tests/test_notes.py
    - 验证 case-insensitive 功能

  ---
  🔍 当前状态分析

  已存在：
  - ✅ 搜索端点：GET /notes/search/?q=... (backend/app/routers/notes.py:27-37)
  - ✅ 基础测试：test_create_and_list_notes 中有简单搜索测试

  问题：
  - ❌ 当前实现使用 contains()，可能不是 case-insensitive
  - ❌ 前端没有搜索 UI
  - ❌ 测试覆盖不足（没有 case-insensitive 测试）

  ---
  🎯 执行计划（使用 Agent Workflows + 现有命令）

  根据 AGENT_WORKFLOWS.md - Workflow 1: Feature Addition

  流程：
  User (spec) → TestAgent → CodeAgent → TestAgent → CodeAgent → DocsAgent
                    ↓            ↓           ↓           ↓            ↓
                Write tests   Implement   Verify     Frontend     Update docs
                    ↑            ↑                      ↑            ↑
                /tests      /format-lint            /format-lint  /docs-sync

  Step 1: TestAgent - 编写/扩展测试

  任务： 添加 case-insensitive 搜索测试

  步骤：
  1. 读取现有的 backend/tests/test_notes.py
  2. 添加测试用例：
    - test_search_case_insensitive_title - 大写搜索小写标题
    - test_search_case_insensitive_content - 小写搜索大写内容
    - test_search_case_insensitive_mixed - 混合大小写
  3. 运行测试：使用命令 /tests
  4. 观察测试结果（预期：部分失败，因为后端还没有更新）
  5. 返回测试文件路径给 CodeAgent

  Step 2: CodeAgent - 实现后端功能

  任务： 确保 case-insensitive 搜索

  步骤：
  1. 读取测试以了解需求
  2. 检查现有搜索实现（backend/app/routers/notes.py:27-37）
  3. 将 Note.title.contains(q) 和 Note.content.contains(q)
  改为 Note.title.ilike(q) 和 Note.content.ilike(q)
  （ilike() 是 SQLAlchemy 的 case-insensitive LIKE 方法）
  4. 运行格式化和 lint：使用命令 /format-lint
  5. 运行测试：使用命令 /tests
  6. 返回状态给 TestAgent

  Step 3: TestAgent - 验证后端实现

  任务： 确保所有测试通过

  步骤：
  1. 运行测试：使用命令 /tests
  2. 确保新增的 case-insensitive 测试通过
  3. 检查覆盖率：使用命令 /coverage-report
  4. 返回最终状态

  Step 4: CodeAgent - 更新前端

  任务： 添加搜索 UI

  步骤：
  1. 读取 frontend/app.js
  2. 读取 frontend/index.html 查看现有 UI 结构
  3. 在 HTML 中添加搜索输入框和搜索按钮
  4. 在 app.js 中添加搜索函数：
    - 获取搜索输入值
    - 调用 GET /notes/search/?q=...
    - 显示搜索结果
  5. 运行格式化和 lint：使用命令 /format-lint（针对 Python 文件）
  6. 测试前端功能（手动验证或启动服务器）
  7. 返回状态

  Step 5: DocsAgent - 更新文档

  任务： 同步文档

  步骤：
  1. 运行文档同步：使用命令 /docs-sync
  2. 这将自动：
    - 获取 OpenAPI spec
    - 更新 docs/API.md
    - 同步文档
  3. 手动更新 docs/TASKS.md 标记任务 2 为完成
  4. 添加完成方法说明（包括使用的命令）
  5. 报告更改

  ---
  🛠️  使用的现有命令

  ┌────────┬──────────────────┬──────────────────────┐
  │  步骤  │       命令       │         用途         │
  ├────────┼──────────────────┼──────────────────────┤
  │ Step 1 │ /tests           │ 运行测试验证当前状态 │
  ├────────┼──────────────────┼──────────────────────┤
  │ Step 2 │ /format-lint     │ 格式化和 lint 代码   │
  ├────────┼──────────────────┼──────────────────────┤
  │ Step 2 │ /tests           │ 验证后端实现         │
  ├────────┼──────────────────┼──────────────────────┤
  │ Step 3 │ /tests           │ 验证所有测试通过     │
  ├────────┼──────────────────┼──────────────────────┤
  │ Step 3 │ /coverage-report │ 检查测试覆盖率       │
  ├────────┼──────────────────┼──────────────────────┤
  │ Step 4 │ /format-lint     │ 格式化和 lint 代码   │
  ├────────┼──────────────────┼──────────────────────┤
  │ Step 5 │ /docs-sync       │ 同步文档             │
  └────────┴──────────────────┴──────────────────────┘

  ---
  ✅ 验收标准

  1. 后端搜索支持 case-insensitive
  2. 前端有搜索 UI（输入框 + 按钮）
  3. 前端可以调用搜索 API
  4. 所有测试通过（使用 /tests 验证）
  5. 覆盖率充足（使用 /coverage-report 验证）
  6. 文档更新完成（使用 /docs-sync 同步）
 ---


## 3) Complete action item flow
- Implement `PUT /action-items/{id}/complete` (already scaffolded)
- Update UI to reflect completion (already wired) and extend test coverage

---
现在完成第3个task，先做一个计划，让我知道你想怎么做。在计划中要先加上任务的需求, 尽量使用command和subagent，如果用subagent，要按照docs里面的AGENT_WORKFLOW.md, 要尽量使用已经存在的command。

现在按照我们align的计划执行，将中间步骤都显示出来

---

● 任务 3 完成计划（包含需求）

  ---
  📋 任务需求

  根据 docs/TASKS.md：

  任务： Complete action item flow

  具体要求：
  1. 后端 API：
    - Implement PUT /action-items/{id}/complete (already scaffolded)
  2. 前端：
    - Update UI to reflect completion (already wired)
  3. 测试：
    - Extend test coverage

  ---
  🔍 当前状态分析

  后端：
  - ✅ PUT /action-items/{id}/complete 端点已实现 (backend/app/routers/action_items.py:27-36)
  - ✅ 包含 404 错误处理

  前端：
  - ✅ UI 已经有 completion 按钮 (frontend/app.js:36-43)
  - ✅ 点击按钮调用 PUT /action-items/{id}/complete
  - ✅ 完成后重新加载列表

  测试：
  - ✅ 基础测试存在：test_create_and_complete_action_item
  - ✅ 测试通过
  - ⚠️  覆盖率 96%，缺少 404 错误路径的测试

  覆盖率报告：
  backend/app/routers/action_items.py: 96% coverage
  Missing: line 31 (404 error handling)

  ---
  🎯 执行计划（使用 Agent Workflows + 现有命令）

  根据 AGENT_WORKFLOWS.md - Workflow 1: Feature Addition（扩展测试）

  流程：
  User (spec) → TestAgent → CodeAgent → TestAgent → DocsAgent
                    ↓            ↓           ↓            ↓
                Write tests   Verify     Verify     Update docs
                                coverage
                    ↑            ↑           ↑            ↑
                /tests      /format-lint /coverage-report /docs-sync

  Step 1: TestAgent - 扩展测试

  任务： 添加测试以覆盖 404 错误路径

  步骤：
  1. 读取现有的 backend/tests/test_action_items.py
  2. 读取当前的 action items router: backend/app/routers/action_items.py
  3. 添加测试用例：
    - test_complete_action_item_not_found - 测试不存在的 action item ID 应该返回 404
  4. 运行测试：使用命令 /tests
  5. 检查覆盖率：使用命令 /coverage-report
  6. 报告结果

  Step 2: CodeAgent - 验证后端实现

  任务： 验证后端端点实现正确

  步骤：
  1. 读取 backend/app/routers/action_items.py
  2. 验证 PUT /action-items/{id}/complete 端点实现
  3. 验证 404 错误处理正确
  4. 运行格式化和 lint：使用命令 /format-lint
  5. 运行测试：使用命令 /tests
  6. 报告结果

  Step 3: TestAgent - 验证测试覆盖率

  任务： 确保测试覆盖率充足

  步骤：
  1. 运行测试：使用命令 /tests
  2. 检查覆盖率：使用命令 /coverage-report
  3. 验证 action_items.py 覆盖率达到 100%
  4. 报告最终状态

  Step 4: DocsAgent - 更新文档

  任务： 同步文档

  步骤：
  1. 运行文档同步：使用命令 /docs-sync
  2. 检查 API.md 是否已经包含 complete 端点文档
  3. 手动更新 docs/TASKS.md 标记任务 3 为完成
  4. 添加完成方法说明（包括使用的命令）
  5. 报告更改

  ---
  🛠️  使用的现有命令

  ┌────────┬──────────────────┬────────────────────┐
  │  步骤  │       命令       │        用途        │
  ├────────┼──────────────────┼────────────────────┤
  │ Step 1 │ /tests           │ 运行测试验证新测试 │
  ├────────┼──────────────────┼────────────────────┤
  │ Step 1 │ /coverage-report │ 检查测试覆盖率     │
  ├────────┼──────────────────┼────────────────────┤
  │ Step 2 │ /format-lint     │ 格式化和 lint 代码 │
  ├────────┼──────────────────┼────────────────────┤
  │ Step 2 │ /tests           │ 验证后端实现       │
  ├────────┼──────────────────┼────────────────────┤
  │ Step 3 │ /tests           │ 验证所有测试通过   │
  ├────────┼──────────────────┼────────────────────┤
  │ Step 3 │ /coverage-report │ 检查最终覆盖率     │
  ├────────┼──────────────────┼────────────────────┤
  │ Step 4 │ /docs-sync       │ 同步文档           │
  └────────┴──────────────────┴────────────────────┘

  ---
  ✅ 验收标准

  1. 后端 PUT /action-items/{id}/complete 端点正确实现
  2. 前端 UI 正确显示 completion 状态
  3. 所有测试通过（使用 /tests 验证）
  4. action_items.py 覆盖率达到 100%（使用 /coverage-report 验证）
  5. 文档更新完成（使用 /docs-sync 同步）

  ---


## 4) Improve extraction logic
- Extend `backend/app/services/extract.py` to parse tags like `#tag` and return them
- Add tests for the new parsing behavior
- (Optional) Expose `POST /notes/{id}/extract` that turns notes into action items

## 5) Notes CRUD enhancements
- Add `PUT /notes/{id}` to edit a note (title/content)
- Add `DELETE /notes/{id}` to delete a note
- Update `frontend/app.js` to support edit/delete; add tests

## 6) Request validation and error handling
- Add simple validation rules (e.g., min lengths) to `schemas.py`
- Return informative 400/404 errors where appropriate; add tests for validation failures

## 7) Docs drift check (manual for now)
- Create/maintain a simple `API.md` describing endpoints and payloads
- After each change, verify docs match actual OpenAPI (`/openapi.json`)
