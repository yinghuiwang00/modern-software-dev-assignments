# Week 4 Implementation Plan

## Assignment Overview

Build **2+ automations** using Claude Code features to improve the developer workflow for the starter application, then use these automations to enhance the app.

## Phase 1: Explore & Setup CLAUDE.md

### Task 1.1: Explore Starter Application
- **Run the application**: `make run`
- **Access**:
  - Frontend: http://localhost:8000
  - API Docs: http://localhost:8000/docs
  - OpenAPI spec: http://localhost:8000/openapi.json
- **Review codebase structure**:
  - `backend/app/` - FastAPI application
    - `routers/` - API endpoints (notes, action_items)
    - `models.py` - SQLAlchemy models
    - `schemas.py` - Pydantic schemas
    - `services/extract.py` - Action item extraction logic
  - `frontend/` - Static UI (app.js, index.html, styles.css)
  - `docs/TASKS.md` - Development tasks
  - `data/seed.sql` - Database seed data

### Task 1.2: Create CLAUDE.md in week4/
Create `week4/CLAUDE.md` with repository guidance:

**Required sections:**

1. **Code Navigation and Entry Points**
   - How to run the app: `make run`
   - Where routers live: `backend/app/routers/`
   - Where tests live: `backend/tests/`
   - Where models live: `backend/app/models.py`
   - How DB is seeded: `backend/app/db.py` + `data/seed.sql`

2. **Style and Safety Guardrails**
   - Tooling expectations: black, ruff, pytest
   - Safe commands to run: `make test`, `make format`, `make lint`, `make run`
   - Commands to avoid: destructive DB operations without confirmation
   - Lint/test gates: must pass before commits

3. **Workflow Snippets**
   - "When asked to add an endpoint, first write a failing test, then implement, then run pre-commit."
   - "When modifying models, update schemas and run migrations."
   - "Always run tests before committing."

## Phase 2: Automations Selection

### Automation A: Custom Slash Commands (3+ commands)

Create `.claude/commands/*.md` files in week4/.

**Required Commands (from assignment examples):**

1. **`tests.md` - Test runner with coverage**
   - Intent: Run `pytest -q backend/tests --maxfail=1 -x` and, if green, run coverage
   - Inputs: Optional marker or path via `$ARGUMENTS`
   - Output: Summarize failures and suggest next steps

2. **`docs-sync.md` - Documentation sync**
   - Intent: Read `/openapi.json`, update `docs/API.md`, and list route deltas
   - Output: Diff-like summary and TODOs

3. **`refactor-module.md` - Refactor harness**
   - Intent: Rename a module (e.g., `services/extract.py` → `services/parser.py`), update imports, run lint/tests
   - Output: A checklist of modified files and verification steps

**Additional Commands (optional):**

4. **`format-lint.md` - Code formatting and linting**
   - Intent: Run `make format` and `make lint` in sequence
   - Output: List of files formatted and any lint errors

5. **`db-reset.md` - Database reset**
   - Intent: Drop and recreate database, reseed from `data/seed.sql`
   - Output: Confirmation of reset and seed status

6. **`coverage-report.md` - Coverage detailed report**
   - Intent: Run pytest with coverage and generate HTML report
   - Output: Coverage percentage and HTML report location

7. **`pre-commit-all.md` - Run pre-commit on all files**
   - Intent: Run `pre-commit run --all-files` and summarize results
   - Output: List of hooks run and any failures

### Automation B: SubAgents (5 agents)

Create `.claude/agents/` directory in week4/ with specialized agents.

**Required Agents:**

1. **TestAgent**
   - Purpose: Write and update tests for changes
   - Responsibilities:
     - Write failing tests for new features
     - Update tests when APIs change
     - Verify tests pass after implementation
   - Tools: Read, Write, Bash (pytest)
   - Workflow: Receive feature spec → Write tests → Return test file path

2. **CodeAgent**
   - Purpose: Implement code to pass tests
   - Responsibilities:
     - Implement API routes and endpoints
     - Write model and schema definitions
     - Fix failing tests
   - Tools: Read, Write, Edit, Bash (pytest, make)
   - Workflow: Receive test file → Implement code → Run tests → Return status

3. **DocsAgent**
   - Purpose: Keep documentation in sync with code
   - Responsibilities:
     - Update `docs/API.md` from OpenAPI spec
     - Update `docs/TASKS.md` with completed items
     - Check documentation drift
   - Tools: Read, Write, Edit, mcp__plugin_chrome-devtools-mcp_* (for OpenAPI)
   - Workflow: Receive code changes → Update docs → Verify sync

