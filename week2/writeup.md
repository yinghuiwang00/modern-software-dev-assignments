# Week 2 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## INSTRUCTIONS

Fill out all of the `TODO`s in this file.

## SUBMISSION DETAILS

Name: **TODO** \
SUNet ID: **TODO** \
Citations: **TODO**

This assignment took me about **TODO** hours to do. 


## YOUR RESPONSES
For each exercise, please include what prompts you used to generate the answer, in addition to the location of the generated response. Make sure to clearly add comments in your code documenting which parts are generated.

### Exercise 1: Scaffold a New Feature
Prompt: 
```
TODO
``` 

Generated Code Snippets:
```
TODO: List all modified code files with the relevant line numbers.
```

### Exercise 2: Add Unit Tests
Prompt: 
```
Prompt: 
```
Write comprehensive unit tests for the `extract_action_items_llm()` function in `week2/app/services/extract.py`. The tests should be added to `week2/tests/test_extract.py`.

Requirements:
1. Mock the OpenAI/Zhipu API client to avoid actual API calls during testing
2. Use pytest as the testing framework (already configured in pyproject.toml)
3. Import the function: `from ..app.services.extract import extract_action_items_llm`

Test Cases to Cover:

1. **Bullet Lists Test** - Test extraction of bullet points with different formats:
   - Text containing "- [ ] Set up database"
   - Text containing "* implement API extract endpoint"
   - Text containing "1. Write tests"
   - Verify correct extraction of action items

2. **Keyword-Prefixed Lines Test** - Test extraction of lines with action keywords:
   - Text containing "todo: Review code"
   - Text containing "action: Fix bug"
   - Text containing "next: Deploy to production"
   - Verify correct extraction with keywords removed

3. **Empty Input Test** - Test handling of empty or whitespace-only input:
   - Empty string should return empty list
   - Whitespace-only string should return empty list

4. **JSON Array Parsing Test** - Test successful JSON array response from LLM:
   - Mock the API to return valid JSON: '["Action 1", "Action 2"]'
   - Verify correct parsing and return

5. **Fallback to Heuristic Test** - Test fallback when LLM returns invalid JSON:
   - Mock the API to return invalid JSON or plain text
   - Verify the function falls back to `extract_action_items()` heuristic extraction

6. **Markdown-wrapped JSON Test** - Test parsing of JSON wrapped in markdown code blocks:
   - Mock API to return: ```json\n["Action 1", "Action 2"]\n```
   - Verify correct parsing

7. **Mixed Content Test** - Test extraction from realistic meeting notes:
   - Bullet points
   - Action keywords
   - Narrative sentences mixed with action items

Make sure to:
- Use pytest's `unittest.mock` or `mocker` fixture for mocking
- Follow the existing test style in `test_extract.py`
- Include descriptive test names
- Add comments explaining what each test validates
- Ensure tests are isolated and don't depend on external services

``` 
``` 

Generated Code Snippets:
```
TODO: List all modified code files with the relevant line numbers.
```

### Exercise 3: Refactor Existing Code for Clarity
Prompt: 
```
Perform a comprehensive refactor of the backend code in the week2/app directory, focusing on the following areas:

## 1. API Contracts/Schemas (Priority: HIGH)

Current State:
- All endpoints use `Dict[str, Any]` for request/response
- No type safety or validation
- Inconsistent data shapes across endpoints

Requirements:
- Create Pydantic models for all API contracts in `week2/app/schemas.py`
- Define separate models for:
  * Request payloads (e.g., ExtractRequest, CreateNoteRequest, MarkDoneRequest)
  * Response payloads (e.g., ExtractResponse, NoteResponse, ActionItemResponse)
  * Database models (e.g., Note, ActionItem)
- Use proper types (str, int, bool, Optional, List) instead of Dict[str, Any]
- Add field validation (e.g., minimum length, required fields)
- Update all router endpoints to use these Pydantic models

## 2. Database Layer Cleanup (Priority: HIGH)

Current State:
- Raw SQLite queries scattered throughout db.py
- Direct use of sqlite3.Row makes type inference difficult
- No repository pattern or abstraction layer
- Mixed concerns: schema definition, connection management, business logic

Requirements:
- Extract repository classes or database models to separate files:
  * `week2/app/repositories/` or `week2/app/models/`
  * Create NoteRepository and ActionItemRepository classes
  * Use proper dataclasses or Pydantic models for database entities
- Consider adding SQLAlchemy for better ORM support (optional but recommended)
- Implement proper connection pooling/context management
- Separate database schema definition from business logic
- Add type hints to all database operations

## 3. App Lifecycle/Configuration (Priority: MEDIUM)

Current State:
- `init_db()` called at module import time in main.py (line 14)
- No FastAPI lifecycle events
- No configuration management

Requirements:
- Move `init_db()` call into FastAPI lifespan event:
  ```python
  @app.on_event("startup")
  async def startup_event():
      init_db()
