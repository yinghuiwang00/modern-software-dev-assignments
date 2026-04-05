# Test Runner with Coverage

Run the test suite with optional markers or paths, and generate coverage report if tests pass.

## Intent
Run `pytest -q backend/tests --maxfail=1 -x` to quickly identify failures. If tests pass, automatically generate a coverage report.

## Inputs
- `$ARGUMENTS`: Optional pytest arguments (marker, path, or specific test name)
  - Examples: `-k "test_notes"`, `backend/tests/test_notes.py`, `-m "slow"`

## Steps

1. **Run tests with failure fast mode**:
   ```bash
   pytest -q backend/tests --maxfail=1 -x $ARGUMENTS
   ```

2. **Analyze results**:
   - If tests FAIL: Summarize failures and suggest next steps
   - If tests PASS: Proceed to coverage

3. **Generate coverage report** (if tests passed):
   ```bash
   pytest --cov=backend --cov-report=term-missing $ARGUMENTS
   ```

4. **Output summary**:
   - Test results (passed/failed/skipped)
   - Coverage percentage
   - Files with missing coverage
   - Recommendations for improving coverage

## Expected Output

**Success Example:**
```
Running tests with: pytest -q backend/tests --maxfail=1 -x
...                                                                   [100%]
3 passed in 0.12s

Coverage Report:
---------- coverage: platform linux, python 3.11 ----------
Name                            Stmts   Miss  Cover   Missing
----------------------------------------------------------------
backend/app/__init__.py              1      0   100%
backend/app/db.py                   42      8    81%   18-20, 28-30
backend/app/models.py               14      0   100%
backend/app/routers/notes.py        25      2    92%   47-48
----------------------------------------------------------------
TOTAL                              82     10    88%

Files with < 100% coverage:
- backend/app/db.py: 81% coverage
- backend/app/routers/notes.py: 92% coverage

Recommendations:
- Add tests for db.py error handling (lines 18-20, 28-30)
- Add test for notes.py error handling (lines 47-48)
```

**Failure Example:**
```
Running tests with: pytest -q backend/tests --maxfail=1 -x
backend/tests/test_notes.py::test_create_and_list_notes FAILED
================================ FAILURES =================================
_________________________ test_create_and_list_notes _________________________
File "/path/to/test_notes.py", line 4, in test_create_and_list_notes
    assert r.status_code == 201, r.text
AssertionError: 400 {"detail": "Invalid input"}

Tests FAILED at first failure

Summary:
- Failed: 1 test (test_create_and_list_notes)
- Error: Status code 400 instead of 201
- Likely cause: Validation error in request payload

Next steps:
1. Check the test payload
2. Verify schema validation in backend/app/schemas.py
3. Check error response details in r.text
```

## Safety Notes
- Uses `--maxfail=1 -x` to stop at first failure for quick feedback
- Coverage only runs if tests pass (no need to generate coverage for broken code)
- All operations are read-only (test database is in-memory, not production)

## How to Run
```bash
/tests                    # Run all tests
/tests -k "test_notes"    # Run only notes tests
/tests backend/tests/test_notes.py  # Run specific test file
```

## Rollback
No rollback needed - tests are read-only operations.