4. **DBAgent**
   - Purpose: Handle database schema and data changes
   - Responsibilities:
     - Propose schema changes (update models)
     - Update `data/seed.sql`
     - Create migration scripts if needed
   - Tools: Read, Write, Edit, Bash (sqlite3)
   - Workflow: Receive schema change → Update model + seed → Return SQL diff

5. **RefactorAgent**
   - Purpose: Handle code refactoring and cleanup
   - Responsibilities:
     - Rename modules/files
     - Update imports across codebase
     - Run lint and fix issues
     - Verify tests still pass
   - Tools: Read, Write, Edit, Glob, Grep, Bash (make lint, make test)
   - Workflow: Receive refactor request → Plan changes → Execute → Verify

**Agent Workflows:**

**Workflow 1: Feature Addition**
```
Spec (user) → TestAgent → CodeAgent → TestAgent → DocsAgent
           ↓            ↓           ↓
        Write tests   Implement   Verify    Update docs
```

**Workflow 2: Documentation Sync**
```
CodeAgent → DocsAgent → TestAgent
   ↓           ↓          ↓
New route   Update API   Verify docs
```

**Workflow 3: Database Schema Change**
```
DBAgent → RefactorAgent → CodeAgent → TestAgent
   ↓           ↓            ↓           ↓
Schema    Update code    Fix routes   Verify
```

## Phase 3: Implementation

### Task 3.1: Implement Slash Commands (3+)

**Step 1:** Create directory structure
```bash
mkdir -p week4/.claude/commands
```

**Step 2:** Implement required commands
1. Create `tests.md`
2. Create `docs-sync.md`
3. Create `refactor-module.md`

**Step 3:** Implement additional commands (choose 1+)
4. Create `format-lint.md`
5. Create `db-reset.md`
6. Create `coverage-report.md`
7. Create `pre-commit-all.md`

**Step 4:** Test each command
- Run `/tests` - verify test output and coverage
- Run `/docs-sync` - verify API.md update
- Run `/refactor-module services/extract.py services/parser.py` - verify refactoring
- Test additional commands

**Step 5:** Refine based on usage
- Add error handling
- Improve output formatting
- Add safety checks

### Task 3.2: Implement SubAgents (5)

**Step 1:** Create directory structure
```bash
mkdir -p week4/.claude/agents
```

**Step 2:** Implement each agent
1. Create `test-agent.md` - TestAgent configuration
2. Create `code-agent.md` - CodeAgent configuration
3. Create `docs-agent.md` - DocsAgent configuration
4. Create `db-agent.md` - DBAgent configuration
5. Create `refactor-agent.md` - RefactorAgent configuration

**Step 3:** Create workflow scripts/documentation
- Document agent workflows in `docs/AGENT_WORKFLOWS.md`
- Include example usage for each workflow
- Include safety notes and rollback procedures

**Step 4:** Test agent workflows
- Test Workflow 1 (Feature Addition) with a simple TASKS.md item
- Test Workflow 2 (Documentation Sync) after adding a route
- Test Workflow 3 (Database Change) for a model update

**Step 5:** Iterate and refine
- Adjust agent prompts for better results
- Add more specific tool constraints
- Improve agent coordination

### Task 3.3: Document Part I of writeup.md
For each automation, fill in:
- **a. Design inspiration** - Cite assignment requirements (section A, B, C)
- **b. Design** - Goals, inputs/outputs, steps
- **c. How to run** - Exact commands, expected outputs, safety notes
- **d. Before vs. after** - Manual workflow vs. automated workflow

**Part I Deliverables:**
- For Slash Commands: Document all 3+ commands implemented
- For SubAgents: Document all 5 agents and their workflows

## Phase 4: Put Automations to Work (Part II)

### Task 4.1: Use Slash Commands on TASKS.md
Pick 2-3 items from `docs/TASKS.md` and complete using slash commands:

**Example:** Task #2 - Add search endpoint for notes
1. Use `/tests` to run existing tests
2. Implement `GET /notes/search?q=...`
3. Use `/tests` to verify new tests pass
4. Use `/docs-sync` to update API.md
5. Document the workflow and efficiency gains

**Example:** Task #5 - Notes CRUD enhancements
1. Use `/refactor-module` if needed
2. Implement `PUT /notes/{id}` and `DELETE /notes/{id}`
3. Use `/tests` to verify
4. Use `/docs-sync` to update docs
5. Use `/format-lint` to clean up code

### Task 4.2: Use SubAgents on TASKS.md
Pick 1-2 items and complete using subagent workflows:

