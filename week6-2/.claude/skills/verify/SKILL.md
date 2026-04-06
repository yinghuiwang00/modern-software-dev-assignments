---
name: verify
description: Verify security fixes by running tests and re-scanning with Semgrep
---

# Verify Skill - Verify Security Fixes

## Overview

Verifies that security fixes are working correctly by running application tests and re-scanning with Semgrep to confirm issues are resolved.

## Usage

```
/verify
```

## What It Does

1. Invokes the `test-runner` agent
2. Runs pytest tests on backend
3. Verifies application starts without errors
4. Re-runs Semgrep scan
5. Checks that fixed issues are resolved
6. Generates `test-results.md` and updated `semgrep-results.json`

## Test Commands Run

```bash
# Run all tests
pytest backend/tests/ -v

# Start application to verify
python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 &
# ... test endpoints ...
# Kill the process

# Re-run Semgrep
semgrep ci --subdir week6 --output semgrep-results.json --json
```

## Expected Output

A summary including:
- Test results (passed/failed)
- Application status (running/not running)
- Semgrep re-scan results
- Verification status (all issues resolved / some remaining)

## Example Output

```
Verifying security fixes...

Test Results:
- Total tests: 15
- Passed: 15
- Failed: 0
- Status: ✓ All tests passed

Application Status:
- Status: ✓ Running on http://localhost:8000
- Endpoints verified: /, /notes/, /action-items/

Semgrep Re-scan:
- Previous findings: 42
- Fixed issues: 3
- Remaining findings: 39
- Status: ✓ All fixed issues resolved

Test results saved to: test-results.md
Updated scan results: semgrep-results.json
```

## Prerequisites

- Security fixes must have been applied
- Code should be syntactically correct
- All dependencies should be installed

## Verification Checklist

- [ ] All tests pass
- [ ] Application starts without errors
- [ ] Key endpoints are accessible
- [ ] No regressions introduced
- [ ] Fixed issues don't appear in re-scan
- [ ] No new security issues introduced

## Error Handling

If tests fail:
- Document which tests failed
- Provide error messages
- Suggest fixes or next steps
- Ask if user wants to continue

If application won't start:
- Check for syntax errors
- Check for missing imports
- Document the error
- Suggest fixes

If issues still in re-scan:
- Identify which issues remain
- Check if fix was applied correctly
- Suggest re-fixing the issue

## Next Steps

After verification:
- If all verified: Use `/report` to generate final report
- If issues found: Fix issues and re-run `/verify`
- Use `/workflow` to run complete process
