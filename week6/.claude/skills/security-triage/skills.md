---
name: security-triage
description: Analyze and prioritize Semgrep security findings. Rates by severity, identifies false positives, and recommends top issues to fix.
allowed-tools: Read, Grep, Glob, AskUserQuestion, Agent, TaskCreate
triggers: triage findings, prioritize issues, analyze security results
---

# Security Triage Skill

Analyze and prioritize Semgrep security findings to identify the most critical issues to fix.

## When to Use

Use this skill after running `/security-scan` to:
- Analyze all security findings
- Rate issues by severity
- Identify false positives or noisy rules
- Recommend top priority issues to fix

## Prerequisites

- `week6/semgrep-results.json` must exist from `/security-scan`
- Semgrep scan must have been completed

## Instructions

### Phase 1: Read and Parse Results

1. Read the semgrep results file:
   ```bash
   cat week6/semgrep-results.json
   ```

2. Parse the JSON structure to extract:
   - All findings with their metadata
   - Severity levels
   - Rule IDs
   - File locations
   - Code snippets

### Phase 2: Launch Security Triage Agent

Use the Agent tool to create and run a specialized triage agent:

```
Launch security-triage-agent with:
- subagent_type: "general-purpose"
- name: "security-triage-agent"
- prompt: "You are a security triage specialist. Analyze the Semgrep findings in week6/semgrep-results.json and:

1. Read and parse the JSON results
2. Categorize all findings by severity (CRITICAL/HIGH/MEDIUM/LOW)
3. Identify any false positives or noisy rules (explain why)
4. Recommend the top 3 issues to fix (prioritize CRITICAL and HIGH)
5. For each recommended issue, provide:
   - Issue ID / Rule ID
   - File path and line numbers
   - Severity level
   - Brief description of the vulnerability
   - Why this should be fixed (risk assessment)

Return your analysis in a structured format that can be used for selecting issues to fix."
```

### Phase 3: Present Findings to User

Create a summary of the triage results:

```markdown
# Security Triage Results

## Summary
- Total findings: [N]
- CRITICAL: [N]
- HIGH: [N]
- MEDIUM: [N]
- LOW: [N]

## False Positives Identified
- [Rule ID]: [Reason why this is a false positive]

## Top 3 Issues to Fix

### 1. [Issue Title]
- **Rule**: [rule-id]
- **Severity**: CRITICAL/HIGH
- **File**: [path/to/file.py:123]
- **Risk**: [description]
- **Why Fix**: [justification]

### 2. [Issue Title]
...

### 3. [Issue Title]
...
```

### Phase 4: Confirm Selection

Use AskUserQuestion to confirm the user wants to proceed with these 3 issues:

```
AskUserQuestion:
- Question: "I've identified the top 3 security issues. Do you want to fix these 3 issues, or would you like to select different ones?"
- Options:
  - "Fix these 3 issues"
  - "Select different issues"
  - "Review full list first"
```

## Output

- Triage analysis from security-triage-agent
- User confirmation on which issues to fix
- List of 3 issue IDs to proceed with remediation

## Example Usage

**User**: "Triage the security findings"

**Response**:
```
Launching security-triage-agent to analyze findings...

[Agent analysis results...]

## Security Triage Results

### Summary
Found 25 findings:
- CRITICAL: 2
- HIGH: 5
- MEDIUM: 10
- LOW: 8

### Top 3 Issues to Fix

1. **Hardcoded API Key** (CRITICAL)
   - Rule: detect-secrets
   - File: backend/app/config.py:15
   - Risk: Credential exposure in source code

2. **SQL Injection Vulnerability** (HIGH)
   - Rule: python.sql-injection
   - File: backend/app/routes.py:42
   - Risk: SQL injection via user input

3. **Insecure Random Number** (HIGH)
   - Rule: python.insecure-random
   - File: backend/app/auth.py:78
   - Risk: Predictable token generation

Do you want to fix these 3 issues?
```

## Next Steps

After user confirmation, proceed to `/security-analyze` for each issue.
