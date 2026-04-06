# Security Triage Report

**Date**: 2026-04-06
**Scan Tool**: Semgrep 1.157.0
**Total Findings**: 6

## Executive Summary

The security scan identified **6 vulnerabilities** across the application. All findings are categorized as **SAST (Static Application Security Testing)** issues. No secrets or supply chain vulnerabilities were detected.

### Severity Breakdown
- **ERROR (High Severity)**: 3 findings
- **WARNING (Medium Severity)**: 3 findings

## Detailed Findings

### Critical Issues (ERROR Severity)

#### 1. SQL Injection - `backend/app/routers/notes.py:71`
- **Rule ID**: `python.sqlalchemy.security.audit.avoid-sqlalchemy-text.avoid-sqlalchemy-text`
- **CWE**: CWE-89: SQL Injection
- **OWASP**: A05:2025 - Injection
- **Description**: Using `sqlalchemy.text` bypasses SQLAlchemy's ORM protections, allowing raw SQL queries to be executed. This creates SQL injection vulnerabilities if user input can reach the query.
- **Likelihood**: LOW
- **Impact**: HIGH
- **Confidence**: MEDIUM

#### 2. Command Injection - `backend/app/routers/notes.py:112`
- **Rule ID**: `python.lang.security.audit.subprocess-shell-true.subprocess-shell-true`
- **CWE**: CWE-78: OS Command Injection
- **OWASP**: A05:2025 - Injection
- **Description**: Using `subprocess.run()` with `shell=True` spawns a command using a shell process, propagating current shell settings and variables. This makes it easier for malicious actors to execute arbitrary commands.
- **Likelihood**: HIGH
- **Impact**: LOW
- **Confidence**: MEDIUM
- **Recommended Fix**: Set `shell=False` instead

#### 3. Cross-Site Scripting (XSS) - `frontend/app.js:14`
- **Rule ID**: `javascript.browser.security.insecure-document-method.insecure-document-method`
- **CWE**: CWE-79: XSS
- **OWASP**: A05:2025 - Injection
- **Description**: User-controlled data is being inserted into the DOM using `innerHTML`, which is an anti-pattern that can lead to XSS vulnerabilities.
- **Likelihood**: LOW
- **Impact**: LOW
- **Confidence**: LOW

### Medium Severity Issues (WARNING)

#### 4. Permissive CORS Policy - `backend/app/main.py:24`
- **Rule ID**: `python.fastapi.security.wildcard-cors.wildcard-cors`
- **CWE**: CWE-942: Permissive Cross-domain Policy
- **OWASP**: A02:2025 - Security Misconfiguration
- **Description**: CORS policy allows any origin using wildcard '*'. This is insecure and should be avoided.
- **Recommendation**: Restrict CORS to specific, trusted origins only.

#### 5. Eval Usage - `backend/app/routers/notes.py:104`
- **Rule ID**: `python.lang.security.audit.eval-detected.eval-detected`
- **CWE**: CWE-95: Eval Injection
- **OWASP**: A05:2025 - Injection
- **Description**: Use of `eval()` function detected. This can be dangerous if used to evaluate dynamic content from external sources.
- **Recommendation**: Replace with safer alternatives (e.g., `json.loads` for JSON parsing).

#### 6. Dynamic urllib Use - `backend/app/routers/notes.py:124`
- **Rule ID**: `python.lang.security.audit.dynamic-urllib-use-detected.dynamic-urllib-use-detected`
- **CWE**: CWE-939: Improper Authorization
- **OWASP**: A01:2017 - Injection
- **Description**: Dynamic value being used with urllib, which supports 'file://' schemes. May allow reading arbitrary files if controlled by malicious actors.
- **Recommendation**: Validate and sanitize URLs before use, consider using `requests` library instead.

## False Positives

**No false positives identified.** All 6 findings are legitimate security concerns that should be addressed.

## Top 3 Issues to Fix

Based on severity, exploitability, and OWASP Top 10 relevance, the following 3 issues are prioritized for remediation:

### Priority #1: SQL Injection (`notes.py:71`)
**Justification**:
- ERROR severity
- OWASP A05:2025 - Injection (Top 3 vulnerability)
- CWE-89 is in CWE Top 25 (2021 & 2022)
- Direct data access compromise potential
- Can lead to data exfiltration, modification, or deletion

### Priority #2: Command Injection (`notes.py:112`)
**Justification**:
- ERROR severity
- OWASP A05:2025 - Injection (Top 3 vulnerability)
- CWE-78 is in CWE Top 25 (2021 & 2022)
- HIGH likelihood of exploitation
- Can lead to full system compromise (RCE)

### Priority #3: XSS (`app.js:14`)
**Justification**:
- ERROR severity
- OWASP A05:2025 - Injection (Top 3 vulnerability)
- CWE-79 is in CWE Top 25 (2021 & 2022)
- Client-side attack vector
- Can lead to session hijacking and data theft

## Remediation Recommendations

### Immediate Actions (This Assignment)
1. Fix SQL Injection by using SQLAlchemy ORM methods instead of raw SQL
2. Fix Command Injection by removing `shell=True` from subprocess calls
3. Fix XSS by using secure DOM manipulation methods (e.g., `textContent`)

### Follow-up Actions (Future Work)
1. Restrict CORS policy to specific origins
2. Replace `eval()` with safer alternatives
3. Implement URL validation for urllib usage or migrate to `requests`
4. Implement input validation across all endpoints
5. Add comprehensive security testing to CI/CD pipeline

## Categorization Summary

| Category | Count | Percentage |
|----------|-------|------------|
| SAST     | 6     | 100%       |
| Secrets  | 0     | 0%         |
| SCA      | 0     | 0%         |

## Conclusion

The application contains 6 security vulnerabilities, with 3 requiring immediate attention (SQL Injection, Command Injection, and XSS). All issues are exploitable and align with OWASP Top 10 injection vulnerabilities. The recommended fixes are straightforward and can be implemented without major architectural changes.

---

**Next Steps**: Proceed with fixing the top 3 prioritized issues.
