# Issue Templates — ihatetobudget

---

## Template 1: Bug Report

```markdown
---
name: Bug Report
about: Report a defect or unexpected behaviour
title: "[BUG] <short description>"
labels: bug, needs-triage
assignees: ''
---

## Summary

<!-- A clear and concise description of the bug. -->

## Steps to Reproduce

1. Go to '...'
2. Click on '...'
3. Enter value '...'
4. Observe error

## Expected Behaviour

<!-- What should have happened? -->

## Actual Behaviour

<!-- What actually happened? Include error messages, stack traces, or screenshots. -->

## Environment

| Item | Detail |
|---|---|
| OS | e.g. Windows 11 / Ubuntu 22.04 |
| Browser (if UI) | e.g. Chrome 124, Firefox 126 |
| Python version | e.g. 3.11.4 |
| Django version | e.g. 4.2.11 |
| Deployment | Local / Docker / Production |

## Reproduction Rate

- [ ] Always
- [ ] Intermittent (~___% of the time)
- [ ] Only happened once

## Related Files / Views

<!-- Which view, model, or template is involved? e.g. `sheets/views.py export_csv_view` -->

## Suggested Fix (optional)

<!-- If you have a hypothesis or patch, describe it here. -->

## Checklist

- [ ] I searched existing issues and this is not a duplicate
- [ ] I can reproduce this reliably
- [ ] I am running the latest version of the branch
```

---

## Template 2: Feature Request / Enhancement

```markdown
---
name: Feature Request / Enhancement
about: Suggest a new feature or improvement
title: "[FEAT] <short description>"
labels: enhancement
assignees: ''
---

## Problem Statement

<!-- What problem does this feature solve? Who is affected and how often? -->

## Proposed Solution

<!-- Describe the feature you would like. Be as specific as possible. -->

## Maintenance Classification

<!-- Select the ISO/IEC 14764 maintenance type that best fits. -->

- [ ] **Corrective** — fixes a defect
- [ ] **Adaptive** — adapts to a changed environment (e.g. dependency upgrade)
- [ ] **Perfective** — improves quality, performance, or usability
- [ ] **Preventive** — reduces future maintenance risk

## Acceptance Criteria

<!-- Define what "done" looks like. Use Given/When/Then or bullet points. -->

- [ ] Criterion 1: ...
- [ ] Criterion 2: ...
- [ ] Criterion 3: ...

## Alternatives Considered

<!-- What other approaches did you consider and why did you reject them? -->

## UI / API Impact

<!-- Describe any new endpoints, URL changes, model changes, or template changes needed. -->

## Test Plan

<!-- How should this be tested? Outline at least two test cases. -->

| Test Case | Input | Expected Output |
|---|---|---|
| Happy path | ... | ... |
| Edge case | ... | ... |

## Additional Context

<!-- Screenshots, mockups, related issues, or links to prior discussion. -->
```

---

## Template 3: Test Failure / Coverage Gap

```markdown
---
name: Test Failure / Coverage Gap
about: Report a failing test, flaky test, or area with insufficient coverage
title: "[TEST] <test name or area>"
labels: testing, coverage
assignees: ''
---

## Test Identifier

<!-- Full test path, e.g. sheets/tests/test_views_comprehensive.py::ExportCsvViewTestCase::test_csv_only_contains_own_expenses -->

## Failure Type

- [ ] Test is failing (assertion error / exception)
- [ ] Test is flaky (passes sometimes)
- [ ] Coverage gap — branch/line not covered
- [ ] Test is slow (>1s for a unit test)

## Failure Output

```
<!-- Paste the pytest/coverage output here -->
```

## Root Cause (if known)

<!-- Is this a test problem or a production code bug? -->

## Suggested Fix

<!-- How should the test or the production code be corrected? -->

## Coverage Impact

<!-- Which file and line range lacks coverage? Run: pipenv run pytest --cov=. --cov-report=term-missing -->

## Checklist

- [ ] I have confirmed this fails on a clean checkout
- [ ] I have checked for import errors and missing fixtures
- [ ] I have attached the full traceback above
```

---

## Template 4: Documentation Issue

```markdown
---
name: Documentation Issue
about: Report missing, incorrect, or outdated documentation
title: "[DOCS] <short description>"
labels: documentation
assignees: ''
---

## Document Affected

<!-- e.g. README.md, DEVELOPER_DOCUMENTATION.md, TEST_DOCUMENTATION.md, code docstring in sheets/views.py -->

## Issue Type

- [ ] Missing documentation
- [ ] Incorrect / outdated content
- [ ] Unclear explanation
- [ ] Broken link or reference

## Current Content (if applicable)

<!-- Paste the incorrect or unclear text -->

## Suggested Correction

<!-- What should the documentation say instead? -->

## Why This Matters

<!-- Who is impacted and how? e.g. "New developers cannot set up the project because the env variable is undocumented." -->
```

---

## Template 5: Security Vulnerability

```markdown
---
name: Security Vulnerability
about: Report a security issue (consider reporting privately via email for critical issues)
title: "[SEC] <brief description — do not include exploit details>"
labels: security, priority-high
assignees: ''
---

> ⚠️ **For critical vulnerabilities (data leakage, authentication bypass, RCE), please report privately rather than opening a public issue.**

## Vulnerability Type

- [ ] Authentication / authorisation bypass
- [ ] Data leakage (e.g. user data returned for wrong user)
- [ ] Injection (SQL, template, command)
- [ ] CSRF / XSS
- [ ] Insecure direct object reference (IDOR)
- [ ] Dependency CVE
- [ ] Other: ___

## Affected Component

<!-- e.g. `export_csv_view` in `sheets/views.py` -->

## Description

<!-- Describe the vulnerability. For public issues, omit exact exploit steps. -->

## Impact

<!-- What data or functionality could be compromised? -->

## Suggested Mitigation

<!-- e.g. "Add `.filter(user=request.user)` to the queryset in `export_csv_view`." -->

## CVE / Reference (if known)

<!-- Link to NVD, GitHub Advisory, or related CVE. -->

## Checklist

- [ ] I have checked the latest version to confirm this is not already fixed
- [ ] I understand that critical issues should be reported privately
```