# Agent Workflows

This document describes the workflows for using the 5 specialized agents in the week4 assignment.

## Available Agents

| Agent | Purpose | Tools | When to Use |
|-------|---------|-------|-------------|
| **TestAgent** | Write and update tests | Read, Write, Edit, Bash (pytest) | Before implementing features, when APIs change |
| **CodeAgent** | Implement code to pass tests | Read, Write, Edit, Bash (pytest, make) | After TestAgent writes tests, to fix failing tests |
| **DocsAgent** | Keep documentation in sync | Read, Write, Edit, Bash (curl) | After code changes, to update API.md and TASKS.md |
| **DBAgent** | Handle database changes | Read, Write, Edit, Bash (sqlite3) | When schema changes needed, when models updated |
| **RefactorAgent** | Refactor and cleanup code | Read, Write, Edit, Glob, Grep, Bash | When code needs restructuring, renaming files |

## Workflow 1: Feature Addition

Use this workflow when adding a new feature or endpoint to the application.

### Purpose
Add a new feature or fix a bug using Test-Driven Development (TDD) principles.

### Flow
```
User (spec) → TestAgent → CodeAgent → TestAgent → DocsAgent
                  ↓            ↓           ↓
              Write tests   Implement   Verify    Update docs
```

### Step-by-Step

**Step 1: User provides feature specification**
```
User: "Add PUT /notes/{id} endpoint to update a note"
```

**Step 2: TestAgent writes tests**
- Read existing test patterns in `backend/tests/test_notes.py`
- Read schemas in `backend/app/schemas.py`
- Read models in `backend/app/models.py`
- Write failing tests:
  - Test success path (update note)
  - Test error path (note not found)
- Run tests to verify they fail
- Return test file path to CodeAgent

**Step 3: CodeAgent implements feature**
- Read the tests to understand requirements
- Update schemas if needed (add NoteUpdate schema)
- Implement endpoint in `backend/app/routers/notes.py`
- Run tests to verify they pass
- If tests fail, debug and fix implementation
- Return status to TestAgent

**Step 4: TestAgent verifies implementation**
- Re-run all tests
- Ensure coverage is adequate
- If any tests fail, report to CodeAgent
- Return final status

**Step 5: DocsAgent updates documentation**
- Fetch OpenAPI spec from running app
- Update `docs/API.md` with new endpoint
- Update `docs/TASKS.md` to mark task as completed
- Report changes made

### Example: Adding PUT /notes/{id}

**User Request:** "Add PUT /notes/{id} endpoint"