Or use the newer context manager pattern:

lifespan_context = contextlib.asynccontextmanager
@lifespan_context
async def lifespan(app: FastAPI):
    # Startup
    init_db()
    yield
    # Shutdown (cleanup if needed)
Create a configuration module week2/app/config.py:
Use pydantic-settings for type-safe configuration
Define settings class with database path, API keys, etc.
Load from environment variables with defaults
Remove hardcoded paths and configuration values

## 4. Error Handling (Priority: MEDIUM)
Current State:

Basic HTTPException usage
No custom exception classes
Inconsistent error responses
No logging
Requirements:

Create custom exception classes in week2/app/exceptions.py:
DatabaseError, ValidationError, NotFoundError, etc.
Implement consistent error response format:
Use JSON response structure with error code, message, details
Add proper logging throughout the application:
Use Python's logging module
Configure log levels and formats
Log important operations and errors
Add validation for all user inputs (Pydantic handles this)

## 5. Code Organization (Priority: LOW)
Current State:

Some circular imports (e.g., from . import db in main.py)
Mixed concerns in files
No clear separation of layers
Requirements:

Improve module structure:

week2/app/
├── __init__.py
├── main.py                 # FastAPI app setup only
├── config.py               # Configuration management
├── dependencies.py         # FastAPI dependencies
├── exceptions.py           # Custom exceptions
├── schemas.py              # Pydantic models for API
├── models/                 # Database models
│   ├── __init__.py
│   ├── note.py
│   └── action_item.py
├── repositories/           # Data access layer
│   ├── __init__.py
│   ├── note_repository.py
│   └── action_item_repository.py
├── services/               # Business logic
│   ├── __init__.py
│   └── extract.py
└── routers/               # API endpoints
    ├── __init__.py
    ├── notes.py
    └── action_items.py
Resolve any circular import issues
Add docstrings to all public functions and classes
Implementation Guidelines
Refactor incrementally: Start with the highest priority items
Maintain backward compatibility: Ensure existing API contracts still work
Add tests: Write tests for new/refactored code
Follow Python best practices: Use type hints, PEP 8, docstrings
Document changes: Update writeup.md with all refactoring decisions
Files to Modify
week2/app/main.py - Add lifecycle events, remove module-level init
week2/app/db.py - Refactor into repositories/models
week2/app/routers/action_items.py - Use Pydantic schemas
week2/app/routers/notes.py - Use Pydantic schemas
Create new files: config.py, schemas.py, exceptions.py, models/, repositories/

##Success Criteria
✅ All endpoints use Pydantic models for request/response
✅ Database layer properly abstracted with repository pattern
✅ FastAPI lifecycle events properly configured
✅ Configuration loaded from environment/settings
✅ Consistent error handling across the application
✅ All tests pass after refactoring
✅ No circular imports
✅ Code is more maintainable and type-safe


