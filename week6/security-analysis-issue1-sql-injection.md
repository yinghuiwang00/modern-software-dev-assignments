# Security Analysis: SQL Injection Vulnerability in unsafe_search Endpoint

**Date:** 2026-04-06
**File:** week6/backend/app/routers/notes.py
**Lines:** 69-92
**Rule ID:** python.sqlalchemy.security.audit.avoid-sqlalchemy-text.avoid-sqlalchemy-text
**Severity:** HIGH

## Vulnerability Understanding

**Vulnerability Type:** SQL Injection (A01:2021-Injection, OWASP Top 10 2025)

**Attack Vector:**
The vulnerability exists in `/unsafe-search` endpoint where user input is directly concatenated into a SQL query using an f-string:
```python
sql = text(f"""SELECT id, title, content, created_at, updated_at
FROM notes
WHERE title LIKE '%{q}%' OR content LIKE '%{q}%'
ORDER BY created_at DESC
LIMIT 50""")
```

The parameter `q` (search query) is inserted directly into SQL string without any sanitization or parameterization, allowing attackers to inject malicious SQL.

**Potential Impact:**
1. **Data Exfiltration:** Attackers can extract all data from database using UNION-based injection
2. **Data Modification:** INSERT, UPDATE, DELETE operations can be injected to corrupt or delete data
3. **Database Schema Disclosure:** Attackers can query system tables (sqlite_master) to discover table structures
4. **Authentication Bypass:** If authentication is added later, injection could bypass it
5. **Denial of Service:** Malicious queries could lock or crash database
6. **Privilege Escalation:** Depending on database permissions, could execute administrative commands

**Exploitable in Current Context:**
Yes, absolutely exploitable. The vulnerability is in a publicly accessible GET endpoint with no authentication. An attacker can:

```python
# Extract all notes regardless of content
/unsafe-search?q=' OR '1'='1

# List all tables in database (SQLite)
/unsafe-search?q=' UNION SELECT name, type, sql, name, name FROM sqlite_master --

# Create a malicious note (if database permissions allow)
/unsafe-search?q='; INSERT INTO notes (title, content) VALUES ('HACKED', 'Pwned') --

# Drop entire notes table
/unsafe-search?q='; DROP TABLE notes; --
```

## Root Cause Analysis

**Why Vulnerability Exists:**
1. **Improper Use of SQLAlchemy's `text()` function:** The `text()` function is designed to be used with bind parameters (`:placeholder`), but developer used string interpolation (f-string) instead
2. **Direct User Input Concatenation:** User input `q` is directly embedded in SQL string without sanitization
3. **Lack of Input Validation:** No validation or sanitization is performed on `q` parameter before use
4. **Missing Security Code Review:** This pattern contradicts SQLAlchemy's documented security practices

**Code Pattern Issues:**
The vulnerable code follows this dangerous pattern:
```python
# DANGEROUS: String interpolation with user input
sql = text(f"SELECT * FROM table WHERE field LIKE '%{user_input}%'")

# The developer bypassed SQLAlchemy's ORM protection by using raw SQL
# instead of safe ORM pattern used elsewhere in codebase
```

**Similar Issues in Codebase:**
The vulnerability is isolated to `unsafe_search` endpoint. However, there are concerning patterns:

1. **Contrast with Safe Code (lines 14-34):** The same file contains a properly implemented search endpoint (`/`) that uses SQLAlchemy ORM safely:
   ```python
   stmt = select(Note)
   if q:
       stmt = stmt.where((Note.title.contains(q)) | (Note.content.contains(q)))
   ```
   This demonstrates developer knows safe pattern but chose not to use it.

2. **Database Seeding (db.py:56):** The seed SQL is also loaded using `text()` with raw SQL, but this is less critical as it's static SQL, not user input.

3. **Other Security Issues:** The file contains multiple other critical vulnerabilities in debug endpoints (eval, subprocess.run, file operations) but these are separate issues.

**Design Decision Issues:**
- The endpoint is explicitly named "unsafe_search", suggesting this might be intentional for educational purposes
- However, no documentation or warnings explain the security implications
- The pattern teaches developers that raw SQL with string interpolation is acceptable

## Mitigation Strategy

**Recommended Fix Approach:**

**Option 1: Use SQLAlchemy ORM (Preferred)**
Replace raw SQL with same safe pattern used in the `/` endpoint:

```python
@router.get("/unsafe-search", response_model=list[NoteRead])
def unsafe_search(q: str, db: Session = Depends(get_db)) -> list[NoteRead]:
    stmt = select(Note).where(
        (Note.title.contains(q)) | (Note.content.contains(q))
    ).order_by(desc(Note.created_at)).limit(50)

    rows = db.execute(stmt).scalars().all()
    return [NoteRead.model_validate(row) for row in rows]
```

**Option 2: Use Parameterized Queries with `text()`**
If raw SQL is necessary (unlikely in this case), use bind parameters:

```python
@router.get("/unsafe-search", response_model=list[NoteRead])
def unsafe_search(q: str, db: Session = Depends(get_db)) -> list[NoteRead]:
    search_pattern = f"%{q}%"  # Only wildcards are added, not SQL
    sql = text("""
        SELECT id, title, content, created_at, updated_at
        FROM notes
        WHERE title LIKE :pattern OR content LIKE :pattern
        ORDER BY created_at DESC
        LIMIT 50
    """)
    rows = db.execute(sql, {"pattern": search_pattern}).all()
    return [NoteRead.model_validate(row) for row in rows]
```

