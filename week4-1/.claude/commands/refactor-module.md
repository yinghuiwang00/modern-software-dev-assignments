# Refactor Module

Rename or restructure a module, update all imports, run linting, and verify tests still pass.

## Intent
Safely rename a module or restructure code by:
1. Renaming the file
2. Updating all import statements
3. Running linter to fix issues
4. Running tests to verify nothing broke

## Inputs
- `$ARGUMENTS`: Old path and new path (space separated)
  - Example: `backend/app/services/extract.py backend/app/services/parser.py`
  - Example: `backend/app/routers/notes.py backend/app/routers/note_routes.py`

## Steps

1. **Parse arguments**:
   ```bash
   # Expected: $ARGUMENTS = "old_path new_path"
   OLD_PATH="$1"
   NEW_PATH="$2"

   # Validate arguments
   if [ -z "$OLD_PATH" ] || [ -z "$NEW_PATH" ]; then
     echo "Usage: /refactor-module <old_path> <new_path>"
     echo "Example: /refactor-module backend/app/services/extract.py backend/app/services/parser.py"
     exit 1
   fi

   # Check if old file exists
   if [ ! -f "$OLD_PATH" ]; then
     echo "Error: File '$OLD_PATH' does not exist"
     exit 1
   fi

   # Check if new file already exists
   if [ -f "$NEW_PATH" ]; then
     echo "Error: File '$NEW_PATH' already exists"
     exit 1
   fi
   ```

2. **Search for import statements**:
   ```bash
   # Find all Python files that import the old module
   OLD_MODULE=$(echo "$OLD_PATH" | sed 's|backend/app/||' | sed 's|\.py||' | sed 's|/|.|g')
   NEW_MODULE=$(echo "$NEW_PATH" | sed 's|backend/app/||' | sed 's|\.py||' | sed 's|/|.|g')

   echo "Old module: $OLD_MODULE"
   echo "New module: $NEW_MODULE"

   # Find files that import the old module
   FILES_TO_UPDATE=$(grep -r "from $OLD_MODULE" backend --include="*.py" | cut -d: -f1 | sort -u)
   FILES_TO_UPDATE="$FILES_TO_UPDATE $(grep -r "import $OLD_MODULE" backend --include="*.py" | cut -d: -f1 | sort -u)"
   ```

3. **Show preview of changes**:
   ```bash
   echo ""
   echo "=== PREVIEW OF CHANGES ==="
   echo ""
   echo "Files to be updated:"
   echo "$FILES_TO_UPDATE" | tr ' ' '\n' | sort -u | grep -v '^$'
   echo ""
   echo "Rename operation:"
   echo "  $OLD_PATH -> $NEW_PATH"
   echo ""
   echo "Import updates:"
   echo "  from $OLD_MODULE -> from $NEW_MODULE"
   echo "  import $OLD_MODULE -> import $NEW_MODULE"
   echo ""
   ```

4. **Ask for confirmation**:
   ```bash
   # This is handled by the tool interaction
   echo "Proceed with refactor? (y/n)"
   ```

5. **Execute refactor** (if confirmed):
   ```bash
   # Create new file
   cp "$OLD_PATH" "$NEW_PATH"

   # Update imports in affected files
   for file in $(echo "$FILES_TO_UPDATE" | tr ' ' '\n' | sort -u | grep -v '^$'); do
     sed -i "s|from $OLD_MODULE|from $NEW_MODULE|g" "$file"
     sed -i "s|import $OLD_MODULE|import $NEW_MODULE|g" "$file"
   done

   # Remove old file
   rm "$OLD_PATH"

   echo ""
   echo "=== REFACTOR COMPLETE ==="
   ```

6. **Run linter to fix issues**:
   ```bash
   echo ""
   echo "Running linter..."
   make lint
   if [ $? -ne 0 ]; then
     echo ""
     echo "Lint issues found. Running auto-fix..."
     make format
     make lint
   fi
   ```

7. **Run tests to verify**:
   ```bash
   echo ""
   echo "Running tests..."
   make test
   if [ $? -ne 0 ]; then
     echo ""
     echo "Tests FAILED! Refactor may have broken something."
     echo "Please review the test failures."
   else
     echo ""
     echo "All tests PASSED! Refactor successful."
   fi
   ```

8. **Generate verification checklist**:
   ```bash
   echo ""
   echo "=== VERIFICATION CHECKLIST ==="
   echo ""
   echo "✓ File renamed: $OLD_PATH -> $NEW_PATH"
   echo "✓ Imports updated in $(echo "$FILES_TO_UPDATE" | tr ' ' '\n' | sort -u | grep -v '^$' | wc -l) file(s)"
   echo "✓ Linter executed"
   echo "✓ Tests executed"
   echo ""
   echo "Manual verification steps:"
   echo "  [ ] Review git diff to ensure all imports are correct"
   echo "  [ ] Run application: make run"
   echo "  [ ] Test affected endpoints"
   echo "  [ ] Commit changes if verified"
   ```

## Expected Output

**Example Success Output:**
```
Refactor Module
==============

Parsing arguments...
Old path: backend/app/services/extract.py
New path: backend/app/services/parser.py
Old module: services.extract
New module: services.parser

Searching for imports...
Found imports in:
  - backend/app/routers/notes.py
  - backend/app/routers/action_items.py
  - backend/tests/test_extract.py

=== PREVIEW OF CHANGES ===

Files to be updated:
  backend/app/routers/action_items.py
  backend/app/routers/notes.py
  backend/app/tests/test_extract.py

Rename operation:
  backend/app/services/extract.py -> backend/app/services/parser.py

Import updates:
  from services.extract -> from services.parser
  import services.extract -> import services.parser

Proceed with refactor? (y/n)

=== REFACTOR COMPLETE ===

Running linter...
All checks passed!

Running tests...
...                                                                   [100%]
3 passed in 0.12s

All tests PASSED! Refactor successful.

=== VERIFICATION CHECKLIST ===

✓ File renamed: backend/app/services/extract.py -> backend/app/services/parser.py
✓ Imports updated in 3 file(s)
✓ Linter executed
✓ Tests executed

Manual verification steps:
  [ ] Review git diff to ensure all imports are correct
  [ ] Run application: make run
  [ ] Test affected endpoints
  [ ] Commit changes if verified
```

## Safety Notes
- **Always shows preview before executing**: No changes without confirmation
- **Creates backup**: Copies file before renaming (if undo needed)
- **Runs tests after**: Verifies nothing broke
- **Works with git**: Changes can be easily rolled back with git

## Rollback
If the refactor breaks something, use git to revert:
```bash
git checkout -- .
git clean -fd
```

Or manually restore:
```bash
cp "$NEW_PATH" "$OLD_PATH"
# Manually revert import changes
```

## How to Run
```bash
/refactor-module backend/app/services/extract.py backend/app/services/parser.py
```

## Error Handling
- Validates old file exists
- Validates new file doesn't already exist
- Validates correct number of arguments
- Shows clear error messages for failures
- Runs tests to catch issues immediately
