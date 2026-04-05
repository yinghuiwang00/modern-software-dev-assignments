# Database Reset

Drop and recreate the database, then reseed from seed.sql.

## Intent
Reset the database to a clean state by deleting the existing database file and re-seeding with fresh data from `data/seed.sql`.

## Inputs
- `--dry-run`: Preview what would happen without actually doing it
- `--confirm`: Skip confirmation prompt (use with caution)

## Steps

1. **Check if app is running**:
   ```bash
   # Check if application is running on port 8000
   if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null ; then
     echo "Warning: Application is running on port 8000"
     echo "Please stop the application first (Ctrl+C in the terminal running 'make run')"
     exit 1
   fi
   ```

2. **Check for dry-run flag**:
   ```bash
   if [[ "$ARGUMENTS" == *"--dry-run"* ]]; then
     DRY_RUN=true
     echo "DRY RUN MODE - No changes will be made"
   else
     DRY_RUN=false
   fi
   ```

3. **Check if confirm flag**:
   ```bash
   if [[ "$ARGUMENTS" == *"--confirm"* ]]; then
     CONFIRM=true
   else
     CONFIRM=false
   fi
   ```

4. **Show current state**:
   ```bash
   DB_PATH="./data/app.db"

   if [ -f "$DB_PATH" ]; then
     DB_SIZE=$(du -h "$DB_PATH" | cut -f1)
     DB_MOD=$(stat -c %y "$DB_PATH" | cut -d' ' -f1,2 | cut -d'.' -f1)
     echo "Current database:"
     echo "  Path: $DB_PATH"
     echo "  Size: $DB_SIZE"
     echo "  Last modified: $DB_MOD"

     # Count records
     if [ "$DRY_RUN" = false ]; then
       NOTES_COUNT=$(sqlite3 "$DB_PATH" "SELECT COUNT(*) FROM notes;" 2>/dev/null || echo "0")
       ACTIONS_COUNT=$(sqlite3 "$DB_PATH" "SELECT COUNT(*) FROM action_items;" 2>/dev/null || echo "0")
       echo "  Records: $NOTES_COUNT notes, $ACTIONS_COUNT action items"
     fi
   else
     echo "No existing database found at $DB_PATH"
   fi

   # Check seed file
   SEED_FILE="./data/seed.sql"
   if [ -f "$SEED_FILE" ]; then
     echo ""
     echo "Seed file: $SEED_FILE"
     echo "  Size: $(du -h "$SEED_FILE" | cut -f1)"
   else
     echo ""
     echo "Warning: Seed file not found at $SEED_FILE"
   fi
   ```

5. **Ask for confirmation** (if not dry-run and not confirmed):
   ```bash
   echo ""
   if [ "$DRY_RUN" = true ]; then
     echo "This is a DRY RUN. No changes will be made."
   else
     if [ "$CONFIRM" = false ]; then
       echo "This will DELETE the existing database and create a fresh one."
       echo "All data will be lost!"
       echo ""
       echo "Are you sure you want to proceed? (yes/no):"
       # Confirmation handled by tool interaction
     else
       echo "Proceeding with database reset (--confirm flag used)..."
     fi
   fi
   ```

6. **Execute reset** (if confirmed):
   ```bash
   if [ "$DRY_RUN" = false ]; then
     echo ""
     echo "=== DELETING DATABASE ==="
     rm -f "$DB_PATH"
     echo "Deleted: $DB_PATH"

     echo ""
     echo "=== RE-CREATING DATABASE ==="
     make seed

     echo ""
     echo "=== VERIFYING NEW DATABASE ==="
     if [ -f "$DB_PATH" ]; then
       echo "Database created successfully!"

       NOTES_COUNT=$(sqlite3 "$DB_PATH" "SELECT COUNT(*) FROM notes;" 2>/dev/null || echo "0")
       ACTIONS_COUNT=$(sqlite3 "$DB_PATH" "SELECT COUNT(*) FROM action_items;" 2>/dev/null || echo "0")
       echo "Records: $NOTES_COUNT notes, $ACTIONS_COUNT action items"
     else
       echo "Error: Database was not created!"
       exit 1
     fi
   else
     echo ""
     echo "=== DRY RUN COMPLETE ==="
     echo "If confirmed, the following would happen:"
     echo "  1. Delete: $DB_PATH"
     echo "  2. Run: make seed"
     echo "  3. Verify new database"
   fi
   ```

7. **Output summary**:
   ```bash
   echo ""
   echo "=== SUMMARY ==="
   if [ "$DRY_RUN" = false ]; then
     echo "Database reset complete!"
     echo "You can now start the application with: make run"
   else
     echo "Dry run complete. Add --confirm flag to actually reset."
   fi
   ```

## Expected Output

**Example Dry Run Output:**
```
Database Reset
==============

Current database:
  Path: ./data/app.db
  Size: 8.0K
  Last modified: 2026-04-05 14:30:15
  Records: 3 notes, 2 action items

Seed file: ./data/seed.sql
  Size: 368 bytes

DRY RUN MODE - No changes will be made

This is a DRY RUN. No changes will be made.

=== DRY RUN COMPLETE ===
If confirmed, the following would happen:
  1. Delete: ./data/app.db
  2. Run: make seed
  3. Verify new database

=== SUMMARY ===
Dry run complete. Add --confirm flag to actually reset.
```

**Example Actual Reset Output:**
```
Database Reset
==============

Current database:
  Path: ./data/app.db
  Size: 8.0K
  Last modified: 2026-04-05 14:30:15
  Records: 3 notes, 2 action items

Seed file: ./data/seed.sql
  Size: 368 bytes

This will DELETE the existing database and create a fresh one.
All data will be lost!

Are you sure you want to proceed? (yes/no): yes

=== DELETING DATABASE ===
Deleted: ./data/app.db

=== RE-CREATING DATABASE ===
PYTHONPATH=. python -c "from backend.app.db import apply_seed_if_needed; apply_seed_if_needed()"

=== VERIFYING NEW DATABASE ===
Database created successfully!
Records: 2 notes, 2 action items

=== SUMMARY ===
Database reset complete!
You can now start the application with: make run
```

## Safety Notes
- **Stops if app is running**: Prevents resetting while app is using the database
- **Requires confirmation**: Must explicitly confirm before executing
- **Dry-run mode**: Preview changes before executing
- **Easy rollback**: Just re-run the reset (idempotent operation)

## How to Run
```bash
/db-reset               # Interactive: asks for confirmation
/db-reset --dry-run      # Preview changes without executing
/db-reset --confirm      # Skip confirmation (use with caution)
```

## Rollback
If you accidentally reset and need to restore data:
- If you have a backup: `cp data/app.db.backup data/app.db`
- If you use version control: Database changes should be managed via seed.sql and migrations
- If you need the old data: Check your recent database backups or migrations

## When to Use
- After schema changes that require a fresh database
- When seed.sql has been updated and you need fresh data
- During development when you want to start clean
- After testing destructive operations

## When NOT to Use
- When you need to preserve existing data
- When the application is running
- In production environments
- When you have unsaved important data