**OWASP Guidelines Applied:**

1. **Primary Defense - Prepared Statements (Parameterized Queries):** Use SQLAlchemy's ORM or bind parameters to separate SQL structure from data
2. **Input Validation:** Validate that `q` is a reasonable length and contains only safe characters (though parameterization makes this less critical)
3. **Least Privilege:** Ensure database connection has minimum required permissions
4. **Defense in Depth:** Combine parameterized queries with input validation and rate limiting

**Security Best Practices:**

1. **Never concatenate user input into SQL strings:** Always use parameterized queries
2. **Use ORM frameworks properly:** SQLAlchemy provides automatic SQL injection protection when used correctly
3. **Avoid raw SQL unless absolutely necessary:** The ORM handles 99% of use cases safely
4. **Security code reviews:** Any use of `text()` with user input should trigger manual review
5. **Static analysis tools:** Enable Semgrep's SQL injection rules in CI/CD pipeline
6. **Developer education:** Train developers on safe database access patterns

## Testing Requirements

**Tests Needed to Verify Fix:**

**1. Functional Tests (Verify Fix Works):**
```python
def test_unsafe_search_normal_query(client):
    """Verify normal search still works after fix"""
    # Create test notes
    client.post("/notes/", json={"title": "Python Tutorial", "content": "Learn Python"})
    client.post("/notes/", json={"title": "JavaScript Guide", "content": "Learn JS"})

    # Test search
    r = client.get("/notes/unsafe-search", params={"q": "Python"})
    assert r.status_code == 200
    results = r.json()
    assert len(results) == 1
    assert "Python" in results[0]["title"]
```

**2. Security Tests (Verify Fix Prevents Injection):**
```python
def test_unsafe_search_sql_injection_or_true(client):
    """Verify SQL injection with ' OR '1'='1 is prevented"""
    r = client.get("/notes/unsafe-search", params={"q": "' OR '1'='1"})
    assert r.status_code == 200
    # Should return empty results or only literal matches, not all data

def test_unsafe_search_sql_injection_union(client):
    """Verify UNION-based injection is prevented"""
    r = client.get("/notes/unsafe-search", params={"q": "' UNION SELECT name, type, sql, name, name FROM sqlite_master --"})
    assert r.status_code == 200
    results = r.json()
    # Should not contain database schema information

def test_unsafe_search_sql_injection_drop(client):
    """Verify DROP TABLE injection is prevented"""
    r = client.get("/notes/unsafe-search", params={"q": "'; DROP TABLE notes; --"})
    assert r.status_code == 200
    # Verify notes still exist
    r2 = client.get("/notes/")
    assert r2.status_code == 200  # If table was dropped, this would fail
```

**3. Edge Cases:**
```python
def test_unsafe_search_special_characters(client):
    """Verify special characters are handled safely"""
    special_chars = ["'", '"', ";", "--", "/*", "*/", "\\", "\""]
    for char in special_chars:
        r = client.get("/notes/unsafe-search", params={"q": char})
        assert r.status_code == 200
        assert isinstance(r.json(), list)

def test_unsafe_search_empty_query(client):
    """Verify empty query is handled"""
    r = client.get("/notes/unsafe-search", params={"q": ""})
    assert r.status_code == 200

def test_unsafe_search_long_query(client):
    """Verify query length limits are enforced"""
    long_query = "a" * 10000
    r = client.get("/notes/unsafe-search", params={"q": long_query})
    # Should either return 400 (validation) or handle gracefully
    assert r.status_code in [200, 400]
```

**Additional Security Measures:**

1. **Input Validation (Defense in Depth):**
```python
from fastapi import Query, HTTPException

@router.get("/unsafe-search", response_model=list[NoteRead])
def unsafe_search(
    q: str = Query(..., min_length=1, max_length=100, pattern="^[a-zA-Z0-9\\s\\-_,.!?]+$"),
    db: Session = Depends(get_db)
) -> list[NoteRead]:
    # Implementation
```

2. **Rate Limiting:** Prevent brute force attacks
3. **Query Logging:** Log suspicious query patterns for monitoring
4. **Error Messages:** Ensure errors don't leak database information

## Summary

This is a **HIGH** severity SQL injection vulnerability that allows complete database compromise. The fix is straightforward: replace raw SQL with string interpolation with SQLAlchemy ORM or parameterized queries. The codebase already contains correct pattern in other endpoints, making this an implementation error rather than a design issue.

**Immediate Actions Required:**
1. Fix vulnerability using Option 1 (ORM approach)
2. Add comprehensive tests for the fix
3. Review other uses of `text()` in codebase
4. Consider removing "unsafe-search" endpoint entirely if not needed
5. Add input validation as a defense-in-depth measure
6. Enable Semgrep SQL injection rules in CI/CD

## Sources

- [SQL Injection Prevention - OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)
- [Dynamic Column Parameterization in SQLAlchemy Core](https://www.geeksforgeeks.org/python/dynamic-column-parameterization-in-sqlalchemy-core/)
