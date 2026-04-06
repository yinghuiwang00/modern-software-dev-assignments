# API Documentation

Generated from OpenAPI spec at http://localhost:8000/openapi.json

## Root Endpoint

### GET /
Root endpoint for the application.

**Response:** 200 OK

---

## Notes Endpoints

### GET /notes/
List all notes.

**Response:**
```json
[
  {
    "id": 1,
    "title": "Welcome",
    "content": "This is a starter note."
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

**Response:** 201 Created with the created note object

### GET /notes/search/
Search notes by query string (case-insensitive).

**Query Parameters:**
- `q` (optional): Search query string - searches both title and content

**Response:** Array of matching notes

**Example:**
```
GET /notes/search/?q=hello
```

### GET /notes/{note_id}
Get a specific note by ID.

**Path Parameters:**
- `note_id` (required): The ID of the note

**Response:** Note object or 404 if not found

### POST /notes/{note_id}/extract
Extract action items and tags from a note.

**Path Parameters:**
- `note_id` (required): The ID of the note

**Response:**
```json
{
  "note_id": 1,
  "note_content": "Note content here",
  "extracted_items": [
    {
      "description": "Fix the bug",
      "tags": ["urgent", "critical"]
    }
  ]
}
```

**Description:**
Extracts action items from the note content. Action items are identified by:
- Lines ending with "!"
- Lines starting with "TODO:"
- Lines containing hashtags (#tag)
- Lines starting with #pattern:

Tags (hashtags) are extracted from each action item and returned separately.

---

## Action Items Endpoints

### GET /action-items/
List all action items.

**Response:**
```json
[
  {
    "id": 1,
    "description": "Do something",
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

**Response:** 201 Created with the created action item object

### PUT /action-items/{item_id}/complete
Mark an action item as complete.

**Path Parameters:**
- `item_id` (required): The ID of the action item

**Response:** Updated action item object with `completed: true`

---

## Data Models

### Note
```json
{
  "id": 1,
  "title": "string",
  "content": "string"
}
```

### ActionItem
```json
{
  "id": 1,
  "description": "string",
  "completed": false
}
```

---

## Notes

- All timestamps are in UTC
- IDs are auto-incrementing integers
- Search is case-insensitive and matches both title and content fields


### PUT /notes/{note_id}
Update a note.

**Path Parameters:**
- `note_id` (required): The ID of the note

**Response:**
```json
{
  "id": 1,
  "title": "Updated Title",
  "content": "Updated Content"
}
```

**Request Body:**
```json
{
  "title": string | null,
  "content": string | null
}
```

### DELETE /notes/{note_id}
Delete a note.

**Path Parameters:**
- `note_id` (required): The ID of the note

**Response:** 204 No Content
