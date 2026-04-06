---
name: analyze
description: Analyze Semgrep results and create triage report
---

# Analyze Skill - Analyze Semgrep Results

## Overview

Analyzes Semgrep scan results, categorizes findings by type and severity, and generates a prioritized triage report.

## Usage

```
/analyze [results_file]
```

**Arguments:**
- `results_file` (optional): Path to Semgrep results JSON file. Default: `semgrep-results.json`

## What It Does

1. Invokes the `security-analyzer` agent
2. Parses Semgrep results file
3. Categorizes findings:
   - SAST (Static Application Security Testing)
   - Secrets (hardcoded credentials)
   - SCA (Software Composition Analysis - dependencies)
4. Prioritizes by severity (Critical > High > Medium > Low)
5. Identifies false positives
6. Generates `security-triage-report.md`

## Expected Output

A summary including:
- Total findings breakdown
- Top 3 prioritized issues to fix
- Path to triage report

## Example Output

```
Analyzing Semgrep results...

Analysis complete!
- Total findings: 42
- Categories: SAST (35), Secrets (2), SCA (5)
- False positives: 3

Top 3 issues prioritized:
1. SQL Injection in backend/app/routers/notes.py:71 (Critical)
2. Command Injection in backend/app/routers/notes.py:108 (High)
3. XSS in frontend/app.js:14 (Medium)

Triage report saved to: security-triage-report.md
```

## Prerequisites

- Semgrep scan must have been run first
- `semgrep-results.json` must exist

## Error Handling

If results file doesn't exist:
- Error message with instructions
- Suggestion to run `/scan` first

If results file is invalid JSON:
- Error message
- Suggestion to re-run `/scan`

## Next Steps

After analysis:
- Use `/fix <issue_number>` to fix a specific issue
- Use `/verify` to run tests after fixes
- Use `/report` to generate final report
- Use `/workflow` to run complete process

## Related Commands

- `/scan` - Run Semgrep scan first
- `/fix` - Fix specific security issues
- `/workflow` - Run complete end-to-end workflow