---
``` 

Generated/Modified Code Snippets:
```
🎯 Completed Tasks:
1. API Contracts/Schemas ✅
Created week2/app/schemas.py with Pydantic models:
Request schemas: ExtractRequest, CreateNoteRequest, MarkDoneRequest
Response schemas: ExtractResponse, NoteResponse, ActionItemResponse, ExtractItemResponse, MarkDoneResponse
Database models: Note, ActionItem
All endpoints now use type-safe Pydantic models instead of Dict[str, Any]
Added field validation and proper type hints
2. Database Layer Cleanup ✅
Created repository pattern in week2/app/repositories/:
NoteRepository - handles all note database operations
ActionItemRepository - handles all action item database operations
Created week2/app/database.py for database initialization
Proper connection management with context managers
Comprehensive error handling and logging
Type hints throughout all database operations
3. App Lifecycle/Configuration ✅
Created week2/app/config.py with Pydantic settings:
Type-safe configuration management
Environment variable loading with defaults
Configuration validation
Refactored main.py to use FastAPI lifespan events:
Database initialization moved to startup event
Proper application shutdown handling
Removed module-level init_db() call
4. Error Handling ✅
Created week2/app/exceptions.py with custom exceptions:
BaseApplicationError, DatabaseError, ValidationError
NotFoundError, ServiceError, ConfigurationError
Consistent error response format with proper HTTP status codes
Comprehensive exception handling in all routers
5. Code Organization ✅
Improved module structure:

week2/app/
├── main.py (FastAPI app setup)
├── config.py (Configuration)
├── database.py (Database initialization)
├── exceptions.py (Custom exceptions)
├── schemas.py (Pydantic models)
├── repositories/ (Data access layer)
│   ├── __init__.py
│   ├── note_repository.py
│   └── action_item_repository.py
├── services/ (Business logic)
│   └── extract.py
└── routers/ (API endpoints)
    ├── notes.py
    └── action_items.py
Resolved circular imports
Added docstrings to all public functions and classes
6. Logging ✅
Added comprehensive logging throughout the application:
Configurable log level via environment variables
Structured logging format
Application lifecycle logging
Database operation logging
API endpoint logging
Error logging with context
✅ Success Criteria Met:
✅ All endpoints use Pydantic models for request/response
✅ Database layer properly abstracted with repository pattern
✅ FastAPI lifecycle events properly configured
✅ Configuration loaded from environment/settings
✅ Consistent error handling across application
✅ All 10 tests pass after refactoring
✅ No circular imports
✅ Code is more maintainable and type-safe
📁 Files Created:
week2/app/schemas.py - Pydantic models
week2/app/exceptions.py - Custom exceptions
week2/app/config.py - Configuration management
week2/app/database.py - Database initialization
week2/app/repositories/ - Repository classes
🔄 Files Modified:
week2/app/main.py - Added lifespan events and logging
week2/app/routers/action_items.py - Updated to use Pydantic schemas and repositories
week2/app/routers/notes.py - Updated to use Pydantic schemas and repositories
week2/app/services/extract.py - Added logging and graceful API key handling
🗑️ Files Removed:
week2/app/db.py - Replaced by repository pattern

```


### Exercise 4: Use Agentic Mode to Automate a Small Task
Prompt: 
```
Implement two small features to enhance the Action Item Extractor application. These features demonstrate how AI agents can automate development tasks while following established patterns.

## Task 1: Create Dedicated LLM Extraction Endpoint

**Current State:**
- Existing endpoint: `POST /action-items/extract` with `use_llm` parameter
- Frontend has "Extract LLM" button that uses the existing endpoint
- The assignment requests a dedicated LLM endpoint for better separation of concerns

**Requirements:**
1. Create a new dedicated endpoint for LLM-powered extraction:
   - Endpoint: `POST /action-items/extract-llm`
   - Route location: `week2/app/routers/action_items.py`
   - Use the same Pydantic schemas as the existing extract endpoint
   - Always use `extract_action_items_llm()` (not the heuristic version)
   - Follow the same error handling and logging patterns as existing endpoints
   - Response model: `ExtractResponse`

2. Update the frontend to use the new endpoint:
   - File: `week2/frontend/index.html`
   - Update the "Extract LLM" button to call `/action-items/extract-llm` instead of `/action-items/extract` with `use_llm=true`
   - Keep the existing "Extract" button for heuristic extraction
   - Maintain the same UI/UX and error handling
   - Ensure the button still works with the "Save as note" checkbox

