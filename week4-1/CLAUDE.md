# Week 4 Repository Guidance

This file provides repository-specific guidance for working with the week4 starter application.

## Code Navigation and Entry Points

### Running the Application
- **Start the app**: `make run` (starts on http://localhost:8000)
- **API documentation**: http://localhost:8000/docs (FastAPI auto-generated)
- **OpenAPI spec**: http://localhost:8000/openapi.json
- **Frontend**: http://localhost:8000 (serves static HTML/JS/CSS)

### Codebase Structure
```
backend/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── models.py            # SQLAlchemy models (Note, ActionItem)
│   ├── schemas.py           # Pydantic schemas (validation, serialization)
│   ├── db.py                # Database connection and session management
│   ├── routers/
│   │   ├── notes.py         # Notes API endpoints
│   │   └── action_items.py  # Action items API endpoints
│   └── services/
│       └── extract.py       # Action item extraction logic
├── tests/
│   ├── conftest.py          # Pytest fixtures (TestClient, test DB)
│   ├── test_notes.py        # Notes endpoint tests
│   ├── test_action_items.py # Action items endpoint tests
│   └── test_extract.py      # Extraction logic tests
frontend/
├── index.html               # Main HTML page
├── app.js                   # Frontend JavaScript
└── styles.css               # Styles
data/
└── seed.sql                 # Database seed data
docs/
├── TASKS.md                 # Development tasks to implement
├── API.md                   # API documentation (manually maintained)
└── IMPLEMENTATION_PLAN.md   # Week 4 assignment implementation plan
```

### Database
- **Database file**: `data/app.db` (SQLite)
- **Seeding**: Automatic on first run via `backend/app/db.py:apply_seed_if_needed()`
- **Seed data**: `data/seed.sql`
- **Reseed**: Delete `data/app.db` and restart, or run `make seed`

### Testing
- **Test location**: `backend/tests/`
- **Test runner**: `make test` (runs pytest)
- **Test fixtures**: `backend/tests/conftest.py` provides in-memory SQLite DB and TestClient
- **Coverage**: `pytest --cov=backend --cov-report=html`

## Style and Safety Guardrails

### Tooling
- **Formatting**: `black .` (Python formatter)
- **Linting**: `ruff check . --fix` (fast Python linter)
- **Testing**: `pytest -q backend/tests`
- **Pre-commit**: `pre-commit run --all-files` (if hooks installed)

### Safe Commands to Run
- `make run` - Start development server
- `make test` - Run test suite
- `make format` - Format code with black and fix ruff issues
- `make lint` - Check code with ruff
- `make seed` - Re-seed database

### Commands to Avoid (or Use with Caution)
- **Destructive DB operations**: Never drop tables without confirmation
- **Direct DB manipulation**: Prefer API endpoints or SQLAlchemy, never raw SQL on production data
- **Hardcoded secrets**: Use environment variables (see `.env.example` if present)
- **Force commits**: Avoid `git push --force` without explicit approval

### Lint/Test Gates
- All code must pass `make format` before commits
- All tests must pass `make test` before commits
- No critical or high lint errors from `make lint` before commits
- Pre-commit hooks should run automatically if installed (`pre-commit install`)

## Workflow Snippets

### When Adding a New API Endpoint
1. Write a failing test first in `backend/tests/test_*.py`
2. Run `make test` to verify the test fails
3. Implement the endpoint in `backend/app/routers/*.py`
4. Add/update Pydantic schemas in `backend/app/schemas.py` if needed
5. Update models in `backend/app/models.py` if schema change needed
6. Run `make test` to verify all tests pass
7. Run `make format` and `make lint` to ensure code quality
8. Update documentation in `docs/API.md`
9. Commit changes with descriptive message

### When Modifying Database Schema
1. Update the model class in `backend/app/models.py`
2. Update Pydantic schemas in `backend/app/schemas.py`
3. Update seed data in `data/seed.sql` if needed
4. Delete `data/app.db` to trigger re-seeding, or run `make seed`
5. Write/update tests to cover the schema change
6. Run `make test` to verify
7. Update routers in `backend/app/routers/*.py` to use new schema
8. Run `make format` and `make lint`
9. Update documentation

### When Adding Frontend Features
1. Add HTML elements to `frontend/index.html`
2. Add JavaScript logic to `frontend/app.js`
3. Add styles to `frontend/styles.css` if needed
4. Test the feature in browser at http://localhost:8000
5. Write E2E tests if critical user flow (optional)
6. Run `make format` and `make lint` on any modified Python files
7. Update documentation if API usage changed

### When Running Tests
- Use `make test` for quick feedback during development
- Use `pytest -q backend/tests --maxfail=1 -x` to stop on first failure
- Use `pytest --cov=backend --cov-report=html` for coverage report
- Use `pytest -k "test_name"` to run specific tests
- Use `pytest -v` for verbose output

### Debugging Tips
- Check API docs at http://localhost:8000/docs for interactive testing
- Use `print()` statements for quick debugging (remove before commit)
- Check `data/app.db` with `sqlite3 data/app.db` for direct DB inspection
- Review browser console for frontend errors
- Check FastAPI logs for server-side errors

## Project-Specific Notes

### Current Features
- **Notes**: CRUD operations (Create, Read, List, Search)
- **Action Items**: Create, List, Complete endpoint
- **Extraction**: Simple action item extraction from text (lines ending with "!" or starting with "TODO:")

### Known Tasks to Implement
See `docs/TASKS.md` for the list of development tasks:
1. Enable pre-commit and fix the repo
2. Add search endpoint for notes (already exists, needs case-insensitive)
3. Complete action item flow (complete endpoint exists, needs UI updates)
4. Improve extraction logic (parse #tag support)
5. Notes CRUD enhancements (add PUT/DELETE)
6. Request validation and error handling
7. Docs drift check (maintain API.md)

### API Patterns
- All endpoints use `response_model` for type-safe responses
- Database errors raise `HTTPException` with appropriate status codes
- 404 errors for missing resources
- 201 status codes for successful creation
- PUT for updates, POST for creation, DELETE for deletion
