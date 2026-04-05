# Format and Lint

Run code formatting and linting to ensure code quality and consistency.

## Intent
Run `make format` and `make lint` in sequence to ensure code is properly formatted and passes all linting rules.

## Inputs
- `$ARGUMENTS`: Optional file paths or directories to format/lint (defaults to entire project)
  - Example: `backend/app/routers/notes.py`
  - Example: `backend/`

## Steps

1. **Parse arguments**:
   ```bash
   TARGET="${ARGUMENTS:-.}"

   echo "Running format and lint on: $TARGET"
   ```

2. **Run formatting**:
   ```bash
   echo ""
   echo "=== FORMATTING ==="
   echo "Running black..."
   black $TARGET

   echo ""
   echo "Running ruff fix..."
   ruff check $TARGET --fix
   ```

3. **Run linting**:
   ```bash
   echo ""
   echo "=== LINTING ==="
   echo "Running ruff check..."
   ruff check $TARGET

   if [ $? -ne 0 ]; then
     echo ""
     echo "Lint issues found! Please fix them before committing."
     exit 1
   else
     echo ""
     echo "All lint checks passed!"
   fi
   ```

4. **Output summary**:
   - List of files formatted
   - Number of lint issues fixed
   - Final lint status
   - Next steps (if issues remain)

## Expected Output

**Example Success Output:**
```
Format and Lint
===============

Running format and lint on: backend/app/routers/notes.py

=== FORMATTING ===
Running black...
reformatted backend/app/routers/notes.py

All done! ✨ 🍰 ✨
1 file reformatted.

Running ruff fix...
Found 1 error (1 fixed, 0 remaining).

=== LINTING ===
Running ruff check...
All checks passed!

Summary:
- 1 file formatted by black
- 1 issue fixed by ruff
- All lint checks passed

You're ready to commit! 🎉
```

**Example with Issues:**
```
Format and Lint
===============

Running format and lint on: backend/

=== FORMATTING ===
Running black...
reformatted backend/app/routers/notes.py
reformatted backend/app/routers/action_items.py

All done! ✨ 🍰 ✨
2 files reformatted.

Running ruff check...
Found 3 errors (2 fixed, 1 remaining).

=== LINTING ===
Running ruff check...
backend/app/routers/notes.py:47:5: F821 Undefined name 'undefined_var'

Summary:
- 2 files formatted by black
- 2 issues fixed by ruff
- 1 lint error remaining

Remaining issues:
- backend/app/routers/notes.py:47:5 - Undefined name 'undefined_var'

Please fix the remaining lint issue before committing.
```

## Safety Notes
- **Non-destructive**: Formatting and linting only modify code style
- **Auto-fix**: Ruff automatically fixes many issues
- **Explicit confirmation needed for commits**: This command doesn't commit
- **Easy rollback**: Use git to revert if needed

## How to Run
```bash
/format-lint                      # Format and lint entire project
/format-lint backend/             # Format and lint only backend/
/format-lint backend/app/*.py     # Format and lint specific files
```

## Rollback
If formatting introduced issues, use git to revert:
```bash
git diff                  # View changes
git checkout -- .         # Revert all changes
git checkout -- path/to/file  # Revert specific file
```

## Integration with Git Workflow
This command is designed to be run before commits:
```bash
# 1. Make your changes
# 2. Run format and lint
/format-lint

# 3. If all checks pass, commit
git add .
git commit -m "Your commit message"
```

## Pre-commit Hook Integration
This command can be used with pre-commit hooks. The `.pre-commit-config.yaml` already includes black and ruff hooks. Install them with:
```bash
pre-commit install
```

Then pre-commit will automatically run these checks before each commit.
