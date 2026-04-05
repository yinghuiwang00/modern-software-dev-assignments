# Coverage Report

Run pytest with coverage and generate an HTML report with detailed coverage information.

## Intent
Generate a detailed HTML coverage report showing which lines of code are covered by tests and which are not.

## Inputs
- `$ARGUMENTS`: Optional pytest arguments (marker, path, or specific test name)
  - Example: `-k "test_notes"`
  - Example: `backend/tests/test_notes.py`

## Steps

1. **Parse arguments**:
   ```bash
   ARGS="${ARGUMENTS:-}"

   echo "Generating coverage report..."
   echo "Arguments: $ARGS"
   ```

2. **Run coverage**:
   ```bash
   echo ""
   echo "=== RUNNING TESTS WITH COVERAGE ==="
   pytest --cov=backend --cov-report=html --cov-report=term-missing $ARGS

   if [ $? -ne 0 ]; then
     echo ""
     echo "Tests failed! Coverage report may be incomplete."
     echo "Please fix failing tests and try again."
     exit 1
   fi
   ```

3. **Display coverage summary**:
   ```bash
   echo ""
   echo "=== COVERAGE SUMMARY ==="
   echo "HTML report generated at: htmlcov/index.html"
   echo ""
   echo "To view the report:"
   echo "  - Open htmlcov/index.html in your browser"
   echo "  - Or run: python -m http.server 8080 -d htmlcov"
   echo "    Then visit: http://localhost:8080"
   ```

4. **Show low-coverage files**:
   ```bash
   echo ""
   echo "=== FILES WITH LOW COVERAGE (< 80%) ==="

   # Extract coverage percentages from terminal output
   COVERAGE_FILE="htmlcov/index.html"
   if [ -f "$COVERAGE_FILE" ]; then
     # Parse and display files with low coverage
     echo "Check the HTML report for detailed line-by-line coverage."
   fi
   ```

5. **Generate improvement recommendations**:
   ```bash
   echo ""
   echo "=== COVERAGE IMPROVEMENT RECOMMENDATIONS ==="
   echo ""
   echo "Files to improve (target: 80%+):"
   echo "  - Identify untested functions and add tests"
   echo "  - Test error handling paths"
   echo "  - Test edge cases and boundary conditions"
   echo ""
   echo "Testing best practices:"
   echo "  - Write tests before implementation (TDD)"
   echo "  - Test both success and failure paths"
   echo "  - Use mocking for external dependencies"
   echo "  - Keep tests fast and independent"
   echo ""
   echo "Coverage goals:"
   echo "  - Minimum: 80% coverage"
   echo "  - Target: 90%+ coverage for business logic"
   echo "  - Critical paths: 100% coverage"
   ```

## Expected Output

**Example Success Output:**
```
Coverage Report
===============

Generating coverage report...
Arguments:

=== RUNNING TESTS WITH COVERAGE ===
---------- coverage: platform linux, python 3.11 ----------
Name                            Stmts   Miss  Cover   Missing
----------------------------------------------------------------
backend/app/__init__.py              1      0   100%
backend/app/db.py                   42      8    81%   18-20, 28-30
backend/app/models.py               14      0   100%
backend/app/routers/action_items.py  28      2    93%   31-32
backend/app/routers/notes.py        25      2    92%   47-48
backend/app/services/extract.py      5      0   100%
----------------------------------------------------------------
TOTAL                              115     12    90%

Coverage HTML written to dir htmlcov

=== COVERAGE SUMMARY ===
HTML report generated at: htmlcov/index.html

To view the report:
  - Open htmlcov/index.html in your browser
  - Or run: python -m http.server 8080 -d htmlcov
    Then visit: http://localhost:8080

=== FILES WITH LOW COVERAGE (< 80%) ===
- backend/app/db.py: 81% coverage
  Missing lines: 18-20, 28-30
  Likely: Error handling paths

=== COVERAGE IMPROVEMENT RECOMMENDATIONS ===

Files to improve (target: 80%+):
  - Identify untested functions and add tests
  - Test error handling paths
  - Test edge cases and boundary conditions

Testing best practices:
  - Write tests before implementation (TDD)
  - Test both success and failure paths
  - Use mocking for external dependencies
  - Keep tests fast and independent

Coverage goals:
  - Minimum: 80% coverage
  - Target: 90%+ coverage for business logic
  - Critical paths: 100% coverage
```

## Viewing the HTML Report

**Option 1: Open directly in browser**
```bash
# Linux
xdg-open htmlcov/index.html

# macOS
open htmlcov/index.html

# Windows
start htmlcov/index.html
```

**Option 2: Start a local HTTP server**
```bash
python -m http.server 8080 -d htmlcov
# Then visit: http://localhost:8080
```

## Understanding the Coverage Report

The HTML report shows:
- **Green lines**: Covered by tests
- **Red lines**: Not covered by tests
- **Yellow lines**: Partially covered (e.g., only one branch of an if statement)

**Color coding in terminal output:**
- **Green**: 90%+ coverage
- **Yellow**: 75-90% coverage
- **Red**: < 75% coverage

## Coverage Goals

**Minimum**: 80% overall coverage
**Target**: 90%+ coverage for business logic
**Critical paths**: 100% coverage (authentication, authorization, data validation)

## Safety Notes
- **Read-only operation**: Only generates reports, doesn't modify code
- **No side effects**: Safe to run anytime
- **Idempotent**: Can be run multiple times

## How to Run
```bash
/coverage-report                        # Full coverage report
/coverage-report -k "test_notes"        # Coverage for specific tests
/coverage-report backend/tests/notes/   # Coverage for specific directory
```

## Integration with CI/CD

Add to your CI pipeline:
```yaml
- name: Run tests with coverage
  run: pytest --cov=backend --cov-report=xml --cov-fail-under=80

- name: Upload coverage to Codecov
  uses: codecov/codecov-action@v3
  with:
    files: ./coverage.xml
```

## Troubleshooting

**Coverage shows 0% for new files:**
- Make sure pytest discovers your tests
- Check that test files follow the pattern `test_*.py`
- Verify tests are importing the code you're testing

**HTML report doesn't open:**
- Check that htmlcov/index.html was created
- Ensure you have a web browser installed
- Try the HTTP server method as an alternative

**Missing lines not showing in terminal:**
- The HTML report shows detailed line-by-line coverage
- Use the HTML report for detailed analysis
- Terminal output is a summary, not the full report