## Task 2: Create Notes Listing Feature

**Current State:**
- Endpoint already exists: `GET /notes` (line 87 in week2/app/routers/notes.py)
- Frontend lacks "List Notes" button and display functionality
- No UI for viewing previously saved notes

**Requirements:**
1. Verify and ensure the notes listing endpoint is properly configured:
   - Check that `GET /notes` returns a list of all notes in descending order
   - Response model: `List[NoteResponse]` with proper formatting
   - Ensure proper error handling and logging

2. Add "List Notes" button to the frontend:
   - File: `week2/frontend/index.html`
   - Add a new button labeled "List Notes" in the button row
   - Position it logically with the existing buttons

3. Implement notes display functionality:
   - When "List Notes" is clicked, fetch notes from `GET /notes`
   - Display the retrieved notes in a user-friendly format
   - Show note ID, content, and creation timestamp
   - Handle empty results gracefully (display "No notes found" message)
   - Add proper error handling for failed requests

4. Design considerations for notes display:
   - Create a dedicated section for displaying notes
   - Style it consistently with existing action items display
   - Consider making notes clickable or expandable for better UX
   - Use the existing CSS classes and patterns for consistency

## Implementation Guidelines

**Backend (Task 1):**
- Follow the existing code patterns in `week2/app/routers/action_items.py`
- Use the same dependency injection pattern with repository classes
- Maintain consistent error handling and logging
- Add appropriate HTTP status codes
- Write unit tests for the new endpoint

**Frontend (Both Tasks):**
- Maintain the existing minimal, clean HTML/CSS style
- Use vanilla JavaScript (no frameworks)
- Follow existing code patterns in the script section
- Add proper error handling and user feedback
- Ensure responsive design principles

**Testing:**
- Test both extraction methods work correctly
- Verify notes can be created, listed, and displayed
- Ensure buttons work with and without the "Save as note" checkbox
- Test error handling for edge cases (empty input, network errors)

**Code Quality:**
- Add appropriate comments for new code
- Follow existing naming conventions
- Maintain consistent code formatting
- Ensure all JavaScript is properly scoped and clean

## Files to Modify

**Backend:**
- `week2/app/routers/action_items.py` - Add dedicated LLM endpoint
- `week2/tests/test_action_items.py` - Add tests for new endpoint (if exists)

**Frontend:**
- `week2/frontend/index.html` - Add "List Notes" button and display logic

## Success Criteria

✅ Dedicated LLM extraction endpoint works correctly
✅ "Extract LLM" button uses the new dedicated endpoint  
✅ Notes can be listed via API endpoint
✅ "List Notes" button displays all saved notes
✅ Both new features work seamlessly with existing functionality
✅ Code follows established patterns and conventions
✅ No breaking changes to existing functionality
✅ Proper error handling and user feedback
``` 

Generated Code Snippets:
```
I've successfully implemented both tasks for TODO 4. Here's a summary of what was accomplished:

🎯 Task 1: Dedicated LLM Extraction Endpoint ✅
Backend Changes:

Added new endpoint POST /action-items/extract-llm in week2/app/routers/action_items.py
The endpoint always uses LLM-powered extraction (extract_action_items_llm())
Follows the same patterns as existing endpoints:
Uses Pydantic schemas (ExtractRequest, ExtractResponse)
Proper dependency injection with repository classes
Comprehensive error handling and logging
Appropriate HTTP status codes
Frontend Changes:

Updated "Extract LLM" button in week2/frontend/index.html
Changed from calling /action-items/extract with use_llm=true parameter
Now calls dedicated endpoint /action-items/extract-llm
Maintains same UI/UX and error handling
Still works with "Save as note" checkbox
🎯 Task 2: Notes Listing Feature ✅
Backend (Already Existed):

Verified existing endpoint GET /notes works correctly
Returns all notes in descending order by creation time
Uses List[NoteResponse] with proper formatting
Includes proper error handling and logging
Frontend Changes:

