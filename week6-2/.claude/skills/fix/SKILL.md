---
name: fix
description: Fix a specific security issue identified by Semgrep
---

# Fix Skill - Fix Security Issue

## Overview

Fixes a specific security vulnerability identified in the triage report using minimal, targeted code changes.

## Usage

```
/fix <issue_number>
```

**Arguments:**
- `issue_number`: The issue number from the triage report (1, 2, or 3)

## What It Does

1. Invokes the `security-fixer` agent
2. Reads the vulnerability details from triage report
3. Analyzes the vulnerable code
4. Applies minimal, targeted fix using best practices
5. Documents the fix in `security-fix-{N}.md`
6. Returns fix summary

## Vulnerability Types Handled

- **SQL Injection**: Use parameterized queries
- **Command Injection**: Avoid shell=True, use safe alternatives
- **Arbitrary Code Execution**: Remove eval() or use safe alternatives
- **Weak Cryptography**: Use strong algorithms (SHA256+, bcrypt)
- **Path Traversal**: Validate and sanitize file paths
- **CORS Misconfiguration**: Specify allowed origins
- **XSS**: Use textContent or sanitize HTML

## Expected Output

A summary including:
- Issue title and description
- File and line number
- Type of fix applied
- Path to fix documentation

## Example Output

```
Fixing issue #1: SQL Injection in notes.py:71...

Fix applied!
- File: backend/app/routers/notes.py:71
- Fix: Replaced f-string SQL with parameterized query
- Risk: Prevents attackers from executing arbitrary SQL queries
- Documentation: security-fix-1.md
```

## Code Change Example

```python
# Before (SQL Injection)
sql = text(f"""
    SELECT id, title, content, created_at, updated_at
    FROM notes
    WHERE title LIKE '%{q}%' OR content LIKE '%{q}%'
""")

# After (Parameterized Query)
sql = text("""
    SELECT id, title, content, created_at, updated_at
    FROM notes
    WHERE title LIKE :pattern OR content LIKE :pattern
""")
rows = db.execute(sql, {"pattern": f"%{q}%"})
```

## Prerequisites

- Security analysis must be complete
- Triage report must exist
- Issue number must be valid (1, 2, or 3)

## Error Handling

If issue number is invalid:
- Error message
- List available issues

If fix is complex or ambiguous:
- Explain options
- Ask user to choose approach
- Don't make assumptions

## Important Notes

- **Minimal changes**: Fix only the vulnerability
- **Maintain functionality**: Code should still work as intended
- **Follow patterns**: Match existing code style
- **Document clearly**: Explain why the fix works
- **Remove debug code**: If fixing debug functions, remove them entirely

## Best Practices

For each vulnerability type:

1. **SQL Injection** → Parameterized queries
2. **Command Injection** → subprocess without shell=True or use shlex.quote()
3. **eval()** → Remove or use ast.literal_eval()
4. **Weak crypto** → Use SHA256+, bcrypt for passwords
5. **Path traversal** → Validate with Path().resolve() and is_relative_to()
6. **CORS** → Specify allowed origins explicitly
7. **XSS** → Use textContent instead of innerHTML

## Next Steps

After fixing:
- Use `/fix <next_issue>` to fix more issues
- Use `/verify` to run tests after all fixes
- Use `/report` to generate final report
- Use `/workflow` to run complete process

## Related Commands

- `/analyze` - Generate triage report first
- `/verify` - Verify fixes with tests
- `/report` - Generate final documentation
- `/workflow` - Run complete end-to-end workflow
