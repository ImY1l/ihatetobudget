# Issue Templates — ihatetobudget
---

## Template: Test Failure / Coverage Gap

**File:** `.github/ISSUE_TEMPLATE/test_failure.md`

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