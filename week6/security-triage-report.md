# Security Triage Report

**Date:** 2026-04-06
**Assessment Tool:** Semgrep
**File:** semgrep-results.json

## Security Findings Summary

Total findings: 6

### By Type
- SAST: 6
- Secrets: 0
- SCA: 0

### By Severity
- CRITICAL: 0
- HIGH: 3
- MEDIUM: 3
- LOW: 0

## Top 3 Issues to Fix

### Issue #1: SQL Injection in unsafe_search endpoint
**Severity:** HIGH
**Type:** SAST
**File:** week6/backend/app/routers/notes.py
**Line:** 71-79
**Rule ID:** python.sqlalchemy.security.audit.avoid-sqlalchemy-text.avoid-sqlalchemy-text
**False Positive:** No
**Description:** The `unsafe_search` endpoint directly interpolates user input (`q`) into a raw SQL query string using `sqlalchemy.text()`. This creates a classic SQL injection vulnerability where an attacker could manipulate the query to access unauthorized data, modify data, or execute administrative operations on the database. The code constructs SQL with f-string interpolation: `WHERE title LIKE '%{q}%' OR content LIKE '%{q}%'`, bypassing SQLAlchemy's built-in SQL injection protections.
**Recommendation:** Remove the `unsafe_search` endpoint entirely as it appears to be a debug/test endpoint. If functionality is needed, rewrite it using SQLAlchemy's safe query builders: `stmt = select(Note).where((Note.title.contains(q)) | (Note.content.contains(q)))` (see the safe implementation in the `list_notes` function above).

### Issue #2: Command Injection in debug_run endpoint
**Severity:** HIGH
**Type:** SAST
**File:** week6/backend/app/routers/notes.py
**Line:** 112
**Rule ID:** python.lang.security.audit.subprocess-shell-true.subprocess-shell-true
**False Positive:** No
**Description:** The `debug_run` endpoint uses `subprocess.run(cmd, shell=True)` which spawns a shell process to execute arbitrary commands provided by the user. Since `shell=True` is used, shell metacharacters, command chaining, and command substitution are possible. This allows attackers to execute arbitrary system commands with the same privileges as the application server. An attacker could read sensitive files, steal credentials, modify system configurations, or pivot to attack other systems on the network.
**Recommendation:** Remove the `debug_run` endpoint entirely as it's a debug endpoint with no legitimate production use case. Debug endpoints should never be deployed to production. If command execution is absolutely necessary for a specific feature, validate the command against a strict whitelist of allowed commands and use `shell=False` with a list of arguments.

### Issue #3: Code Injection in debug_eval endpoint
**Severity:** HIGH
**Type:** SAST
**File:** week6/backend/app/routers/notes.py
**Line:** 104
**Rule ID:** python.lang.security.audit.eval-detected.eval-detected
**False Positive:** No
**Description:** The `debug_eval` endpoint uses `eval(expr)` to execute arbitrary Python code provided by the user via the `expr` parameter. This is a critical code injection vulnerability that allows attackers to execute any Python code within the application's context. An attacker could import malicious modules, access sensitive data, modify application state, read environment variables, establish reverse shells, or perform lateral movement. The `# noqa: S307` comment indicates this was intentionally left insecure, likely for educational or testing purposes.
**Recommendation:** Remove the `debug_eval` endpoint entirely. Never use `eval()` on user input in production code. If you need to parse and evaluate user-provided expressions, use a safe evaluation library like `ast.literal_eval()` (for literal values only) or a dedicated expression evaluator like `simpleeval` with restricted functionality.

## Other Findings

### Issue #4: Insecure document method in frontend
**Severity:** MEDIUM
**Type:** SAST
**File:** week6/frontend/app.js
**Line:** 14
**Rule ID:** javascript.browser.security.insecure-document-method.insecure-document-method
**False Positive:** No
**Description:** The frontend code uses `li.innerHTML` to inject user-controlled data (`n.title` and `n.content`) directly into the DOM without sanitization. While the data comes from the API and may already be sanitized on the server side, this pattern is risky. If an attacker can inject malicious content into the database (e.g., through a future vulnerability or insider threat), or if the API response is compromised, this could lead to stored XSS attacks affecting all users who view the malicious note.
**Recommendation:** Use `textContent` instead of `innerHTML` when setting text content: `li.textContent = n.title + ': ' + n.content;`. If HTML formatting is necessary, sanitize the input using a library like DOMPurify: `li.innerHTML = DOMPurify.sanitize('<strong>' + escapeHtml(n.title) + '</strong>: ' + escapeHtml(n.content));`.

### Issue #5: Wildcard CORS configuration
**Severity:** MEDIUM
**Type:** SAST
**File:** week6/backend/app/main.py
**Line:** 24
**Rule ID:** python.fastapi.security.wildcard-cors.wildcard-cors
**False Positive:** No
**Description:** The CORS middleware is configured with `allow_origins=["*"]`, which allows requests from any origin. This bypasses the same-origin policy and enables cross-origin requests from any website. While this is acceptable during development, in production it could enable CSRF attacks, data leakage to unauthorized origins, or be abused in phishing attacks. Additionally, the `allow_credentials=True` option combined with wildcard origins is contradictory and may cause issues in some browsers.
**Recommendation:** Replace `allow_origins=["*"]` with an explicit list of allowed origins in production: `allow_origins=["https://yourdomain.com"]`. For development, use environment variables to configure allowed origins: `ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")`. Remove `allow_credentials=True` if using wildcard origins, or combine it with specific origins only.

### Issue #6: Dynamic urllib use in debug_fetch endpoint
**Severity:** MEDIUM
**Type:** SAST
**File:** week6/backend/app/routers/notes.py
**Line:** 124
**Rule ID:** python.lang.security.audit.dynamic-urllib-use-detected.dynamic-urllib-use-detected
**False Positive:** No
**Description:** The `debug_fetch` endpoint uses `urlopen(url)` with user-controlled URL. While this doesn't directly enable attacks like SQL injection, it can be abused for Server-Side Request Forgery (SSRF). An attacker could use this endpoint to scan internal networks and port services, access metadata services (e.g., AWS IMDS, GCP metadata), access internal APIs that shouldn't be exposed, retrieve sensitive files using `file://` URIs (though this is often blocked), or abuse of server's IP for attacks on other systems.
**Recommendation:** Remove the `debug_fetch` endpoint as it's a debug endpoint with no legitimate production use. If URL fetching functionality is required, implement strict URL validation to only allow HTTPS URLs to specific whitelisted domains, and use a more modern library like `requests` with timeouts and proper error handling.

---

## Summary

The analysis reveals **6 security findings**, all of which are actual vulnerabilities (no false positives). The findings fall into two categories:

**Critical Production Issues (3):**
- Three debug endpoints (`unsafe_search`, `debug_run`, `debug_eval`) that provide direct access to injection vulnerabilities
- These should be **removed immediately** before any production deployment

**Development/Configuration Issues (3):**
- CORS wildcard configuration (acceptable in dev, dangerous in prod)
- XSS vulnerability in frontend
- SSRF vulnerability in another debug endpoint

**Immediate Action Required:**
Delete or disable all debug endpoints (`/unsafe-search`, `/debug/*`) before deploying to any environment beyond local development. These are clearly marked as debug/test code and have no legitimate production use case.
