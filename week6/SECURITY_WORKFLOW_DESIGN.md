# Security Workflow Design: Semgrep Scan & Remediation

## Overview
This document describes the workflow, skills, and subagents designed for the Week 6 security assignment.

## Workflow Phases

### Phase 1: Initial Scan
- Execute `semgrep scan week6` from parent directory
- Parse and categorize findings (SAST/Secrets/SCA)

### Phase 2: Triage & Selection
- Analyze all findings
- Rate by severity (CRITICAL/HIGH/MEDIUM/LOW)
- Identify false positives
- Select top 3 issues to fix

### Phase 3: Remediation Loop (3 iterations per issue)
- Analyze the security issue
- Implement fix using TDD (RED-GREEN-IMPROVE)
- Verify fix with tests and re-scan

### Phase 4: Documentation
- Generate comprehensive report
- Document before/after for each fix
- Explain mitigation strategies

## Skills Created

### 1. /security-scan
**Purpose**: Execute Semgrep security scan and parse results
**File**: ~/.claude/skills/security-scan/SKILL.md
**Key Command**: `semgrep scan week6 --json --output=week6/semgrep-results.json`

### 2. /security-triage
**Purpose**: Analyze and prioritize security findings
**File**: ~/.claude/skills/security-triage/SKILL.md
**Subagent**: security-triage-agent

### 3. /security-analyze
**Purpose**: Deep-dive analysis of single security issue
**File**: ~/.claude/skills/security-analyze/SKILL.md
**Subagent**: security-analyzer-agent

### 4. /security-fix
**Purpose**: Fix security issues using TDD
**File**: ~/.claude/skills/security-fix/SKILL.md
**Subagent**: fix-implementer-agent

### 5. /security-verify
**Purpose**: Verify security fixes are correct
**File**: ~/.claude/skills/security-verify/SKILL.md
**Subagent**: test-validator-agent

### 6. /security-report
**Purpose**: Generate comprehensive security remediation report
**File**: ~/.claude/skills/security-report/SKILL.md
**Subagent**: report-generator-agent
**Output**: week6/SECURITY_FIXES.md

## Subagents Created

### 1. security-triage-agent
Analyzes semgrep findings, rates by severity, identifies false positives, recommends top issues.

### 2. security-analyzer-agent
Deep analysis of single security issue, understands vulnerability, researches best practices.

### 3. fix-implementer-agent
Implements fixes following TDD principles (RED-GREEN-IMPROVE cycle).

### 4. test-validator-agent
Verifies fixes by running tests, smoke testing, and re-running semgrep.

### 5. report-generator-agent
Generates comprehensive security report with findings and before/after documentation.

## Key Commands

```bash
# Initial scan
cd /home/ericwang/workspace/AI_Coding/College_Application_03.08/modern-software-dev-assignments/
semgrep scan week6 --json --output=week6/semgrep-results.json

# Verify fix
cd week6/backend && python -m pytest tests/ -v --cov
cd week6/frontend && npm test

# Re-scan
cd ../..
semgrep scan week6
```

## Deliverables

1. **SECURITY_FIXES.md** - Comprehensive report with:
   - Findings overview (SAST/Secrets/SCA)
   - 3 fixes with before/after code
   - Risk descriptions
   - Mitigation explanations

2. **semgrep-results.json** - Original scan results

3. **Fixed code** - Remediated vulnerabilities
