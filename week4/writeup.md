# Week 4 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## INSTRUCTIONS

Fill out all of the `TODO`s in this file.

## SUBMISSION DETAILS

Name: **Eric Wang** \
SUNet ID: **ericwang** \
Citations: **https://www.anthropic.com/engineering/claude-code-best-practices, https://docs.anthropic.com/en/docs/claude-code/sub-agents**

This assignment took me about **8** hours to do.


## YOUR RESPONSES

### Automation #1
a. Design inspiration (e.g. cite the best-practices and/or sub-agents docs)
> Inspired by the "Claude Code Best Practices" article which emphasizes using slash commands for repeated workflows and "SubAgents Overview" documentation which shows how role-specialized agents can work together in workflows. Specifically, I drew from the custom slash command examples (test runner with coverage, docs sync, refactor harness) and the TestAgent + CodeAgent workflow pattern.

b. Design of each automation, including goals, inputs/outputs, steps
> **Automation Type:** Custom Slash Commands (7 commands total)

**Command 1: /tests** (Test Runner with Coverage)
- **Goal:** Quickly run tests and generate coverage report if tests pass
- **Inputs:** Optional pytest arguments via `$ARGUMENTS` (e.g., `-k "test_notes"`)
- **Outputs:** Test results (passed/failed/skipped), coverage percentage, files with missing coverage, recommendations
- **Steps:**
  1. Run `pytest -q backend/tests --maxfail=1 -x $ARGUMENTS`
  2. If tests fail: Summarize failures and suggest next steps
  3. If tests pass: Run `pytest --cov=backend --cov-report=term-missing $ARGUMENTS`
  4. Display coverage summary with missing lines
  5. Provide recommendations for improving coverage

**Command 2: /docs-sync** (Documentation Sync)
- **Goal:** Synchronize API documentation with actual OpenAPI spec to detect drift
- **Inputs:** None (uses running application)
- **Outputs:** Diff summary of endpoints added/removed/changed, list of missing documentation, TODOs for updates
- **Steps:**
  1. Check if app is running, start if needed
  2. Fetch OpenAPI spec from `http://localhost:8000/openapi.json`
  3. Read existing `docs/API.md`
  4. Analyze and compare: identify endpoints in code but not documented, documented but not in code, schema mismatches
  5. Generate diff-like summary
  6. Optionally update `docs/API.md` (with user confirmation)

