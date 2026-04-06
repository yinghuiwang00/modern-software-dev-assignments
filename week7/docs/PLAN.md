
     Context

     This assignment focuses on practicing agent-driven development and comparing manual code review with AI-assisted code review using
      Graphite Diamond. The assignment requires implementing 4 tasks, each with a 1-shot AI prompt, followed by manual review, PR
     creation, and Graphite Diamond AI review.

     The existing codebase is a FastAPI application with:
     - Notes API (CRUD operations with pagination and sorting)
     - Action Items API (CRUD with completion tracking)
     - SQLAlchemy database models (Note, ActionItem)
     - Basic action item extraction service
     - Pytest-based test suite

     Implementation Plan

     User Preferences:
     - AI Tool: Claude (current session)
     - Task Order: Sequential (1→2→3→4)

     The 4 tasks will be implemented sequentially, each following the same workflow:
     1. Create a separate branch
     2. Use 1-shot Claude prompt to implement the task
     3. Manually review the changes line-by-line
     4. Fix issues and add commit messages
     5. Open a PR with detailed description
     6. Use Graphite Diamond for AI review
     7. Document results in writeup.md

     ---
     Task 1: Add More Endpoints and Validations

     Files to modify:
     - backend/app/routers/notes.py - Add DELETE endpoint
     - backend/app/routers/action_items.py - Add DELETE endpoint
     - backend/app/schemas.py - Add field validators

     Approach:
     - Add DELETE /notes/{note_id} endpoint
     - Add DELETE /action-items/{item_id} endpoint
     - Add PUT endpoint for full note updates
     - Add field validators using Pydantic (e.g., title length constraints, content non-empty)
     - Add validation for pagination parameters (skip >= 0, limit between 1-200)

     Existing patterns to reuse:
     - HTTP 404 error handling pattern from existing endpoints
     - Pydantic BaseModel schema pattern in schemas.py
     - Session management via db.get() pattern

     ---
     Task 2: Extend Extraction Logic

     Files to modify:
     - backend/app/services/extract.py - Enhance extraction algorithm

     Approach:
     - Add regex-based pattern matching for more formats
     - Support multiple action item formats:
       - [ ] checkbox format
       - * or - bullet points with action verbs
       - Priority indicators (high, medium, low)
       - Due date parsing
     - Add confidence scoring for extracted items
     - Return structured data (not just strings)

     Existing patterns to reuse:
     - Current simple string-based extraction in extract.py
     - List return type pattern

     ---
     Task 3: Add New Model and Relationships

     Files to modify:
     - backend/app/models.py - Add new models
     - backend/app/schemas.py - Add new schemas
     - backend/app/routers/notes.py - Add tag-related endpoints
     - backend/app/db.py - No changes needed (SQLAlchemy handles relationships)

     Approach:
     - Add Tag model (id, name, color, timestamps)
     - Create Many-to-Many relationship: Note ↔ Tag
     - Add NoteTag association table
     - Add endpoints:
       - GET/POST /tags/ - list and create tags
       - POST /notes/{note_id}/tags/ - add tag to note
       - DELETE /notes/{note_id}/tags/{tag_id} - remove tag from note
     - Update NoteRead schema to include tags

     Existing patterns to reuse:
     - TimestampMixin in models.py
     - Base declarative base pattern
     - Pydantic schemas with from_attributes = True config

     ---
     Task 4: Improve Tests for Pagination and Sorting

     Files to modify:
     - backend/tests/test_notes.py - Add comprehensive pagination/sorting tests
     - backend/tests/test_action_items.py - Add comprehensive pagination/sorting tests

     Approach:
     Add tests for:
     - Pagination edge cases:
       - skip=0, limit variations
       - skip > total count
       - Negative skip values (should error)
       - limit > 200 (should cap at 200)
       - Empty result sets
     - Sorting edge cases:
       - Valid sort fields (title, created_at, updated_at)
       - Invalid sort fields (should default to created_at)
       - Ascending vs descending
       - Sort with empty results
     - Combined pagination + sort + filter
     - Performance: large datasets (create 1000+ items, test pagination)

     Existing patterns to reuse:
     - Test client fixture in conftest.py
     - Test pattern: create, read, assert structure
     - Query parameter passing in tests

     ---
     Workflow for Each Task

     For each of the 4 tasks:

     1. Create branch
     git checkout -b task-{N}-{description}
     2. 1-shot AI prompt implementation
       - Use a single comprehensive prompt to implement the entire task
       - Let AI make design decisions within constraints
     3. Manual review
       - Read through all changes line-by-line
       - Check for:
           - Correctness (does it work?)
         - Performance (any N+1 queries, inefficiencies?)
         - Security (input validation, SQL injection, XSS?)
         - Naming (clear, consistent?)
         - Test gaps (edge cases covered?)
         - API shape (RESTful, consistent?)
         - UX (appropriate error messages?)
       - Fix any issues found
       - Add explanatory commit messages
     4. Create PR
       - Push branch to remote
       - Create PR with:
           - Clear description of problem and approach
         - Summary of testing (commands and results)
         - Notable tradeoffs/limitations
         - Follow-ups if any
     5. Graphite Diamond AI review
       - Enable Graphite Diamond on the PR
       - Let AI generate review comments
       - Review AI comments vs manual review
     6. Document results
       - Add PR link and description to writeup.md
       - Note Graphite Diamond review findings

     ---
     Final Deliverable

     Update writeup.md with:
     - 4 PR links with descriptions
     - Graphite Diamond AI review summaries
     - Brief reflection comparing manual vs AI reviews:
       - Types of comments typically made
       - Comparison with Graphite's comments
       - Examples of when AI was better/worse
       - Comfort level with AI reviews and heuristics

     ---
     Verification

     For each task, verify:
     1. All tests pass: pytest -v
     2. Manual testing of new endpoints
     3. Code review completed
     4. PR created and pushed
     5. Graphite Diamond review generated
     6. writeup.md updated