**TestAgent:**
1. Reads existing tests
2. Writes test in `backend/tests/test_notes.py`:
```python
def test_update_note(client):
    # Create a note first
    create_payload = {"title": "Original", "content": "Content"}
    r = client.post("/notes/", json=create_payload)
    note_id = r.json()["id"]

    # Update the note
    update_payload = {"title": "Updated", "content": "New content"}
    r = client.put(f"/notes/{note_id}", json=update_payload)
    assert r.status_code == 200
    data = r.json()
    assert data["title"] == "Updated"

def test_update_note_not_found(client):
    update_payload = {"title": "Updated", "content": "New content"}
    r = client.put("/notes/999", json=update_payload)
    assert r.status_code == 404
```
3. Runs tests, they fail (endpoint doesn't exist)
4. Reports: "Tests written in backend/tests/test_notes.py"

**CodeAgent:**
1. Reads tests to understand requirements
2. Adds NoteUpdate schema to `backend/app/schemas.py`
3. Adds PUT endpoint to `backend/app/routers/notes.py`
4. Runs tests, they pass
5. Reports: "Implementation complete, tests passing"

**TestAgent:**
1. Re-runs all tests
2. Verifies coverage
3. Reports: "All tests passing"

**DocsAgent:**
1. Fetches OpenAPI spec
2. Updates `docs/API.md` with PUT endpoint documentation
3. Marks task in `docs/TASKS.md` as completed
4. Reports: "Documentation updated"

### Safety Notes

- Always run tests before committing
- Use version control: commit before major changes
- Review git diff before committing
- Test edge cases thoroughly
- Ensure error handling is complete

### Rollback Procedure

If the feature breaks something:
```bash
# Revert code changes
git checkout -- backend/app/routers/notes.py
git checkout -- backend/app/schemas.py

# Revert test changes
git checkout -- backend/tests/test_notes.py

# Revert doc changes
git checkout -- docs/API.md
git checkout -- docs/TASKS.md
```

---

## Workflow 2: Documentation Sync

Use this workflow after code changes to ensure documentation stays in sync.

### Purpose
Keep API documentation and task lists accurate after code changes.

### Flow
```
CodeAgent → DocsAgent → TestAgent
   ↓           ↓          ↓
New route   Update API   Verify docs
```

### Step-by-Step

**Step 1: CodeAgent completes code changes**
- Implements new routes or modifies existing ones
- Runs tests to verify
- Reports completion

**Step 2: DocsAgent updates documentation**
- Checks if app is running (start if needed)
- Fetches OpenAPI spec: `curl -s http://localhost:8000/openapi.json`
- Compares with existing `docs/API.md`
- Identifies new, modified, or removed endpoints
- Updates `docs/API.md` with current endpoints
- Updates `docs/TASKS.md` with completed items
- Reports changes made

**Step 3: TestAgent verifies**
- (Optional) Verifies documentation matches actual API behavior
- Checks that examples in docs work
- Reports any discrepancies

### Example: After Adding Search Endpoint

**CodeAgent:**
- Implements `GET /notes/search?q=...` endpoint
- Tests pass
- Reports: "Search endpoint implemented"

**DocsAgent:**
1. Fetches OpenAPI spec
2. Identifies new endpoint: `GET /notes/search/`
3. Updates `docs/API.md`:
```markdown
### GET /notes/search/
Search notes by query string.

**Query Parameters:**
- `q` (optional): Search query string

**Response:** Array of matching notes
```
4. Updates `docs/TASKS.md`: marks task as completed
5. Reports: "Documentation updated with search endpoint"

**TestAgent:**
- (Optional) Verifies search endpoint works as documented
- Reports: "Documentation matches API behavior"

### Safety Notes

- Always verify app is running before fetching OpenAPI spec
- Review changes before committing documentation updates
- Keep examples in docs accurate and up-to-date

---

## Workflow 3: Database Schema Change

Use this workflow when modifying database schema or models.

### Purpose
Handle database schema changes safely with proper migrations and documentation.

### Flow
```
DBAgent → RefactorAgent → CodeAgent → TestAgent
   ↓           ↓            ↓           ↓
Schema    Update code    Fix routes   Verify
```

### Step-by-Step

**Step 1: DBAgent proposes schema change**
- Reads current models in `backend/app/models.py`
- Reads current seed data in `data/seed.sql`
- Proposes schema changes (e.g., add field, create table)
- Updates `backend/app/models.py`
- Updates `data/seed.sql` if needed
- Creates migration SQL if needed
- Returns SQL diff to user

**Step 2: User reviews and approves**
- Reviews proposed changes
- Approves or requests modifications

**Step 3: RefactorAgent updates code**
- Updates Pydantic schemas in `backend/app/schemas.py`
- Updates routers to use new schema
- Updates imports if needed
- Runs linter to fix issues
- Reports changes made

**Step 4: CodeAgent fixes routes**
- Updates routers to handle new schema
- Fixes any broken references
- Runs tests to verify
- Reports status

**Step 5: TestAgent verifies**
- Runs all tests
- Ensures schema changes work correctly
- Reports any issues

### Example: Adding Tags to Notes

**User Request:** "Add a tags field to notes table"

**DBAgent:**
1. Reads current Note model
2. Proposes adding `tags` field
3. Updates `backend/app/models.py`:
```python
class Note(Base):
    __tablename__ = "notes"
    # ... existing fields ...
    tags = Column(String(500), nullable=True)
```
4. Updates `data/seed.sql`:
```sql
INSERT INTO notes (title, content, tags) VALUES
  ('Welcome', '...', 'welcome,todo'),
  ('Demo', '...', 'demo,urgent');
```
5. Returns SQL diff:
```
ALTER TABLE notes ADD COLUMN tags TEXT;
```

**User:** "Approved"

**RefactorAgent:**
1. Updates `backend/app/schemas.py`:
```python
class NoteCreate(BaseModel):
    title: str
    content: str
    tags: str | None = None

class NoteRead(BaseModel):
    id: int
    title: str
    content: str
    tags: str | None = None
```
2. Runs linter
3. Reports: "Schemas updated"

**CodeAgent:**
1. Verifies routers work with new schema
2. No route changes needed (field is nullable)
3. Runs tests
4. Reports: "All tests passing"

**TestAgent:**
1. Runs all tests
2. Verifies tags field works correctly
3. Reports: "Schema change verified"

### Safety Notes

- **Always backup before schema changes**: `cp data/app.db data/app.db.backup`
- Test on development database first
- Use transactions when possible
- Document breaking changes
- Provide rollback SQL

### Rollback Procedure

If schema change causes issues:
```bash
# Restore database backup
cp data/app.db.backup data/app.db

# Or manually rollback
sqlite3 data/app.db
sqlite> ALTER TABLE notes DROP COLUMN tags;
```

### Migration for Existing Databases

If the database already exists:
```bash
# Option 1: Recreate database
rm data/app.db
make seed

# Option 2: Run migration
sqlite3 data/app.db < migrations/001_add_tags_to_notes.sql
```

---

## Agent Coordination Best Practices

### Communication Between Agents

- **TestAgent → CodeAgent**: Provide test file path and test descriptions
- **CodeAgent → TestAgent**: Report pass/fail status and any issues
- **CodeAgent → DocsAgent**: Report code changes made
- **DBAgent → User**: Provide SQL diff for approval
- **RefactorAgent → CodeAgent**: Report files modified

### Parallel Execution

**When agents can work in parallel:**
- TestAgent writing tests for feature A while CodeAgent implements feature B
- DocsAgent updating API.md while TestAgent writes tests
- RefactorAgent cleaning up utility functions while CodeAgent implements routes

**When agents must run sequentially:**
- TestAgent must write tests before CodeAgent implements (TDD)
- DBAgent must approve schema changes before CodeAgent uses new schema
- CodeAgent must complete implementation before DocsAgent updates docs

### Error Handling

**When an agent fails:**
1. Agent reports error to user or next agent in workflow
2. User decides whether to retry with different approach
3. Workflow can be restarted or modified

**Example:**
```
TestAgent: Tests written in backend/tests/test_notes.py
CodeAgent: Implementation complete, but tests failing at line 47
User: Check test at line 47
TestAgent: Reviewing test...发现测试有个bug，需要修改测试
TestAgent: Test fixed
CodeAgent: Tests passing now!
```

---

## Safety and Rollback

### General Safety Guidelines

1. **Always use version control**: Commit before major changes
2. **Test frequently**: Run tests after each change
3. **Review diffs**: Check git diff before committing
4. **Backup data**: Backup database before schema changes
5. **Document changes**: Keep track of what was modified

### Rollback Procedures

**Git-based rollback:**
```bash
# View changes
git diff

# Revert specific file
git checkout -- path/to/file

# Revert all changes
git checkout -- .

# Undo last commit
git reset --soft HEAD~1
```

**Database rollback:**
```bash
# Restore from backup
cp data/app.db.backup data/app.db

# Or run rollback SQL
sqlite3 data/app.db < migrations/rollback_001.sql
```

### Verification Checklist

Before considering a workflow complete:
- [ ] All tests pass: `make test`
- [ ] Code is formatted: `make format`
- [ ] Linter passes: `make lint`
- [ ] Documentation updated: DocsAgent confirms
- [ ] Application works: Manual verification
- [ ] No breaking changes: Review API contract
- [ ] Coverage adequate: `/coverage-report`

---

## Troubleshooting

### Common Issues

**Tests won't pass after implementation:**
1. TestAgent: Review test expectations
2. CodeAgent: Check implementation against tests
3. Add print statements for debugging
4. Run specific test: `pytest -k test_name -v`

**Documentation drift detected:**
1. DocsAgent: Compare OpenAPI spec with docs
2. Identify missing or incorrect documentation
3. Update docs/API.md
4. Verify docs match actual API

**Schema change breaks existing code:**
1. DBAgent: Review schema changes
2. RefactorAgent: Update affected code
3. CodeAgent: Fix broken routes
4. TestAgent: Verify all tests pass

**Refactoring breaks functionality:**
1. RefactorAgent: Review what changed
2. CodeAgent: Fix broken references
3. TestAgent: Verify tests pass
4. Rollback if needed: `git checkout -- .`

---

## Example Session: Complete Feature Workflow

**User:** "Add DELETE /notes/{id} endpoint"

**Step 1: TestAgent**
- Writes tests in `backend/tests/test_notes.py`
- Runs tests, they fail (endpoint doesn't exist)
- Reports: "Tests written"

**Step 2: CodeAgent**
- Reads tests
- Implements DELETE endpoint in `backend/app/routers/notes.py`
- Runs tests, they pass
- Reports: "Implementation complete"

**Step 3: TestAgent**
- Re-runs all tests
- Verifies coverage
- Reports: "All tests passing"

**Step 4: DocsAgent**
- Fetches OpenAPI spec
- Updates `docs/API.md` with DELETE endpoint
- Updates `docs/TASKS.md` to mark task as completed
- Reports: "Documentation updated"

**Result:**
- New endpoint implemented
- Tests passing
- Documentation updated
- Feature complete!

---

## Summary

These agent workflows provide a structured approach to developing and maintaining the FastAPI application:

- **Workflow 1**: Feature addition using TDD
- **Workflow 2**: Documentation synchronization
- **Workflow 3**: Database schema changes

By following these workflows and using the specialized agents appropriately, you can:
- Maintain code quality
- Keep documentation in sync
- Handle database changes safely
- Refactor code with confidence
- Catch issues early with tests

Each agent has a specific role and works together with other agents to complete complex tasks efficiently and safely.
