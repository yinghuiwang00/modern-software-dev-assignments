---
name: scan
description: Run Semgrep security scan and save results
---

# Scan Skill - Run Semgrep Security Scan

## Overview

Runs a comprehensive Semgrep security scan on the week6 codebase and saves the results for analysis.

## Usage

```
/scan
```

## What It Does

1. Runs `semgrep scan` command
2. Saves results to `semgrep-results.json`
3. Returns a summary of findings

## Command

```bash
semgrep scan --output semgrep-results.json --json
```

## Expected Output

A summary including:
- Total number of findings
- Breakdown by severity (Critical, High, Medium, Low)
- Categories found (SAST, Secrets, SCA)

## Example Output

```
Running Semgrep scan...

Scan complete!
- Total findings: 42
- Critical: 3 | High: 8 | Medium: 18 | Low: 13
- Results saved to: semgrep-results.json
```

## Error Handling

If Semgrep is not installed or fails:
- Error message with details
- Instructions to install Semgrep
- Link to Semgrep documentation

## Next Steps

After running scan:
- Use `/analyze` to categorize and triage findings
- Use `/workflow` to run complete analysis and fix process
