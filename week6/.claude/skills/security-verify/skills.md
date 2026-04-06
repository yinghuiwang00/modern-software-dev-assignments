---
name: security-verify
description: Verify security fixes are correct and complete. Runs tests, smoke tests application, and re-runs Semgrep to confirm resolution.
allowed-tools: Bash, Read, Grep, Glob, mcp__ide__getDiagnostics, Agent
triggers: verify fix, validate security fix, confirm remediation
---

# Security Verification Skill

Verify that a security fix is correct and complete by running comprehensive tests and re-scanning with Semgrep.

## When to Use

Use this skill after `/security-fix` to:
- Verify the fix works correctly
- Ensure no regressions were introduced
- Confirm the issue is resolved in Semgrep
- Validate the application still works

## Prerequisites

- Fix has been implemented via `/security-fix`
- Tests have been added/updated
- Application should be runnable

## Instructions

### Phase 1: Run Test Suite

Execute comprehensive testing:

```bash
# Navigate to parent directory
cd /home/ericwang/workspace/AI_Coding/College_Application_03.08/modern-software-dev-assignments/

# Backend tests
cd week6/backend
python -m pytest tests/ -v --cov

# Frontend tests
cd ../frontend
npm test

# Check for any test failures
```

Document the results:
- Number of tests run
- Number of tests passed/failed
- Coverage percentage
- Any failing tests (if any)

### Phase 2: Smoke Test the Application

Start the application and perform basic smoke tests:

```bash
# Backend smoke test
cd week6/backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 &

# Wait for startup
sleep 3

# Test basic endpoints
curl http://localhost:8000/health || echo "Health check failed"
curl http://localhost:8000/ || echo "Root endpoint failed"

# Cleanup
pkill -f "uvicorn app.main:app"
```

### Phase 3: Launch Test Validator Agent

Use the Agent tool to create and run a validation agent:

```
Launch test-validator-agent with:
- subagent_type: "general-purpose"
- name: "test-validator-agent"
- prompt: "You are a security validation specialist. Verify the fix for issue '{issue_id}':

**Validation Steps:**

1. **Run Backend Tests:**
   - cd week6/backend && python -m pytest tests/ -v --cov
   - Record all test results
   - Note any failures

2. **Run Frontend Tests:**
   - cd week6/frontend && npm test
   - Record all test results
   - Note any failures

3. **Smoke Test Application:**
   - Start the backend server
   - Test basic endpoints (health, root)
   - Verify no crashes or errors

4. **Re-run Semgrep Scan:**
   - cd /home/ericwang/workspace/AI_Coding/College_Application_03.08/modern-software-dev-assignments/
   - semgrep scan week6 --json | grep '{issue_id}'
   - Check if the issue is still present

5. **Check for Regressions:**
   - Compare new scan results with original
   - Identify any new issues introduced

**Generate Report:**
Create a verification report saved to week6/verification-{issue_id}.md containing:
- Test results (backend and frontend)
- Smoke test results
- Semgrep scan results (is issue resolved?)
- Any new issues introduced
- Overall verification status (PASS/FAIL)

**Exit Codes:**
- Return PASS if: all tests pass, smoke test works, issue is resolved in semgrep, no new issues
- Return FAIL if: any test fails, smoke test fails, issue still present, or new issues introduced"
```

### Phase 4: Present Verification Results

Create a summary for the user:

```markdown
# Verification Results: [Issue Title]

## Test Results
- **Backend Tests**: ✅ PASSED (N/N) | ❌ FAILED (X/N)
- **Frontend Tests**: ✅ PASSED | ❌ FAILED
- **Coverage**: N%

## Smoke Test
- **Health Check**: ✅ OK | ❌ Failed
- **Application**: ✅ Running | ❌ Crashed

## Semgrep Scan
- **Issue Resolved**: ✅ Yes | ❌ No (still present)
- **New Issues**: None | Found N new issues

## Overall Status
**✅ VERIFIED** or **❌ FAILED**

## Issues Found (if any)
- [List any failures or new issues]
```

### Phase 5: Handle Failures

If verification fails:

1. **Test Failures**:
   - Read the test output
   - Identify what's failing
   - Return to `/security-fix` to adjust

2. **Issue Still Present**:
   - The fix didn't address the vulnerability
   - Re-analyze with `/security-analyze`
   - Fix again with `/security-fix`

3. **New Issues Introduced**:
   - The fix created new problems
   - Analyze the new issues
   - Adjust the fix

## Output

- `week6/verification-{issue_id}.md` - Detailed verification report
- Summary presented to user
- Pass/Fail status

## Example Usage

**User**: "Verify the SQL injection fix"

**Response**:
```
Launching test-validator-agent to verify python.sql-injection fix...

**Running Backend Tests...**
tests/test_routes.py::test_get_user PASSED
tests/test_sql_injection.py::test_sql_injection_prevention PASSED
======================== 2 passed in 0.5s ========================
Coverage: 95%

**Running Frontend Tests...**
PASS: frontend/src/App.test.js
All frontend tests passed ✓

**Smoke Testing Application...**
Starting backend server...
Health check: 200 OK ✓
Root endpoint: 200 OK ✓
Server stopped.

**Re-running Semgrep Scan...**
Searching for python.sql-injection...
Result: No matches found ✓

**Checking for New Issues...**
Comparing with original scan...
No new issues introduced ✓

## Verification Results: SQL Injection Fix

### Test Results
- **Backend Tests**: ✅ PASSED (2/2)
- **Frontend Tests**: ✅ PASSED
- **Coverage**: 95%

### Smoke Test
- **Health Check**: ✅ OK
- **Application**: ✅ Running

### Semgrep Scan
- **Issue Resolved**: ✅ Yes
- **New Issues**: None

### Overall Status
**✅ VERIFIED**

Detailed report saved to: week6/verification-python.sql-injection.md

The fix is complete and verified! Ready to proceed to the next issue.
```

## Next Steps

After successful verification:
- Proceed to fix the next issue (back to `/security-analyze`)
- After all 3 issues are fixed, run `/security-report` to generate the final report
