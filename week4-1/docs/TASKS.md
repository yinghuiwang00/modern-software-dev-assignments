# Tasks for Repo

## 1) ✅ Enable pre-commit and fix the repo **[COMPLETED]**
- ✅ Install hooks: `pre-commit install`
- ✅ Run: `pre-commit run --all-files`
- ✅ Fix any formatting/lint issues (black/ruff)

### How completed:
- Used command: `/pre-commit-all` to run pre-commit hooks
- Used command: `/format-lint` to fix formatting and linting issues
- Verified: `pre-commit run --files backend/**/*.py` → All checks passed
- Note: Project-wide pre-commit checks still show errors in other week directories (week1, week2, week3-2, week6), but week4-1 directory is clean

```
  步骤 3: 运行所有预提交检查

  使用命令：/pre-commit-all
  （这会运行 pre-commit run --all-files）

  步骤 4: 如果有格式化/lint问题

  使用命令：/format-lint
  （这会运行 make format 和 make lint）

  步骤 5: 重复步骤 3-4 直到通过

  确保所有检查都通过后，任务完成。
```

## 2) ✅ Add search endpoint for notes **[COMPLETED]**
- ✅ Add/extend `GET /notes/search?q=...` (case-insensitive) using SQLAlchemy filters
- ✅ Update `frontend/app.js` to use the search query
- ✅ Add tests in `backend/tests/test_notes.py`

### How completed:
- Used **TestAgent** to write case-insensitive search tests
- Used **CodeAgent** to update backend to use `ilike()` for case-insensitive search
- Used **TestAgent** to verify all tests pass (6/6, 88% coverage)
- Used **CodeAgent** to add search UI to frontend (input, button, clear button)
- Used **CodeAgent** to add `searchNotes()` function with Enter key support
- Used **/format-lint** to format and lint code
- Used **/tests** to verify all tests pass
- Used **/coverage-report** to check coverage (88%)
- Used **DocsAgent** (/docs-sync) to create `docs/API.md` with search endpoint documentation
- Updated `docs/TASKS.md` to mark task as completed

### Files modified:
- `backend/app/routers/notes.py` - Updated search to use `ilike()`
- `backend/tests/test_notes.py` - Added 3 case-insensitive search tests
- `frontend/index.html` - Added search input, button, and clear button
- `frontend/app.js` - Added `searchNotes()` function and event listeners
- `docs/API.md` - Created new API documentation

## 3) ✅ Complete action item flow **[COMPLETED]**
- ✅ Implement `PUT /action-items/{id}/complete` (already scaffolded)
- ✅ Update UI to reflect completion (already wired) and extend test coverage

### How completed:
- Verified backend implementation: `PUT /action-items/{id}/complete` endpoint correctly implemented
- Used **TestAgent** to add `test_complete_action_item_not_found` test for 404 error path
- Used **CodeAgent** to verify backend implementation and run `/format-lint`
- Used **TestAgent** to verify test coverage with `/tests` and `/coverage-report`
- Frontend UI already had completion functionality (Complete button)
- Verified action_items.py coverage reached 100% (from 96%)
- Used **DocsAgent** (/docs-sync) to verify documentation is up to date
- Updated `docs/TASKS.md` to mark task as completed

### Files modified:
- `backend/tests/test_action_items.py` - Added `test_complete_action_item_not_found` test
- `docs/TASKS.md` - Updated to mark task as completed

### Test Results:
- All 7 tests passing
- Overall coverage: 89%
- action_items.py coverage: 100%

## 4) ✅ Improve extraction logic **[COMPLETED]**
- ✅ Extend `backend/app/services/extract.py` to parse tags like `#tag` and return them
- ✅ Add tests for the new parsing behavior
- ✅ (Optional) Expose `POST /notes/{id}/extract` that turns notes into action items