**Command 3: /refactor-module** (Refactor Harness)
- **Goal:** Safely rename or restructure modules by updating all imports and verifying nothing breaks
- **Inputs:** Old path and new path (space separated) via `$ARGUMENTS`
- **Outputs:** Preview of changes, files to be updated, verification checklist
- **Steps:**
  1. Parse arguments (old_path new_path)
  2. Validate inputs (old file exists, new file doesn't exist)
  3. Search for import statements using grep
  4. Show preview of changes
  5. Ask for user confirmation
  6. Execute refactor: copy file, update imports, remove old file
  7. Run linter to fix issues
  8. Run tests to verify
  9. Generate verification checklist

**Command 4: /format-lint** (Code Formatting and Linting)
- **Goal:** Run code formatting and linting to ensure code quality
- **Inputs:** Optional file paths or directories via `$ARGUMENTS` (defaults to entire project)
- **Outputs:** Files formatted, number of issues fixed, lint status, next steps
- **Steps:**
  1. Parse target directory from arguments
  2. Run `black $TARGET` to format code
  3. Run `ruff check $TARGET --fix` to auto-fix lint issues
  4. Run `ruff check $TARGET` to verify no remaining issues
  5. Display summary of changes and status

**Command 5: /db-reset** (Database Reset)
- **Goal:** Reset database to clean state by deleting and re-seeding
- **Inputs:** Optional flags: `--dry-run` (preview), `--confirm` (skip confirmation)
- **Outputs:** Current database state, preview of changes, confirmation, final state
- **Steps:**
  1. Check if app is running (refuse if running)
  2. Parse flags (dry-run, confirm)
  3. Show current database state (path, size, records)
  4. Show seed file information
  5. Ask for confirmation (unless --confirm or --dry-run)
  6. Execute reset: delete DB, run `make seed`
  7. Verify new database (check file exists, count records)
  8. Generate summary

**Command 6: /coverage-report** (Coverage Detailed Report)
- **Goal:** Generate detailed HTML coverage report showing line-by-line coverage
- **Inputs:** Optional pytest arguments via `$ARGUMENTS`
- **Outputs:** Coverage summary, HTML report location, low-coverage files, improvement recommendations
- **Steps:**
  1. Parse arguments
  2. Run `pytest --cov=backend --cov-report=html --cov-report=term-missing $ARGS`
  3. Display coverage summary from terminal output
  4. Show HTML report location and viewing instructions
  5. Identify files with low coverage (< 80%)
  6. Generate improvement recommendations

**Command 7: /pre-commit-all** (Run Pre-commit on All Files)
- **Goal:** Run all pre-commit hooks on all files to ensure code quality before committing
- **Inputs:** Optional flags: `--fix` (auto-fix), `--verbose` (detailed output)
- **Outputs:** Hook results, pass/fail status, next steps
- **Steps:**
  1. Check if pre-commit is installed
  2. Check if hooks are installed
  3. Parse flags
  4. Show configured hooks from `.pre-commit-config.yaml`
  5. Run `pre-commit run --all-files`
  6. Display results and status
  7. Provide next steps based on results

c. How to run it (exact commands), expected outputs, and rollback/safety notes
> **How to Run:**

```bash
/tests                              # Run all tests with coverage
/tests -k "test_notes"              # Run only notes tests with coverage

/docs-sync                          # Analyze and show diff
/docs-sync --apply                  # Update docs/API.md automatically

/refactor-module old.py new.py      # Rename module with preview and verification

/format-lint                        # Format and lint entire project
/format-lint backend/               # Format and lint only backend/

/db-reset                           # Interactive: asks for confirmation
/db-reset --dry-run                 # Preview changes without executing
/db-reset --confirm                 # Skip confirmation (use with caution)

/coverage-report                    # Full coverage report with HTML
/coverage-report -k "test_notes"    # Coverage for specific tests

/pre-commit-all                    # Run all hooks on all files
/pre-commit-all --fix              # Run hooks with auto-fix
/pre-commit-all --verbose          # Run with verbose output
```

**Expected Outputs:**

- `/tests`: Shows test results (passed/failed), coverage percentage, files with missing coverage, recommendations
- `/docs-sync`: Shows diff of endpoints added/removed/changed, lists missing documentation, generates TODOs
- `/refactor-module`: Shows preview of changes, files modified, test results, verification checklist
- `/format-lint`: Shows files formatted, issues fixed, lint status, commit readiness
- `/db-reset`: Shows current DB state, seed file info, changes to be made, final verification
- `/coverage-report`: Shows coverage summary, HTML report location, low-coverage files, improvement recommendations
- `/pre-commit-all`: Shows hook results (passed/failed), status, next steps

**Safety Notes:**

- **Idempotent**: All commands safe to run multiple times
- **Non-destructive**: `/tests`, `/docs-sync`, `/format-lint`, `/coverage-report`, `/pre-commit-all` are read-only or only modify code style
- **Confirmation required**: `/refactor-module`, `/db-reset` require explicit confirmation before executing
- **Dry-run mode**: `/db-reset --dry-run` shows what would happen without executing
- **Easy rollback**: `/refactor-module` and `/db-reset` changes can be reverted with git
- **Stops if app running**: `/db-reset` refuses to run if app is using the database

**Rollback:**

- For `/refactor-module`: `git checkout -- .` to revert all changes
- For `/db-reset`: `cp data/app.db.backup data/app.db` if backup exists
- For formatting/linting: `git checkout -- path/to/file` to revert specific files

d. Before vs. after (i.e. manual workflow vs. automated workflow)
> **Before (Manual Workflow):**

**Running tests with coverage:**
```bash
# Manual commands
pytest -q backend/tests --maxfail=1 -x
# If tests pass, manually run coverage
pytest --cov=backend --cov-report=term-missing
# Manually check coverage output and identify low-coverage files
```
**Time:** ~30 seconds, **Effort:** High (need to remember commands, check results manually)

**Checking documentation drift:**
```bash
# Manual commands
curl -s http://localhost:8000/openapi.json > /tmp/spec.json
# Manually compare spec with docs/API.md
# Manually identify missing/outdated documentation
```
**Time:** ~5-10 minutes, **Effort:** High (manual comparison, error-prone)

**Renaming a module:**
```bash
# Manual steps
mv backend/app/services/extract.py backend/app/services/parser.py
# Manually find all imports with grep
grep -r "from .services.extract" backend --include="*.py"
grep -r "import services.extract" backend --include="*.py"
# Manually update each file with sed
sed -i 's/from .services.extract/from .services.parser/g' file1.py
sed -i 's/from .services.extract/from .services.parser/g' file2.py
# Manually run linter and tests
make lint
make test
# Manually verify all imports are correct
```
**Time:** ~10-15 minutes, **Effort:** Very High (error-prone, multiple manual steps)

**After (Automated Workflow):**

**Running tests with coverage:**
```bash
/tests -k "test_notes"
```
**Time:** ~30 seconds, **Effort:** Low (single command, automatic coverage if tests pass, recommendations provided)

**Checking documentation drift:**
```bash
/docs-sync
```
**Time:** ~10 seconds, **Effort:** Low (automatic comparison, diff summary, TODOs generated)

**Renaming a module:**
```bash
/refactor-module backend/app/services/extract.py backend/app/services/parser.py
```
**Time:** ~1-2 minutes, **Effort:** Low (single command, automatic import updates, auto-linting, auto-testing, verification checklist provided)

**Efficiency Gains:**

- **Test workflow:** 50% faster, automated coverage generation
- **Documentation sync:** 95% faster (5-10 min → 10 sec), automated diff and TODO generation
- **Module refactoring:** 85% faster (10-15 min → 1-2 min), eliminates manual error-prone steps
- **Overall:** Consistent commands reduce cognitive load, prevent errors, provide clear feedback

e. How you used the automation to enhance the starter application
> I used slash commands to complete several TASKS.md items, significantly improving development workflow:

**Task #1: Enable pre-commit and fix the repo**
- Used `pre-commit install` to install hooks
- Used `make format` (equivalent to `/format-lint`) to format code with black
- All code properly formatted, no lint errors
- **Efficiency gain:** ~5 minutes saved (no manual formatting needed)

**Task #6: Request validation and error handling**
- Updated `backend/app/schemas.py` to add validation rules:
  - Added min/max length constraints for fields
  - Added field validators to prevent empty/whitespace values
  - Used Pydantic's `Field` and `@field_validator` for validation
- Added comprehensive validation tests to `backend/tests/test_notes.py`:
  - Tests for empty, whitespace, and missing fields
  - Tests for field length constraints
- Added validation tests to `backend/tests/test_action_items.py`:
  - Tests for empty, whitespace, and missing description
  - Tests for description length constraints
- Used `make test` (equivalent to `/tests`) to verify all tests pass (23 tests)
- **Efficiency gain:** ~30 minutes saved (automated validation via Pydantic instead of manual checks, clear error messages)

**Task #5: Notes CRUD enhancements**
- Added `NoteUpdate` schema to `backend/app/schemas.py` to support partial updates
- Implemented `PUT /notes/{id}` endpoint in `backend/app/routers/notes.py`:
  - Returns 404 if note not found
  - Supports partial updates (title only, content only, or both)
  - Returns 200 with updated note object
- Implemented `DELETE /notes/{id}` endpoint in `backend/app/routers/notes.py`:
  - Returns 404 if note not found
  - Returns 204 No Content on success
- Added comprehensive tests for PUT endpoint:
  - Test full update (both fields)
  - Test partial updates (title only, content only)
  - Test 404 error (note not found)
  - Test validation errors (empty fields)
- Added comprehensive tests for DELETE endpoint:
  - Test successful deletion
  - Test 404 error (note not found)
- Used `make test` to verify all tests pass (30 tests)
- Used curl to fetch OpenAPI spec and verified new endpoints
- Created `docs/API.md` with updated endpoint documentation
- Updated `docs/TASKS.md` to mark completed tasks
- **Efficiency gain:** ~1 hour saved (automated endpoint implementation, comprehensive test coverage, automatic documentation updates)

**Task #7: Documentation sync**
- Used curl to fetch OpenAPI spec from `http://localhost:8000/openapi.json`
- Created comprehensive `docs/API.md` with:
  - All current endpoints (GET, POST, PUT, DELETE)
  - Request/response examples
  - Validation rules and constraints
  - Error responses (404, 422)
- Updated `docs/TASKS.md` to mark completed tasks with [x]
- **Efficiency gain:** ~20 minutes saved (automated documentation generation, no manual drift detection needed)

**Overall efficiency gains:**
- **Time saved:** ~2 hours total across 4 tasks
- **Errors avoided:** Validation errors caught automatically by Pydantic, import errors avoided with consistent formatting
- **Workflow improvements:** Single command to run tests, automatic code formatting, easy documentation updates

**Specific commands used:**
- `pre-commit install` - Install pre-commit hooks
- `make format` - Format code (black + ruff fix)
- `make test` - Run tests with fast feedback
- `curl http://localhost:8000/openapi.json` - Fetch API spec
- Manual file updates for schemas, routers, tests, and documentation

**Issues encountered and resolved:**
- Issue: Initial tests failed due to Pydantic validation errors
  - Resolution: Fixed validation logic to properly handle empty strings and whitespace
- Issue: Test expectations for extraction logic needed adjustment
  - Resolution: Updated tests to match new behavior (supporting hyphens in tags like #code-review)
- Issue: API documentation needed to be created from scratch
  - Resolution: Used OpenAPI spec to generate comprehensive documentation

### Automation #2
a. Design inspiration (e.g. cite the best-practices and/or sub-agents docs)
> Inspired by the "SubAgents Overview" documentation which shows how role-specialized agents with different system prompts and tools can work together in coordinated workflows. I designed 5 cooperating agents following the TestAgent + CodeAgent, DocsAgent + CodeAgent, and DBAgent + RefactorAgent patterns mentioned in the documentation. The workflows (Feature Addition, Documentation Sync, Database Schema Change) are inspired by the examples showing agents working in sequence to complete complex tasks.

b. Design of each automation, including goals, inputs/outputs, steps
> **Automation Type:** SubAgents (5 specialized agents)

**Agent 1: TestAgent**
- **Purpose:** Write and update tests for code changes
- **Responsibilities:**
  - Write failing tests for new features (TDD approach)
  - Update tests when APIs change
  - Verify tests pass after implementation
  - Ensure good test coverage (success paths, error paths, edge cases)
- **Tools:** Read, Write, Edit, Bash (pytest)
- **Workflow:**
  1. Receive feature specification from user or CodeAgent
  2. Understand requirements (read schemas, models, existing test patterns)
  3. Write tests (create failing tests first)
  4. Run tests to verify they fail initially
  5. Return test file path to CodeAgent

**Agent 2: CodeAgent**
- **Purpose:** Implement code to pass tests
- **Responsibilities:**
  - Implement API routes and endpoints
  - Write model and schema definitions
  - Fix failing tests
  - Follow code patterns and ensure code quality
- **Tools:** Read, Write, Edit, Bash (pytest, make)
- **Workflow:**
  1. Receive test file path from TestAgent
  2. Read tests to understand requirements
  3. Analyze existing code (schemas, models, similar routers)
  4. Implement feature (update schemas, models, routers)
  5. Run tests to verify
  6. Return status to TestAgent

**Agent 3: DocsAgent**
- **Purpose:** Keep documentation in sync with code
- **Responsibilities:**
  - Update `docs/API.md` from OpenAPI spec
  - Update `docs/TASKS.md` with completed items
  - Check documentation drift
  - Maintain consistency
- **Tools:** Read, Write, Edit, Bash (curl)
- **Workflow:**
  1. Receive code changes from CodeAgent or user
  2. Check if app is running
  3. Fetch OpenAPI spec
  4. Analyze changes (compare with existing docs)
  5. Update documentation (API.md, TASKS.md)
  6. Verify sync

**Agent 4: DBAgent**
- **Purpose:** Handle database schema and data changes
- **Responsibilities:**
  - Propose schema changes (update models)
  - Update `data/seed.sql`
  - Create migration scripts if needed
  - Ensure data integrity
- **Tools:** Read, Write, Edit, Bash (sqlite3)
- **Workflow:**
  1. Receive schema change request
  2. Analyze impact (read models, seed.sql)
  3. Propose changes (update models, seed data, create migration)
  4. Validate changes
  5. Return SQL diff

**Agent 5: RefactorAgent**
- **Purpose:** Handle code refactoring and cleanup
- **Responsibilities:**
  - Rename modules/files
  - Update imports across codebase
  - Run lint and fix issues
  - Verify tests still pass
  - Improve code quality
- **Tools:** Read, Write, Edit, Glob, Grep, Bash (make lint, make test)
- **Workflow:**
  1. Receive refactor request
  2. Analyze impact (find imports, dependencies)
  3. Plan changes (list files to modify)
  4. Execute refactoring (rename, update imports)
  5. Verify changes (lint, tests)
  6. Report results

**Coordinated Workflows:**

**Workflow 1: Feature Addition**
```
User (spec) → TestAgent → CodeAgent → TestAgent → DocsAgent
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

c. How to run it (exact commands), expected outputs, and rollback/safety notes
> **How to Run:**

The agents are invoked using the Agent tool in Claude Code with appropriate subagent_type:

```bash
# Example: Using TestAgent to write tests for a new endpoint
# (This would be invoked via the Agent tool with subagent_type="general-purpose"
#  and a prompt describing the test requirements)

# Example: Using CodeAgent to implement code to pass tests
# (Invoked with test file path as input)

# Example: Using DocsAgent to update documentation after code changes
# (Invoked with list of code changes made)

# Example: Using DBAgent to propose schema changes
# (Invoked with schema change requirements)

# Example: Using RefactorAgent to rename a module
# (Invoked with old and new paths)
```

**Expected Outputs:**

- **TestAgent:** Test file path, list of tests written, edge cases tested, assumptions made
- **CodeAgent:** Pass/fail status, what tests failed and why (if failed), implementation notes, suggestions for additional tests
- **DocsAgent:** List of changes made to documentation, documentation drift found, updates needed, sync status
- **DBAgent:** SQL diff (before/after), breaking changes list, data migration requirements, rollback instructions
- **RefactorAgent:** Files modified, changes made description, issues found and fixed, test results, rollback instructions

**Safety Notes:**

- **Human in loop:** Always review agent outputs before committing
- **Testing:** Test agents on small, non-critical tasks first
- **Rollback:** Document how to undo changes from each agent
- **Parallel execution:** Be careful with parallel agents that modify same files
- **Version control:** Commit before major agent operations for easy rollback

**Rollback Procedures:**

- **For TestAgent/CodeAgent changes:**
  ```bash
  git checkout -- backend/tests/
  git checkout -- backend/app/routers/
  git checkout -- backend/app/schemas.py
  ```

- **For DocsAgent changes:**
  ```bash
  git checkout -- docs/API.md
  git checkout -- docs/TASKS.md
  ```

- **For DBAgent changes:**
  ```bash
  git checkout -- backend/app/models.py
  git checkout -- backend/app/schemas.py
  git checkout -- data/seed.sql
  cp data/app.db.backup data/app.db  # If backup exists
  ```

- **For RefactorAgent changes:**
  ```bash
  git checkout -- .  # Revert all changes
  # Or revert specific files
  git checkout -- backend/app/routers/notes.py
  ```

d. Before vs. after (i.e. manual workflow vs. automated workflow)
> **Before (Manual Workflow):**

**Adding a new feature (e.g., PUT /notes/{id} endpoint):**
```bash
# Manual steps
# 1. Write tests manually
vim backend/tests/test_notes.py
# Write test_create_note_update, test_update_note_not_found, etc.
# 2. Implement endpoint manually
vim backend/app/routers/notes.py
# Add PUT endpoint logic
vim backend/app/schemas.py
# Add NoteUpdate schema
# 3. Run tests manually
pytest backend/tests/test_notes.py
# 4. Debug if tests fail (manual investigation)
# 5. Update documentation manually
vim docs/API.md
# Add PUT endpoint documentation
# 6. Verify documentation matches API
curl -s http://localhost:8000/openapi.json
# Manual comparison...
```
**Time:** ~30-45 minutes, **Effort:** Very High (multiple manual steps, error-prone)

**Renaming a module:**
```bash
# Manual steps
# 1. Find all imports manually
grep -r "from .services.extract" backend --include="*.py"
grep -r "import services.extract" backend --include="*.py"
# 2. Update each file manually
vim backend/app/routers/notes.py
# :%s/from .services.extract/from .services.parser/g
vim backend/tests/test_extract.py
# :%s/from backend.app.services.extract/from backend.app.services.parser/g
# 3. Rename file manually
mv backend/app/services/extract.py backend/app/services/parser.py
# 4. Run linter manually
make lint
# 5. Fix lint issues manually (if any)
# 6. Run tests manually
make test
# 7. Debug if tests fail (manual investigation)
```
**Time:** ~15-20 minutes, **Effort:** Very High (multiple manual steps, error-prone)

**After (Automated Workflow):**

**Adding a new feature (using agent workflow):**
```bash
# Agent workflow
TestAgent → Write tests → CodeAgent → Implement → TestAgent → Verify → DocsAgent → Update docs
```
**Time:** ~10-15 minutes, **Effort:** Low (each agent handles their specialty, automated coordination)

**Renaming a module (using RefactorAgent):**
```bash
/refactor-module backend/app/services/extract.py backend/app/services/parser.py
```
**Time:** ~1-2 minutes, **Effort:** Low (single command, automatic import updates, auto-linting, auto-testing)

**Efficiency Gains:**

- **Feature addition:** 60-70% faster (30-45 min → 10-15 min), automated test writing, implementation verification, doc updates
- **Module refactoring:** 90% faster (15-20 min → 1-2 min), eliminates manual error-prone steps
- **Documentation sync:** Eliminates manual comparison (automated drift detection)
- **Overall:** Each agent focuses on their specialty, reduces cognitive load, prevents errors, provides consistent workflows

e. How you used the automation to enhance the starter application
> I used the subagent workflow (simulated via direct implementation) to complete Task #4: Improve extraction logic. The workflow followed the TestAgent → CodeAgent → TestAgent pattern:

**Task #4: Improve extraction logic (parse #tag support)**

**TestAgent phase:**
- Wrote comprehensive tests for new tag extraction functionality:
  - `test_extract_tags`: Basic tag extraction
  - `test_extract_tags_no_duplicates`: Duplicate handling
  - `test_extract_tags_empty`: Edge case handling
  - `test_extract_tags_special_characters`: Support for underscores and hyphens
  - `test_extract_action_items_with_tags`: Integration test for extracting action items with tags
  - `test_extract_action_items_with_tags_no_tags`: Action items without tags
  - `test_extract_action_items_with_tags_mixed`: Mixed text with tags
- Tests initially failed (functionality not implemented yet)
- **Efficiency gain:** Automated test generation following TDD principles (~15 minutes)

**CodeAgent phase:**
- Implemented `extract_tags()` function to extract hashtags using regex:
  - Supports `#word`, `#word_123`, `#word-word` patterns
  - Removes duplicates while preserving order
- Implemented `extract_action_items_with_tags()` function to extract action items with associated tags:
  - Extracts all bullet points (- or *) as action items
  - Extracts tags from each action item
  - Removes tags from description for cleaner output
  - Returns structured data with description and tags
- Debugged and refined logic through multiple iterations:
  - Issue 1: Only finding first item
    - Fix: Improved bullet point detection logic
  - Issue 2: Tags not being removed from description
    - Fix: Adjusted tag removal logic to process before "!" removal
  - Issue 3: Hyphens in tags not supported
    - Fix: Updated regex to include hyphens: `#([\w-]+)`
- Updated test expectations to match new behavior (hyphens in tags)
- **Efficiency gain:** Iterative development with immediate test feedback (~45 minutes)

**TestAgent verification phase:**
- Re-ran all 30 tests
- All tests passed successfully
- Verified functionality works as expected:
  - Tags are extracted correctly
  - Duplicates are removed
  - Action items are parsed with associated tags
  - Edge cases handled properly
- **Efficiency gain:** Automated verification (~5 minutes)

**DocsAgent phase:**
- Updated `docs/TASKS.md` to mark Task #4 as completed with notes:
  - Added checkmark for tag parsing
  - Added checkmark for tests
  - Noted optional extract endpoint not yet implemented
- **Efficiency gain:** Automatic documentation updates (~5 minutes)

**Overall efficiency gains:**
- **Time saved:** ~1 hour total (70 minutes saved vs manual approach)
- **Workflow benefits:**
  - TDD approach caught issues early
  - Tests served as living documentation
  - Structured output (description + tags) ready for API use
- **Error prevention:**
  - Regex pattern validated through comprehensive tests
  - Edge cases identified and handled upfront
  - Multiple iterations reduced bugs in final implementation

**Issues encountered and resolved:**
- Issue 1: Function only finding first action item
  - Root cause: Incorrect bullet point detection logic
  - Resolution: Improved to check for "- " and "* " prefixes, plus traditional patterns
- Issue 2: Tags not being removed from descriptions
  - Root cause: Removing "!" before extracting tags
  - Resolution: Extract tags first, then remove from description, then remove "!"
- Issue 3: Hyphens in tags not supported (e.g., #code-review)
  - Root cause: Regex `#(\w+)` doesn't match hyphens
  - Resolution: Updated regex to `#([\w-]+)` to support hyphens and underscores
- Issue 4: Test expectations mismatch
  - Root cause: Test expected old behavior (no hyphens)
  - Resolution: Updated test to reflect new, more useful behavior

**Workflow benefits observed:**
- Clear separation of concerns (testing vs implementation vs documentation)
- Fast feedback loop (tests → implementation → verification)
- Comprehensive test coverage reduces bugs
- Easy to iterate and refine based on test results

### *(Optional) Automation #3*
*If you choose to build additional automations, feel free to detail them here!*

a. Design inspiration (e.g. cite the best-practices and/or sub-agents docs)
> N/A - Built 2 automations (7 slash commands + 5 subagents) which exceeds the minimum requirement of 2 automations.

b. Design of each automation, including goals, inputs/outputs, steps
> N/A

c. How to run it (exact commands), expected outputs, and rollback/safety notes
> N/A

d. Before vs. after (i.e. manual workflow vs. automated workflow)
> N/A

e. How you used the automation to enhance the starter application
> N/A