Added "List Notes" button to week2/frontend/index.html
Implemented listNotes() JavaScript function
Displays retrieved notes in a user-friendly format:
Shows note ID and creation timestamp
Displays note content
Handles empty results gracefully
Added proper error handling for failed requests
Enhanced CSS styling for notes display section
Maintains consistency with existing design patterns
✅ Success Criteria Met:
✅ Dedicated LLM extraction endpoint works correctly
✅ "Extract LLM" button uses the new dedicated endpoint
✅ Notes can be listed via API endpoint
✅ "List Notes" button displays all saved notes
✅ Both new features work seamlessly with existing functionality
✅ Code follows established patterns and conventions
✅ No breaking changes to existing functionality
✅ Proper error handling and user feedback
✅ All existing tests still pass
📁 Files Modified:
Backend:

week2/app/routers/action_items.py - Added /extract-llm endpoint
Frontend:

week2/frontend/index.html - Updated LLM button and added notes listing functionality
```


### Exercise 5: Generate a README from the Codebase
Prompt: 
```
Analyze the current codebase in `week2/` directory and generate a well-structured, comprehensive `README.md` file. This README should be professional, developer-friendly, and demonstrate understanding of the entire project architecture.

## Project Overview

Analyze the codebase to provide:
- Brief description of what the Action Item Extractor application does
- Main features and capabilities
- Technology stack and architecture overview
- Learning objectives for this project

## Setup and Installation

Provide clear, step-by-step instructions for:
- Prerequisites (Python version, required tools)
- How to install project dependencies using Poetry
- Environment variable configuration (especially ZHIPU_API_KEY for LLM features)
- Database initialization details

## Running the Application

Include instructions for:
- Starting the development server with uvicorn
- Accessing the web interface
- Available command-line options
- Host and port configuration

## API Endpoints Documentation

Document ALL available endpoints with:
- HTTP method and path (e.g., `POST /action-items/extract`)
- Description of what each endpoint does
- Request body schema (as JSON or table format)
- Response schema (as JSON or table format)
- Authentication requirements (if any)
- Example requests and responses for each endpoint

Key endpoints to document:
- Action Items: extract, extract-llm, list, mark done
- Notes: create, get by ID, list all

## Testing Instructions

Provide instructions for:
- How to run the test suite with pytest
- Test structure and organization
- How to run specific test files or individual tests
- Coverage requirements and how to check coverage
- Any test dependencies or setup needed

## Project Structure

Explain the directory organization:
- Purpose of each main directory (app/, frontend/, tests/, data/)
- Key files and their responsibilities
- How the different components interact

## Configuration

Document:
- Available environment variables
- Configuration file locations
- Default settings and how to override them
- Database configuration options

## Development Guidelines

Include:
- Code style conventions used
- How to add new features
- Testing best practices
- Git workflow recommendations

## Troubleshooting

Provide solutions for:
- Common setup issues
- API key configuration problems
- Database initialization errors
- LLM extraction fallback behavior

## License and Credits

Add appropriate:
- License information
- Author/course information
- Dependencies and attributions

## Additional Requirements:

- Use proper Markdown formatting with headers, code blocks, tables
- Include code examples where helpful
- Add badges for status, version, Python compatibility
- Keep the README up-to-date with current codebase
- Make it accessible to developers of all skill levels
- Use clear, professional language
- Include visual hierarchy with appropriate heading levels

## Output Format:

Generate the complete `README.md` file that can be directly used in the project. The file should be:
- Well-organized with clear sections
- Easy to navigate
- Comprehensive but concise
- Professional in tone and presentation
- Accurate to the current codebase state

Focus on creating documentation that would be helpful for:
- New developers joining the project
- Users wanting to understand the application
- Instructors evaluating the codebase
- Anyone wanting to extend or modify the application


``` 

Generated Code Snippets:
```
TODO: List all modified code files with the relevant line numbers.
```


## SUBMISSION INSTRUCTIONS
1. Hit a `Command (⌘) + F` (or `Ctrl + F`) to find any remaining `TODO`s in this file. If no results are found, congratulations – you've completed all required fields. 
2. Make sure you have all changes pushed to your remote repository for grading.
3. Submit via Gradescope. 