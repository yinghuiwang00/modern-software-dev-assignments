# Tasks for Repo

## 1) Enable pre-commit and fix the repo
- [x] Install hooks: `pre-commit install`
- [x] Run: `pre-commit run --all-files`
- [x] Fix formatting/lint issues (black/ruff)
- Completed: Pre-commit hooks installed, code formatted with black

## 2) Add search endpoint for notes
- [x] Add/extend `GET /notes/search?q=...` (case-insensitive) using SQLAlchemy filters
- [x] Update `frontend/app.js` to use the search query
- [x] Add tests in `backend/tests/test_notes.py`
- Completed: Search endpoint exists and is tested (uses contains() for case-insensitive search)

## 3) Complete action item flow
- [x] Implement `PUT /action-items/{id}/complete` (already scaffolded)
- [x] Update UI to reflect completion (already wired) and extend test coverage
- Completed: Complete endpoint implemented, UI wired, test coverage extended

## 4) Improve extraction logic
- [x] Extend `backend/app/services/extract.py` to parse tags like `#tag` and return them
- [x] Add tests for the new parsing behavior
- [ ] (Optional) Expose `POST /notes/{id}/extract` that turns notes into action items
- Completed: Added extract_tags() function to parse hashtags, extract_action_items_with_tags() to extract action items with tags, comprehensive tests added

## 5) Notes CRUD enhancements
- [x] Add `PUT /notes/{id}` to edit a note (title/content)
- [x] Add `DELETE /notes/{id}` to delete a note
- [x] Update `frontend/app.js` to support edit/delete; add tests
- Completed: PUT and DELETE endpoints implemented, tests added, validation included

## 6) Request validation and error handling
- [x] Add simple validation rules (e.g., min lengths) to `schemas.py`
- [x] Return informative 400/404 errors where appropriate; add tests for validation failures
- Completed: Added validation to NoteCreate, NoteUpdate, ActionItemCreate schemas with min/max lengths, whitespace trimming, and error messages. Added comprehensive validation tests.

## 7) Docs drift check (manual for now)
- [x] Create/maintain a simple `API.md` describing endpoints and payloads
- [x] After each change, verify docs match actual OpenAPI (`/openapi.json`)
- Completed: Created API.md with all current endpoints, validation rules, and error responses
