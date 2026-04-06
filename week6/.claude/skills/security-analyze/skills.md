---
name: security-analyze
description: Deep-dive analysis of a single security issue. Reads affected code, understands vulnerability, and researches best practices for remediation.
allowed-tools: Read, Grep, Glob, WebSearch, Agent, Write
triggers: analyze issue, understand vulnerability, investigate security issue
---

# Security Issue Analyzer Skill

Perform deep-dive analysis of a single security issue to understand the vulnerability and research remediation approaches.

## When to Use

Use this skill after `/security-triage` to:
- Analyze a specific security issue in depth
- Understand the vulnerability mechanism
- Research best practices for fixing it
- Identify potential side effects of the fix

## Prerequisites

- Issue ID or Rule ID from triage results
- `week6/semgrep-results.json` must exist

## Instructions

### Phase 1: Extract Issue Details

1. Get the issue ID from the user or previous triage results
2. Extract issue details from semgrep-results.json:
   - Rule ID and category
   - Affected files and line numbers
   - Code snippet showing the vulnerability
   - Severity level

### Phase 2: Launch Security Analyzer Agent

Use the Agent tool to create and run a specialized analysis agent:

```
Launch security-analyzer-agent with:
- subagent_type: "general-purpose"
- name: "security-analyzer-agent"
- prompt: "You are a security analysis specialist. Analyze security issue '{issue_id}':

1. Read week6/semgrep-results.json to extract details for issue '{issue_id}'
2. Read all affected files mentioned in the finding
3. Understand the vulnerability:
   - What is the security flaw?
   - How could it be exploited?
   - What is the impact if exploited?
4. Research OWASP best practices for this issue type
5. Identify safe remediation approaches
6. Document potential side effects of the fix
7. Create a detailed analysis document saved to week6/analysis-{issue_id}.md

The analysis should include:
- Vulnerability description
- Exploitation scenario
- Impact assessment
- Recommended fix approaches
- Potential side effects
- References to OWASP/CVE documentation"
```

### Phase 3: Present Analysis Summary

Create a concise summary for the user:

```markdown
# Security Issue Analysis: [Issue Title]

## Issue Details
- **Rule ID**: [rule-id]
- **Category**: [SAST/Secrets/SCA]
- **Severity**: CRITICAL/HIGH/MEDIUM/LOW
- **File**: [path/to/file.py:123]

## Vulnerability Description
[Explain what the security flaw is]

## Exploitation Scenario
[How could an attacker exploit this?]

## Impact
[What happens if exploited?]

## Recommended Fix
[Best practice approach to fix this]

## Potential Side Effects
[What else might this fix affect?]

## References
- OWASP: [link]
- CVE: [link if applicable]
```

## Output

- `week6/analysis-{issue_id}.md` - Detailed analysis document
- Summary presented to user

## Example Usage

**User**: "Analyze issue python.sql-injection"

**Response**:
```
Launching security-analyzer-agent to analyze python.sql-injection...

[Reading files and analyzing...]

## Security Issue Analysis: SQL Injection Vulnerability

### Issue Details
- **Rule ID**: python.sql-injection
- **Category**: SAST
- **Severity**: HIGH
- **File**: backend/app/routes.py:42

### Vulnerability Description
The application constructs SQL queries by concatenating user input directly into the query string, allowing attackers to inject malicious SQL code.

### Exploitation Scenario
An attacker could send: `id=1 OR 1=1` to return all records, or `id=1; DROP TABLE users--` to delete the users table.

### Impact
- Data exfiltration
- Data deletion
- Authentication bypass
- Remote code execution (in some cases)

### Recommended Fix
Use parameterized queries with SQLAlchemy's safe query methods:
```python
# Instead of:
query = f"SELECT * FROM users WHERE id = {user_id}"

# Use:
query = text("SELECT * FROM users WHERE id = :id")
result = db.execute(query, {"id": user_id})
```

### Potential Side Effects
- Need to ensure all query parameters are properly typed
- May require updates to test cases

### References
- OWASP SQL Injection: https://owasp.org/www-community/attacks/SQL_Injection
- SQLAlchemy Safe Queries: [link]

Detailed analysis saved to: week6/analysis-python.sql-injection.md
```

## Next Steps

After analysis, proceed to `/security-fix` to implement the remediation.
