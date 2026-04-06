---
name: security-fix
description: Fix security issues using Test-Driven Development (TDD). Follows RED-GREEN-IMPROVE cycle: write test first, implement fix, refactor.
allowed-tools: Read, Edit, Write, Bash, Grep, TaskCreate, TaskUpdate, Agent, mcp__ide__getDiagnostics
triggers: fix security issue, implement security fix, remediate vulnerability
---

# Security Fix Implementation Skill

Fix security issues using Test-Driven Development (TDD) following the RED-GREEN-IMPROVE cycle.

## When to Use

Use this skill after `/security-analyze` to:
- Implement the security fix
- Follow TDD best practices
- Ensure code quality
- Document the changes

## Prerequisites

- Analysis document from `/security-analyze` for the issue
- Understanding of the vulnerability and recommended fix

## TDD Cycle

This skill strictly follows the TDD cycle:

1. **RED**: Write a failing test (if no test exists)
2. **GREEN**: Implement minimal fix to pass the test
3. **IMPROVE**: Refactor for code quality and maintainability

## Instructions

### Phase 1: Read Analysis

Read the analysis document to understand:
- The vulnerability
- The recommended fix
- Potential side effects

```bash
cat week6/analysis-{issue_id}.md
```

### Phase 2: Launch Fix Implementer Agent

Use the Agent tool to create and run a TDD-focused implementation agent:

```
Launch fix-implementer-agent with:
- subagent_type: "general-purpose"
- name: "fix-implementer-agent"
- prompt: "You are a TDD-focused security remediation specialist. Fix security issue '{issue_id}' following strict TDD principles:

**TDD CYCLE - FOLLOW EXACTLY:**

1. **RED** - Write a failing test:
   - If no test exists for this vulnerability, write one first
   - The test should fail with the vulnerable code
   - Save the test file

2. **GREEN** - Implement minimal fix:
   - Make the smallest change possible to pass the test
   - Do NOT refactor yet
   - Run the test to verify it passes

3. **IMPROVE** - Refactor:
   - Now refactor the code for quality
   - Ensure the test still passes
   - Improve readability and maintainability

**Requirements:**
- Read the analysis in week6/analysis-{issue_id}.md
- Follow the recommended fix approach
- Make minimal, targeted changes
- Document your changes in week6/fix-{issue_id}.md
- Create a before/after diff

**Test Commands:**
- Backend: cd week6/backend && python -m pytest tests/ -v
- Frontend: cd week6/frontend && npm test

**Important:**
- Do not skip any TDD step
- Verify tests pass after each step
- Address the root cause, not just symptoms
- Save your progress and documentation"
```

### Phase 3: Verify the Fix

After the agent completes:

1. Run the test suite:
   ```bash
   cd week6/backend && python -m pytest tests/ -v --cov
   cd week6/frontend && npm test
   ```

2. Check for any linting issues:
   ```bash
   cd week6/backend && python -m ruff check .
   cd week6/frontend && npm run lint
   ```

3. Verify the fix addresses the root cause

### Phase 4: Document the Fix

Create a fix documentation with before/after:

```markdown
# Security Fix: [Issue Title]

## Issue
- **Rule ID**: [rule-id]
- **File**: [path/to/file.py:123]

## Before
```python
# Vulnerable code
```

## After
```python
# Fixed code
```

## Changes Made
- [List specific changes]
- [Explain why this fixes the vulnerability]

## Testing
- [Test added]: [test description]
- [Test results]: [pass/fail]

## Verification
- [x] Tests pass
- [x] No new issues introduced
- [x] Root cause addressed
```

## Output

- Fixed code files
- Test files (if added)
- `week6/fix-{issue_id}.md` - Fix documentation
- Before/after diff

## Example Usage

**User**: "Fix the SQL injection issue"

**Response**:
```
Launching fix-implementer-agent to fix python.sql-injection...

**TDD Step 1: RED - Writing failing test...**
Created: backend/tests/test_sql_injection.py
Test should FAIL with vulnerable code ✓

**TDD Step 2: GREEN - Implementing minimal fix...**
Modified: backend/app/routes.py:42
Changed from: query = f"SELECT * FROM users WHERE id = {user_id}"
Changed to: query = text("SELECT * FROM users WHERE id = :id")
Running tests... PASSED ✓

**TDD Step 3: IMPROVE - Refactoring...**
Refactored for better error handling
Running tests... PASSED ✓

## Fix Summary
- Modified: backend/app/routes.py
- Added test: backend/tests/test_sql_injection.py
- All tests passing

Fix documented in: week6/fix-python.sql-injection.md
```

## Next Steps

After fix is complete, proceed to `/security-verify` to validate the fix.