**Example:** Task #3 - Complete action item flow
1. **TestAgent**: Write tests for `PUT /action-items/{id}/complete`
2. **CodeAgent**: Implement the endpoint
3. **TestAgent**: Verify tests pass
4. **DocsAgent**: Update documentation
5. Document workflow and efficiency gains

**Example:** Task #4 - Improve extraction logic
1. **DBAgent**: No schema change needed
2. **CodeAgent**: Extend `services/extract.py` to parse `#tag`
3. **TestAgent**: Write tests for new parsing
4. **DocsAgent**: Update docs if needed
5. Document workflow and efficiency gains

### Task 4.3: Document Part II of writeup.md
For each automation, fill in:
- **e. How you used the automation to enhance the starter application**
  - Which TASKS.md item(s) you completed
  - Specific commands/agents used
  - Efficiency gains (time saved, errors avoided)
  - Any issues encountered and how resolved

## Phase 5: Final Deliverables

### Task 5.1: Complete writeup.md
- Fill all TODOs
- Add submission details (Name, SUNet ID, Citations, Hours)
- Review for completeness
- Ensure Part I and Part II are fully documented

### Task 5.2: Verify Everything Works
- Run `make test` - all tests pass
- Run `make format` and `make lint` - no issues
- Run `make run` - app works correctly
- Test all slash commands
- Test all subagent workflows
- Verify CLAUDE.md is present in week4/

### Task 5.3: Final Check
- Verify `.claude/commands/*.md` files exist (3+)
- Verify `.claude/agents/*.md` files exist (5+)
- Verify `week4/CLAUDE.md` exists
- Verify `docs/API.md` exists (created by docs-sync)
- Verify all TASKS.md items attempted are working

### Task 5.4: Submit
- Push all changes to remote
- Add brentju and febielin as collaborators on repo
- Submit via Gradescope

## Safety & Rollback Notes

### For Slash Commands
- **Idempotency**: Commands should be safe to run multiple times
- **Dry-run**: Add `--dry-run` option for destructive commands (db-reset)
- **Safe tools**: Use Bash tool with safe commands only; avoid destructive operations
- **Validation**: Verify state before making changes (e.g., check if file exists before writing)

### For SubAgents
- **Human in loop**: Always review agent outputs before committing
- **Testing**: Test agents on small, non-critical tasks first
- **Rollback**: Document how to undo changes from each agent
- **Parallel execution**: Be careful with parallel agents that modify same files

### For CLAUDE.md
- **Start conservative**: Begin with basic guidance, iterate
- **No dangerous commands**: Don't include commands that destroy data
- **Document exceptions**: When to deviate from CLAUDE.md guidance

### Git Safety
- Before major operations: `git status` and `git diff`
- Commit frequently for easy rollback
- Use `git reflog` to recover from accidental deletions
- Never use `git reset --hard` without confirmation

## File Structure After Implementation

```
week4/
├── CLAUDE.md                    # Repository guidance
├── .claude/
│   ├── commands/
│   │   ├── tests.md            # Test runner with coverage
│   │   ├── docs-sync.md        # Documentation sync
│   │   ├── refactor-module.md  # Refactor harness
│   │   ├── format-lint.md      # Format and lint
│   │   └── (additional commands...)
│   └── agents/
│       ├── test-agent.md       # TestAgent configuration
│       ├── code-agent.md       # CodeAgent configuration
│       ├── docs-agent.md       # DocsAgent configuration
│       ├── db-agent.md         # DBAgent configuration
│       └── refactor-agent.md   # RefactorAgent configuration
├── docs/
│   ├── TASKS.md                # Existing tasks
│   ├── API.md                  # Generated by docs-sync
│   ├── IMPLEMENTATION_PLAN.md  # This plan
│   └── AGENT_WORKFLOWS.md      # Agent workflow documentation
├── writeup.md                   # Assignment writeup
└── (existing files...)
```

## Timeline Estimate

- **Phase 1**: 30 minutes (explore + create CLAUDE.md)
- **Phase 2**: 30 minutes (planning and design)
- **Phase 3**: 3-5 hours (implement commands + agents + document Part I)
- **Phase 4**: 2-3 hours (use automations on TASKS.md + document Part II)
- **Phase 5**: 30 minutes (verification + submission)

**Total**: 6.5 - 9 hours

## Next Steps

1. ✅ Implementation plan created
2. ⏳ Ready to start Phase 1: Explore application + Create CLAUDE.md
3. ⏳ Then implement 3+ slash commands
4. ⏳ Then implement 5 subagents
5. ⏳ Then use automations on TASKS.md items
6. ⏳ Complete writeup.md and submit
