# Pre-commit All Files

Run pre-commit hooks on all files in the repository to ensure code quality before committing.

## Intent
Run `pre-commit run --all-files` to execute all configured pre-commit hooks on all files, not just staged files. This is useful for cleaning up the entire codebase or ensuring consistency before a commit.

## Inputs
- `--fix`: Automatically fix issues where possible (pass to pre-commit)
- `--verbose`: Show detailed output from each hook

## Steps

1. **Check if pre-commit is installed**:
   ```bash
   if ! command -v pre-commit &> /dev/null; then
     echo "Error: pre-commit is not installed"
     echo ""
     echo "To install pre-commit:"
     echo "  pip install pre-commit"
     echo ""
     echo "To install hooks in this repository:"
     echo "  pre-commit install"
     exit 1
   fi
   ```

2. **Check if hooks are installed**:
   ```bash
   if [ ! -d ".git/hooks" ]; then
     echo "Warning: .git/hooks directory not found"
     echo "This may not be a git repository or hooks are not installed."
     echo ""
     echo "To install hooks:"
     echo "  pre-commit install"
   fi
   ```

3. **Parse arguments**:
   ```bash
   PRE_COMMIT_ARGS="--all-files"

   if [[ "$ARGUMENTS" == *"--fix"* ]]; then
     PRE_COMMIT_ARGS="$PRE_COMMIT_ARGS"
   fi

   if [[ "$ARGUMENTS" == *"--verbose"* ]]; then
     PRE_COMMIT_ARGS="$PRE_COMMIT_ARGS --verbose"
   fi
   ```

4. **Show pre-commit configuration**:
   ```bash
   echo "Pre-commit All Files"
   echo "===================="
   echo ""
   echo "Running pre-commit hooks with: pre-commit run $PRE_COMMIT_ARGS"
   echo ""

   if [ -f ".pre-commit-config.yaml" ]; then
     echo "Configured hooks:"
     grep -A 2 "^  - repo:" .pre-commit-config.yaml | grep -E "(^\s+- repo:|^\s+id:)" | sed 's/^[[:space:]]*/  /'
     echo ""
   else
     echo "Warning: .pre-commit-config.yaml not found"
     echo ""
   fi
   ```

5. **Run pre-commit**:
   ```bash
   echo "=== RUNNING PRE-COMMIT HOOKS ==="
   echo ""

   pre-commit run $PRE_COMMIT_ARGS

   EXIT_CODE=$?
   ```

6. **Handle results**:
   ```bash
   echo ""
   echo "=== RESULTS ==="

   if [ $EXIT_CODE -eq 0 ]; then
     echo "✓ All pre-commit hooks passed!"
     echo ""
     echo "Your code is ready to commit."
     echo ""
     echo "Next steps:"
     echo "  git add ."
     echo "  git commit -m 'Your commit message'"
   else
     echo "✗ Some pre-commit hooks failed"
     echo ""
     echo "Please fix the issues above and run again:"
     echo "  /pre-commit-all"
     echo ""
     echo "Or use /format-lint to fix formatting and linting issues:"
     echo "  /format-lint"
     exit 1
   fi
   ```

7. **Show summary**:
   ```bash
   echo ""
   echo "=== SUMMARY ==="
   echo "Hooks run: $(grep -c "^  - id:" .pre-commit-config.yaml 2>/dev/null || echo "unknown")"
   echo "Status: $([ $EXIT_CODE -eq 0 ] && echo "PASSED" || echo "FAILED")"
   echo ""
   echo "Files checked: all files in repository"
   echo ""
   echo "Note: This runs hooks on ALL files, not just staged files."
   echo "For staged files only, run: pre-commit run"
   ```

## Expected Output

**Example Success Output:**
```
Pre-commit All Files
====================

Running pre-commit hooks with: pre-commit run --all-files

Configured hooks:
  - repo: https://github.com/psf/black
    id: black
  - repo: https://github.com/astral-sh/ruff-pre-commit
    id: ruff

=== RUNNING PRE-COMMIT HOOKS ===
black....................................................................Passed
ruff.....................................................................Passed

=== RESULTS ===
✓ All pre-commit hooks passed!

Your code is ready to commit.

Next steps:
  git add .
  git commit -m 'Your commit message'

=== SUMMARY ===
Hooks run: 2
Status: PASSED

Files checked: all files in repository

Note: This runs hooks on ALL files, not just staged files.
For files in staging area only, run: pre-commit run
```

**Example with Fixes:**
```
Pre-commit All Files
====================

Running pre-commit hooks with: pre-commit run --all-files

Configured hooks:
  - repo: https://github.com/psf/black
    id: black
  - repo: https://github.com/astral-sh/ruff-pre-commit
    id: ruff

=== RUNNING PRE-COMMIT HOOKS ===
black.................................................................Failed
- hook id: black
- exit code: 1
- files were modified by this hook

reformatted backend/app/routers/notes.py
reformatted backend/app/routers/action_items.py

ruff.....................................................................Passed

=== RESULTS ===
✗ Some pre-commit hooks failed

Please fix the issues above and run again:
  /pre-commit-all

Or use /format-lint to fix formatting and linting issues:
  /format-lint

=== SUMMARY ===
Hooks run: 2
Status: FAILED
```

## Safety Notes
- **Reads all files**: Scans entire repository
- **Auto-fixes where possible**: Some hooks (black, ruff) automatically fix issues
- **Non-destructive**: Only modifies code style, not logic
- **Easy rollback**: Use git to revert if needed

## How to Run
```bash
/pre-commit-all          # Run all hooks on all files
/pre-commit-all --fix    # Run hooks (hooks auto-fix where possible)
/pre-commit-all --verbose # Run with verbose output
```

## Pre-commit Configuration

The `.pre-commit-config.yaml` file in this repository includes:
- **black**: Python code formatter
- **ruff**: Python linter

To add more hooks, edit `.pre-commit-config.yaml`.

## Installing Pre-commit

```bash
# Install pre-commit
pip install pre-commit

# Install hooks in this repository
pre-commit install

# Hooks will now run automatically before each commit
```

## Integration with Git Workflow

**Option 1: Automatic hooks (recommended)**
```bash
# Install hooks once
pre-commit install

# Now hooks run automatically before each commit
git add .
git commit -m "Your message"
```

**Option 2: Manual hooks**
```bash
# Run hooks manually before committing
/pre-commit-all

git add .
git commit -m "Your message"
```

## Troubleshooting

**Hook fails but doesn't show why:**
```bash
pre-commit run --all-files --verbose
```

**Hook is slow:**
- Some hooks only need to run on changed files
- Run on staged files only: `pre-commit run`
- Consider removing slow hooks from config

**Pre-commit not found:**
```bash
pip install pre-commit
pre-commit install
```

## CI/CD Integration

Add to your CI pipeline:
```yaml
- name: Run pre-commit
  run: pre-commit run --all-files
```

## Rollback

If pre-commit made unwanted changes:
```bash
# View changes
git diff

# Revert all changes
git checkout -- .

# Revert specific file
git checkout -- path/to/file
```