### How completed:
- Used **TestAgent** to write tag parsing tests (4 tests)
- Used **CodeAgent** to implement tag parsing logic in extract.py
- Used **TestAgent** to verify implementation and coverage (100% on extract.py)
- Used **CodeAgent** to add `POST /notes/{note_id}/extract` API endpoint
- Used **CodeAgent** to add `ExtractResponse` schema
- Used **/format-lint** to format and lint code
- Used **/tests** to verify all tests pass
- Used **/coverage-report** to check coverage (92% overall, 100% on extract.py)
- Used **DocsAgent** (/docs-sync) to update docs/API.md with new endpoint
- Updated `docs/TASKS.md` to mark task as completed

### Files modified:
- `backend/app/services/extract.py` - Added tag parsing logic, returns `[{"description": str, "tags": list[str]}]`
- `backend/tests/test_extract.py` - Added 3 new tests for tag parsing
- `backend/app/schemas.py` - Added `ExtractResponse` schema
- `backend/app/routers/notes.py` - Added `POST /notes/{note_id}/extract` endpoint
- `frontend/index.html` - Added extraction results container
- `frontend/app.js` - Added `extractActionItems()` and `createActionItem()` functions
- `docs/API.md` - Added documentation for extract endpoint
- `docs/TASKS.md` - Updated to mark task as completed

### Test Results:
- All 10 tests passing
- Overall coverage: 92%
- extract.py coverage: 100%

### Features Implemented:
- Multi-tag extraction: `#urgent #critical #production` → tags: `["urgent", "critical", "production"]`
- Pattern prefix cleaning: `#urgent: Fix the bug` → description: `"Fix the bug #critical"`, tags: `["urgent", "critical"]`
- Tag preservation in description: `- TODO: write tests #important` → description: `"TODO: write tests #important"`, tags: `["important"]`
- API endpoint: `POST /notes/{note_id}/extract` - Extracts action items from note content

## 5) ✅ Notes CRUD enhancements **[COMPLETED]**
- ✅ Add `PUT /notes/{id}` to edit a note (title/content)
- ✅ Add `DELETE /notes/{id}` to delete a note
- ✅ Update `frontend/app.js` to support edit/delete; add tests

### How completed:
- Used **TestAgent** to write edit and delete note tests (2 new tests)
- Used **CodeAgent** to implement PUT and DELETE endpoints in `backend/app/routers/notes.py`
- Used **TestAgent** to verify backend implementation (93% coverage, 14/14 tests passing)
- Used **CodeAgent** to update `frontend/app.js`:
  - Added Edit and Delete buttons to each note in `loadNotes()`
  - Added `editNote(noteId)` function using `prompt()` for user input
  - Added `deleteNote(noteId)` function using `confirm()` dialog
- Ran `/format-lint` to format and lint code
- Ran `/tests` to verify all tests pass
- Used **DocsAgent** (/docs-sync) to update docs/API.md with PUT and DELETE endpoints
- Updated `docs/TASKS.md` to mark task as completed

### Files modified:
- `backend/app/schemas.py` - Added `NoteUpdate` schema
- `backend/app/routers/notes.py` - Added `PUT /{note_id}` and `DELETE /{note_id}` endpoints
- `backend/tests/test_notes.py` - Added 2 new tests for edit and delete functionality
- `frontend/app.js` - Updated `loadNotes()` function with Edit and Delete buttons
- `docs/API.md` - Added PUT and DELETE endpoint documentation
- `docs/TASKS.md` - Updated to mark task as completed

### Test Results:
- All 14/14 tests passing (including 2 new tests)
- Overall coverage: 93%
- notes.py coverage: 92%

### Features Implemented:
- Edit note functionality with user input (title and content)
- Delete note functionality with confirmation dialog
- Buttons added to each note for quick access
- All changes preserve existing functionality (create, search, extract action items)

## 6) Request validation and error handling
- Add simple validation rules (e.g., min lengths) to `schemas.py`
- Return informative 400/404 errors where appropriate; add tests for validation failures

## 7) Docs drift check (manual for now)
- Create/maintain a simple `API.md` describing endpoints and payloads
- After each change, verify docs match actual OpenAPI (`/openapi.json`)
