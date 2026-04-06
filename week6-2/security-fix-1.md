# Security Fix #1: SQL Injection

**Issue ID**: #1
**Location**: `backend/app/routers/notes.py:71-79`
**Severity**: ERROR
**OWASP**: A05:2025 - Injection
**CWE**: CWE-89: SQL Injection

## Vulnerability Description

The `unsafe_search` endpoint was using raw SQL queries with `sqlalchemy.text()` and directly interpolating user input into the query string. This bypasses SQLAlchemy's ORM protections and creates a classic SQL injection vulnerability.

## Attack Vector

A malicious user could inject SQL commands through the `q` parameter:
```
GET /notes/unsafe-search?q=' OR '1'='1
```

This would return all records regardless of the search criteria. More severe attacks could include:
- Data exfiltration: `q=' UNION SELECT * FROM users--`
- Data deletion: `q='; DROP TABLE notes;--`
- Authentication bypass: `q=' OR '1'='1' --`

## Before (Vulnerable Code)

```python
@router.get("/unsafe-search", response_model=list[NoteRead])
def unsafe_search(q: str, db: Session = Depends(get_db)) -> list[NoteRead]:
    sql = text(
        f"""
        SELECT id, title, content, created_at, updated_at
        FROM notes
        WHERE title LIKE '%{q}%' OR content LIKE '%{q}%'
        ORDER BY created_at DESC
        LIMIT 50
        """
    )
    rows = db.execute(sql).all()
    # ...
```

**Issues**:
- User input (`q`) is directly interpolated into SQL string
- Using `text()` bypasses SQLAlchemy's ORM protections
- No input sanitization or parameterization

## After (Secure Code)

```python
@router.get("/unsafe-search", response_model=list[NoteRead])
def unsafe_search(q: str, db: Session = Depends(get_db)) -> list[NoteRead]:
    # FIXED: Using SQLAlchemy ORM methods instead of raw SQL to prevent SQL injection
    stmt = (
        select(Note)
        .where((Note.title.contains(q)) | (Note.content.contains(q)))
        .order_by(desc(Note.created_at))
        .limit(50)
    )
    rows = db.execute(stmt).scalars().all()
    # ...
```

**Improvements**:
- Using SQLAlchemy ORM's `select()` method
- User input is properly parameterized via `contains()` method
- SQLAlchemy automatically handles escaping and sanitization
- Same functionality with improved security

## Why This Fix Works

1. **Parameterization**: SQLAlchemy ORM methods automatically parameterize inputs, preventing injection.
2. **Type Safety**: ORM methods enforce type safety at compile time.
3. **Automatic Escaping**: Framework handles proper escaping of special characters.
4. **Consistency**: Uses the same pattern as the safe `list_notes` endpoint.

## Testing Recommendations

1. Verify search functionality still works correctly:
   ```bash
   curl "http://localhost:8000/notes/unsafe-search?q=test"
   ```

2. Test injection attempts (should return safe results):
   ```bash
   curl "http://localhost:8000/notes/unsafe-search?q=' OR '1'='1"
   ```

3. Verify Semgrep scan no longer flags this issue:
   ```bash
   semgrep scan --json --output semgrep-results.json
   ```

## Related Resources

- [OWASP SQL Injection](https://owasp.org/www-community/attacks/SQL_Injection)
- [SQLAlchemy ORM Tutorial](https://docs.sqlalchemy.org/en/14/orm/tutorial.html)
- [CWE-89: SQL Injection](https://cwe.mitre.org/data/definitions/89.html)

---

**Fixed**: 2026-04-06
