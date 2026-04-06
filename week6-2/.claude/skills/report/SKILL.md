---
name: report
description: Generate final security report documenting findings, fixes, and verification
---

# Report Skill - Generate Final Security Report

## Overview

Compiles all security analysis findings, fixes, and verification results into a comprehensive, professional report suitable for assignment submission.

## Usage

```
/report
```

## What It Does

1. Invokes the `report-generator` agent
2. Reads Semgrep results
3. Reads security triage report
4. Reads individual fix documentation files
5. Compiles findings overview
6. Documents each fix with before/after comparisons
7. Adds verification results
8. Generates `SECURITY_REPORT.md`

## Report Structure

The generated report includes:

1. **Executive Summary** - Brief overview of work completed
2. **Brief Findings Overview** - Scan summary with categories
3. **Three Fixes** - Detailed documentation of each fix:
   - Issue details (file, line, rule, severity)
   - Risk description
   - Change applied (before/after code)
   - Explanation of mitigation
4. **Verification** - Test results and re-scan confirmation
5. **Conclusion** - Summary of work completed

## Expected Output

A summary including:
- Report file path
- Sections included
- Total findings documented
- Fixes documented

## Example Output

```
Generating final security report...

Report generated!
- File: SECURITY_REPORT.md
- Sections: 5 (Summary, Findings, 3 Fixes, Verification, Conclusion)
- Total findings documented: 42
- Fixes documented: 3

Ready for assignment submission!
```

## Prerequisites

- Semgrep scan must have been run
- Security analysis must be complete
- All fixes must be documented
- Tests must have been run

## Required Files

The following files must exist:
- `semgrep-results.json` - Scan results
- `security-triage-report.md` - Triage analysis
- `security-fix-1.md` - First fix documentation
- `security-fix-2.md` - Second fix documentation
- `security-fix-3.md` - Third fix documentation
- `test-results.md` - Test verification

## Error Handling

If required files are missing:
- List which files are missing
- Suggest running previous steps
- Generate report with available information
- Note what's missing in the report

## Assignment Requirements

The report will include:

### Brief Findings Overview
- ✓ Categories reported (SAST/Secrets/SCA)
- ✓ False positives with explanations

### Three Fixes (before → after)
For each fix:
- ✓ File and line(s)
- ✓ Rule/category Semgrep flagged
- ✓ Brief risk description
- ✓ Change (code diff or explanation)
- ✓ Why this mitigates the issue

## Next Steps

After report generation:
- Review `SECURITY_REPORT.md`
- Make any manual adjustments if needed
- Submit to Gradescope
- Push changes to GitHub

## Related Commands

- `/scan` - Run Semgrep scan
- `/analyze` - Analyze results
- `/fix` - Apply fixes
- `/verify` - Verify fixes
- `/workflow` - Run complete end-to-end process
