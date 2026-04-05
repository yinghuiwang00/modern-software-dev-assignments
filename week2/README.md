# Action Item Extractor

A modern FastAPI application that converts free-form meeting notes into actionable items using both heuristic pattern matching and LLM-powered extraction.

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111%2B-green)
![License](https://img.shields.io/badge/license-Educational%20Use-yellow)

## 📋 Overview

The Action Item Extractor is a web application designed to help teams and individuals extract actionable items from meeting notes and other unstructured text. It features:

- **Dual Extraction Methods**: Choose between heuristic pattern matching and LLM-powered extraction
- **Notes Management**: Save, retrieve, and manage meeting notes
- **Action Item Tracking**: Create, list, and mark action items as completed
- **Modern Architecture**: Built with FastAPI, using clean architecture patterns and type-safe code
- **Developer-Friendly**: Comprehensive error handling, logging, and testing

### Learning Objectives

This project demonstrates modern software development practices including:
- RESTful API design with FastAPI
- Database abstraction using the repository pattern
- Type-safe API contracts with Pydantic
- LLM integration for natural language processing
- Comprehensive testing with pytest
- Clean code organization and error handling

## 🚀 Features

### Core Functionality
- **Heuristic Extraction**: Extracts action items using pattern matching (bullet points, keywords, checkboxes)
- **LLM-Powered Extraction**: Leverages Zhipu AI (GLM-4) for intelligent extraction
- **Notes Database**: Persist and retrieve meeting notes with timestamps
- **Action Item Management**: Track action items with completion status
- **Real-time Updates**: Interactive frontend with immediate feedback

### Technical Features
- **Type-Safe API**: Pydantic schemas for request/response validation
- **Repository Pattern**: Clean database abstraction layer
- **Custom Logging**: Configurable logging throughout the application
- **Error Handling**: Comprehensive exception handling with meaningful error messages
- **Lifespan Management**: Proper FastAPI startup/shutdown events
- **Configuration Management**: Environment-based configuration with defaults

## 🛠️ Technology Stack

- **Backend Framework**: FastAPI (>= 0.111.0)
- **Database**: SQLite with repository pattern
- **Data Validation**: Pydantic (>= 2.0.0)
- **LLM Integration**: Zhipu AI (GLM-4 model) via OpenAI SDK
- **Testing**: pytest with comprehensive test coverage
- **Code Quality**: Black (formatting) and Ruff (linting)
- **Server**: Uvicorn (>= 0.23.0)

## 📦 Installation

### Prerequisites
- Python 3.10 or higher
- Poetry for dependency management
- Optional: Zhipu AI API key for LLM extraction

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd modern-software-dev-assignments
   ```

2. **Install dependencies**
   ```bash
   # Using Poetry (recommended)
   poetry install

   # Or using pip (if poetry is not available)
   pip install fastapi uvicorn sqlalchemy pydantic python-dotenv openai pytest
   ```

3. **Configure environment variables**
   Create a `.env` file in the project root:
   ```bash
   # Required for LLM extraction (optional - will fall back to heuristic extraction)
   ZHIPU_API_KEY=your_zhipu_api_key_here

   # Optional configuration
   LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR, CRITICAL
   ```

4. **Initialize the database**
   The database is automatically initialized when the application starts, or you can run:
   ```bash
   python -m week2.app.main
   ```

## 🏃 Running the Application

### Development Server

```bash
# Basic development server
poetry run uvicorn week2.app.main:app --reload

# With custom host and port
poetry run uvicorn week2.app.main:app --reload --host 0.0.0.0 --port 8000

# Or using Python directly
python -m uvicorn week2.app.main:app --reload --host 0.0.0.0 --port 8000
```

### Access the Application

Open your browser and navigate to:
- `http://localhost:8000/` - Web interface
- `http://localhost:8000/docs` - Interactive API documentation (Swagger UI)
- `http://localhost:8000/redoc` - Alternative API documentation (ReDoc)

## 📚️ API Endpoints

### Action Items

#### Extract Action Items (Heuristic or LLM)
```http
POST /action-items/extract
```

**Request Body:**
```json
{
  "text": "Meeting notes here...",
  "save_note": true,
  "use_llm": false
}
```

**Response:**
```json
{
  "note_id": 1,
  "items": [
    {
      "id": 1,
      "text": "Set up database"
    }
  ]
}
```

#### Extract Action Items (LLM Only)
```http
POST /action-items/extract-llm
```

**Request Body:**
```json
{
  "text": "Meeting notes here...",
  "save_note": true
}
```

**Response:** Same as `/action-items/extract`

#### List Action Items
```http
GET /action-items?note_id=<optional_id>
```

**Parameters:**
- `note_id` (optional): Filter action items by note ID

**Response:**
```json
[
  {
    "id": 1,
    "note_id": 1,
    "text": "Set up database",
    "done": false,
    "created_at": "2026-04-04T19:00:00.000000"
  }
]
```

#### Mark Action Item as Done
```http
POST /action-items/{action_item_id}/done
```

**Request Body:**
```json
{
  "done": true
}
```

**Response:**
```json
{
  "id": 1,
  "done": true
}
```

### Notes

#### Create Note
```http
POST /notes
```

**Request Body:**
```json
{
  "content": "Meeting notes here..."
}
```

**Response:**
```json
{
  "id": 1,
  "content": "Meeting notes here...",
  "created_at": "2026-04-04T19:00:00.000000"
}
```

#### Get Note by ID
```http
GET /notes/{note_id}
```

**Response:** Same as Create Note response

#### List All Notes
```http
GET /notes
```

**Response:**
```json
[
  {
    "id": 1,
    "content": "Meeting notes here...",
    "created_at": "2026-04-04T19:00:00.000000"
  }
]
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
poetry run pytest

# Run with verbose output
poetry run pytest -v

# Run specific test file
poetry run pytest week2/tests/test_extract.py

# Run with coverage
poetry run pytest --cov=week2 --cov-report=term-missing
```

### Test Structure

```
week2/tests/
├── conftest.py           # Pytest configuration and fixtures
├── test_extract.py         # Unit tests for extraction functions
└── __init__.py
```

### Coverage Requirements

The project maintains 80%+ test coverage for critical business logic:
- Extraction functions (heuristic and LLM)
- Repository operations
- API endpoints
- Error handling

## 📁 Project Structure

```
week2/
├── app/                          # Main application code
│   ├── main.py                   # FastAPI application setup
│   ├── config.py                 # Configuration management
│   ├── database.py               # Database initialization
│   ├── schemas.py                # Pydantic models
│   ├── exceptions.py              # Custom exceptions
│   ├── services/                 # Business logic
│   │   └── extract.py           # Action item extraction
│   ├── repositories/              # Data access layer
│   │   ├── note_repository.py
│   │   └── action_item_repository.py
│   └── routers/                 # API endpoints
│       ├── notes.py
│       └── action_items.py
├── tests/                        # Test suite
│   ├── conftest.py
│   └── test_extract.py
├── frontend/                     # Web interface
│   └── index.html
├── data/                        # SQLite database storage
├── assignment.md                # Assignment requirements
├── writeup.md                   # Development writeup
└── README.md                    # This file
```

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|----------|-----------|
| `ZHIPU_API_KEY` | Zhipu AI API key for LLM extraction | None | Optional |
| `LOG_LEVEL` | Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL) | INFO | Optional |

