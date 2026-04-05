# API Documentation

Generated from OpenAPI spec at http://localhost:8000/openapi.json

## Notes Endpoints

### GET /notes/
List all notes.

**Response:** Array of Note objects

**Example Response:**
```json
[
  {
    "id": 1,
    "title": "Welcome",
    "content": "This is a starter note. TODO: explore the app!"
  },
  {
    "id": 2,
    "title": "Demo",
    "content": "Click around and add a note. Ship feature!"
  }
]
```

### POST /notes/
Create a new note.

**Request Body:**
```json
{
  "title": "My Note",
  "content": "Note content"
}
```

**Validation:**
- `title`: Required, 1-200 characters, non-empty after trimming whitespace
- `content`: Required, 1-5000 characters, non-empty after trimming whitespace

**Response:** 201 Created with Note object

**Example Response:**
```json
{
  "id": 3,
  "title": "My Note",
  "content": "Note content"
}
```

**Error Responses:**
- 422: Validation error (e.g., empty title, missing fields, length exceeded)

### GET /notes/search/
Search notes by query string.

**Query Parameters:**
- `q` (optional): Search query string - searches both title and content

**Response:** Array of matching Note objects

**Example:** `GET /notes/search/?q=welcome`

**Example Response:**
```json
[
  {
    "id": 1,
    "title": "Welcome",
    "content": "This is a starter note. TODO: explore the app!"
  }
]
```

### GET /notes/{note_id}
Get a specific note by ID.

**Path Parameters:**
- `note_id` (integer): Note ID

**Response:** Note object

**Example Response:**
```json
{
  "id": 1,
  "title": "Welcome",
  "content": "This is a starter note. TODO: explore the app!"
}
```

**Error Responses:**
- 404: Note not found

### PUT /notes/{note_id}
Update an existing note.

**Path Parameters:**
- `note_id` (integer): Note ID

**Request Body:** All fields are optional - only provided fields will be updated
```json
{
  "title": "Updated Title",
  "content": "Updated content"
}
```

**Validation:**
- `title`: If provided, 1-200 characters, non-empty after trimming whitespace
- `content`: If provided, 1-5000 characters, non-empty after trimming whitespace

**Response:** 200 OK with updated Note object

**Example Response:**
```json
{
  "id": 1,
  "title": "Updated Title",
  "content": "Updated content"
}
```

**Error Responses:**
- 404: Note not found
- 422: Validation error

### DELETE /notes/{note_id}
Delete a note.

**Path Parameters:**
- `note_id` (integer): Note ID

**Response:** 204 No Content

**Error Responses:**
- 404: Note not found

## Action Items Endpoints

### GET /action-items/
List all action items.

**Response:** Array of ActionItem objects

**Example Response:**
```json
[
  {
    "id": 1,
    "description": "Try pre-commit",
    "completed": false
  },
  {
    "id": 2,
    "description": "Run tests",
    "completed": false
  }
]
```

### POST /action-items/
Create a new action item.

**Request Body:**
```json
{
  "description": "Do something"
}
```

**Validation:**
- `description`: Required, 1-500 characters, non-empty after trimming whitespace

**Response:** 201 Created with ActionItem object

**Example Response:**
```json
{
  "id": 3,
  "description": "Do something",
  "completed": false
}
```

**Error Responses:**
- 422: Validation error (e.g., empty description, missing field, length exceeded)

### PUT /action-items/{item_id}/complete
Mark an action item as complete.

**Path Parameters:**
- `item_id` (integer): Action item ID

**Response:** 200 OK with updated ActionItem object

**Example Response:**
```json
{
  "id": 1,
  "description": "Try pre-commit",
  "completed": true
}
```

**Error Responses:**
- 404: Action item not found

## Common Error Responses

### 422 Validation Error
When request data fails validation:
```json
{
  "detail": [
    {
      "loc": ["body", "title"],
      "msg": "value is not a valid string",
      "type": "string_type"
    }
  ]
}
```

### 404 Not Found
When a resource doesn't exist:
```json
{
  "detail": "Note not found"
}
```
