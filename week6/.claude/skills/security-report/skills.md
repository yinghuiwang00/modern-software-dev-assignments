---
name: security-report
description: Generate comprehensive security remediation report. Compiles findings overview, documents 3 fixes with before/after comparisons, and explains mitigation strategies.
allowed-tools: Read, Write, Grep, Glob, TaskGet, Agent
triggers: generate security report, create security findings, document security fixes
---

# Security Report Generator Skill

Generate a comprehensive security remediation report documenting all findings and fixes.

## When to Use

Use this skill after completing all 3 security fixes to:
- Compile a final report for submission
- Document all findings and fixes
- Create before/after comparisons
- Explain mitigation strategies

## Prerequisites

- `week6/semgrep-results.json` - Original scan results
- `week6/analysis-{issue_id}.md` - Analysis for each fixed issue
- `week6/fix-{issue_id}.md` - Fix documentation for each issue
- `week6/verification-{issue_id}.md` - Verification for each issue

## Instructions

### Phase 1: Gather All Documentation

Read all relevant files:
1. Original semgrep results
2. Analysis documents for all 3 issues
3. Fix documents for all 3 issues
4. Verification documents for all 3 issues

### Phase 2: Launch Report Generator Agent

Use the Agent tool to create and run a report generation agent:

```
Launch report-generator-agent with:
- subagent_type: "general-purpose"
- name: "report-generator-agent"
- prompt: "You are a technical documentation specialist. Generate a comprehensive security remediation report.

**Input Files:**
- week6/semgrep-results.json
- week6/analysis-*.md (3 files)
- week6/fix-*.md (3 files)
- week6/verification-*.md (3 files)

**Report Structure:**

1. **Findings Overview**
   - Total findings count
   - Breakdown by category (SAST/Secrets/SCA)
   - Severity distribution
   - False positives ignored (with reasons)

2. **Three Fixes (Before → After)**
   For each fixed issue:
   - File and line(s)
   - Rule/category Semgrep flagged
   - Brief risk description
   - Before code (the vulnerable code)
   - After code (the fix)
   - Your change explanation
   - Why this mitigates the issue

3. **Verification Summary**
   - For each fix: test results, semgrep confirmation
   - Overall verification status

**Requirements:**
- Read all input files
- Compile information into a cohesive report
- Use clear, professional language
- Include code snippets for before/after
- Explain the security reasoning
- Save the report as week6/SECURITY_FIXES.md

**Output Format:** Markdown document suitable for assignment submission"
```

### Phase 3: Review and Finalize

After the agent generates the report:

1. Read the generated report:
   ```bash
   cat week6/SECURITY_FIXES.md
   ```

2. Verify completeness:
   - [ ] Findings overview included
   - [ ] All 3 fixes documented
   - [ ] Before/after code included
   - [ ] Risk descriptions clear
   - [ ] Mitigation explanations present
   - [ ] Verification summary included

3. Check formatting:
   - Proper markdown syntax
   - Code blocks properly formatted
   - Consistent structure

## Report Template

The generated report should follow this structure:

```markdown
# Security Remediation Report

## Assignment Overview
This report documents the security vulnerabilities found by Semgrep and the remediation steps taken to address them.

## Findings Overview

### Scan Summary
- **Scan Date**: [Date]
- **Target**: week6/
- **Total Findings**: [N]

### Findings by Category
- **SAST** (Static Application Security Testing): [N] findings
- **Secrets**: [N] findings
- **SCA** (Software Composition Analysis): [N] findings

### Severity Distribution
- **CRITICAL**: [N]
- **HIGH**: [N]
- **MEDIUM**: [N]
- **LOW**: [N]
- **INFO**: [N]

### False Positives Ignored
- [Rule ID]: [Reason why this is a false positive]

---

## Fix 1: [Issue Title]

### Issue Details
- **File**: [path/to/file.py:123]
- **Rule**: [semgrep-rule-id]
- **Category**: [SAST/Secrets/SCA]
- **Severity**: [CRITICAL/HIGH/MEDIUM/LOW]

### Risk Description
[Explain what the vulnerability is and its potential impact]

### Before
```python
# Vulnerable code here
```

### After
```python
# Fixed code here
```

### Changes Made
[List the specific changes made to fix the issue]

### Why This Mitigates the Issue
[Explain how the fix addresses the vulnerability and why it's secure]

### Verification
- [x] Tests pass
- [x] Issue confirmed resolved in Semgrep
- [x] No new issues introduced

---

## Fix 2: [Issue Title]
[Same structure as Fix 1]

---

## Fix 3: [Issue Title]
[Same structure as Fix 1]

---

## Verification Summary

### Fix 1: [Issue Title]
- **Tests**: ✅ PASSED
- **Semgrep**: ✅ Resolved
- **Status**: ✅ VERIFIED

### Fix 2: [Issue Title]
- **Tests**: ✅ PASSED
- **Semgrep**: ✅ Resolved
- **Status**: ✅ VERIFIED

### Fix 3: [Issue Title]
- **Tests**: ✅ PASSED
- **Semgrep**: ✅ Resolved
- **Status**: ✅ VERIFIED

## Conclusion
[Summary of the security improvements made]
```

## Output

- `week6/SECURITY_FIXES.md` - Comprehensive final report

## Example Usage

**User**: "Generate the security report"

**Response**:
```
Launching report-generator-agent to compile security remediation report...

Reading input files:
- week6/semgrep-results.json ✓
- week6/analysis-python.sql-injection.md ✓
- week6/fix-python.sql-injection.md ✓
- week6/verification-python.sql-injection.md ✓
- [All 9 files read]

Generating report...

Report generated successfully! ✓

## Summary

**Findings Overview:**
- Total findings: 25
- SAST: 18
- Secrets: 3
- SCA: 4

**Fixes Documented:**
1. SQL Injection Vulnerability (HIGH)
2. Hardcoded API Key (CRITICAL)
3. Insecure Random Number (HIGH)

**Verification Status:**
- All 3 fixes verified ✅
- All tests passing ✅
- No new issues introduced ✅

Full report saved to: week6/SECURITY_FIXES.md

The report is ready for submission!
```

## Next Steps

After report generation:
1. Review the report for accuracy
2. Make any manual adjustments if needed
3. Commit all changes to git
4. Submit via Gradescope