### Database Configuration

- **Location**: `data/app.db` (automatically created)
- **Type**: SQLite
- **Initialization**: Automatic on application startup
- **Schema**: Notes and Action Items tables with foreign key relationship

## 🧩 Development Guidelines

### Code Style

- **Formatting**: Black (line length: 100)
- **Linting**: Ruff
- **Type Hints**: Required for all public functions
- **Documentation**: Docstrings for all public functions and classes

### Adding New Features

1. **Backend**:
   - Add Pydantic schemas to `schemas.py`
   - Implement repository methods if database access needed
   - Add API endpoint in appropriate router file
   - Write comprehensive tests

2. **Frontend**:
   - Follow existing HTML/CSS patterns
   - Use vanilla JavaScript (no frameworks)
   - Implement proper error handling
   - Maintain responsive design

### Testing Best Practices

- Write tests before implementation (TDD approach)
- Mock external dependencies (API keys, database)
- Test both success and error cases
- Maintain 80%+ code coverage
- Use descriptive test names

## 🔧 Troubleshooting

### Common Issues

**LLM Extraction Not Working**
- Ensure `ZHIPU_API_KEY` is set in `.env` file
- Check API key validity
- The application will fall back to heuristic extraction if LLM is unavailable

**Database Errors**
- Ensure the `data/` directory has write permissions
- Delete `data/app.db` and restart if schema issues occur
- Check SQLite version compatibility (should be built into Python)

**Import Errors**
- Run `poetry install` to ensure all dependencies are installed
- Check Python version is 3.10+
- Verify you're in the correct directory

**Testing Issues**
- Set `ZHIPU_API_KEY=test_api_key_for_unit_tests_only` in `.env`
- Run tests from project root directory
- Check pytest version: `poetry run pytest --version`

## 📊 Architecture Overview

The application follows a clean, layered architecture:

1. **Presentation Layer** (`routers/`): FastAPI endpoints handling HTTP requests/responses
2. **Business Logic Layer** (`services/`): Core application logic (extraction algorithms)
3. **Data Access Layer** (`repositories/`): Database operations with connection management
4. **Model Layer** (`schemas/`): Pydantic models for type safety and validation
5. **Configuration Layer** (`config.py`): Environment-based settings management

### Key Design Patterns

- **Repository Pattern**: Database abstraction with clear separation of concerns
- **Dependency Injection**: FastAPI's `Depends()` for clean dependency management
- **Factory Pattern**: Repository instantiation for testability
- **Context Manager**: Database connection management for proper resource cleanup

## 📝 Contributing

This is an educational project. Contributions should:
- Follow existing code style and patterns
- Include tests for new functionality
- Update documentation for API changes
- Maintain backward compatibility

## 📄 License

This project is developed for educational purposes as part of the Modern Software Development course.

## 🤝 Credits

**Course**: Modern Software Development
**Assignment**: Week 2 - Action Item Extractor
**Technology**: FastAPI, Python, LLM Integration

---

**Note**: This project uses the Zhipu AI API for LLM-powered extraction. Ensure you have a valid API key or the application will fall back to heuristic extraction methods.
