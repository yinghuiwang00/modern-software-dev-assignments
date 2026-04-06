---
name: security-scan
description: Execute Semgrep security scan on codebase and parse results. Automatically categorizes findings (SAST/Secrets/SCA) and saves structured output.
allowed-tools: Bash, Read, Write, Grep, Glob
triggers: security scan, run semgrep, scan for vulnerabilities, semgrep scan
---

# Security Scanner Skill

Execute Semgrep security scan on the week6 codebase and parse results.

## When to Use

Use this skill when you need to:
- Run a security scan on the codebase
- Check for vulnerabilities
- Analyze code quality issues
- Scan for secrets and dependencies

## Prerequisites

Semgrep must be available in the system PATH (no installation needed per assignment).

## Instructions

### Phase 1: Navigate to Parent Directory

```bash
cd /home/ericwang/workspace/AI_Coding/College_Application_03.08/modern-software-dev-assignments/
```

### Phase 2: Run Semgrep Scan

Execute the comprehensive scan:

```bash
# Run scan with JSON output for parsing
semgrep scan week6 --json --output=week6/semgrep-results.json

# Also generate SARIF format for tool compatibility
semgrep scan week6 --sarif --output=week6/semgrep-results.sarif
```

### Phase 3: Parse and Categorize Results

Read the JSON output and categorize findings:

1. **Read the results**:
   ```bash
   cat week6/semgrep-results.json | jq '.'
   ```

2. **Categorize by type**:
   - **SAST** (Static Application Security Testing): Code vulnerabilities
   - **Secrets**: Hardcoded secrets/tokens
   - **SCA** (Software Composition Analysis): Dependency vulnerabilities

3. **Generate summary**:
   - Count total findings per category
   - Identify severity distribution
   - Note any immediate CRITICAL issues

### Phase 4: Save Summary

Create a summary document:

```markdown
# Semgrep Scan Summary

**Scan Date**: [Date]
**Target**: week6/

## Findings Overview
- Total findings: [N]
  - SAST: [N]
  - Secrets: [N]
  - SCA: [N]

## Severity Distribution
- CRITICAL: [N]
- HIGH: [N]
- MEDIUM: [N]
- LOW: [N]
- INFO: [N]

## Files Scanned
- Backend: week6/backend/
- Frontend: week6/frontend/
- Dependencies: week6/requirements.txt
- Config: week6/

## Next Steps
Proceed with /security-triage to analyze and prioritize findings.
```

## Output Files

- `week6/semgrep-results.json` - Full scan results in JSON format
- `week6/semgrep-results.sarif` - Scan results in SARIF format
- `week6/semgrep-summary.md` - Human-readable summary

## Example Usage

**User**: "Run a security scan"

**Response**:
```
Executing security scan on week6 directory...

[semgrep output...]

Scan complete! Found 25 findings:
- SAST: 18
- Secrets: 3
- SCA: 4

Severity breakdown:
- CRITICAL: 2
- HIGH: 5
- MEDIUM: 10
- LOW: 8

Results saved to week6/semgrep-results.json

Next: Use /security-triage to analyze and prioritize these findings.
```

## Notes

- Semgrep is already installed and available
- Scan runs from parent directory using `semgrep scan week6`
- JSON output enables automated parsing and analysis
- All findings are saved for reference during triage
