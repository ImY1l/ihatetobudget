
---
## Summary

<!-- One or two sentences describing what this PR does and why. -->
<!-- issue number -->

---

## Maintenance Type (ISO/IEC 14764)

<!-- Select the type that best describes this change. -->

- [ ] **Corrective** — fixes a defect
- [ ] **Adaptive** — responds to a changed environment (e.g. dependency, OS, framework upgrade)
- [ ] **Perfective** — improves quality, performance, UI, or maintainability without fixing a bug
- [ ] **Preventive** — restructuring or documentation to prevent future failures

---

## Changes Made

<!-- Bullet list of concrete changes. Be specific about files, functions, and models affected. -->

- 
- 
- 

---

## Enhancement Reference (if applicable)

| Enhancement # | Description | Assignee |
|---|---|---|
| #__ | | |

---

## Testing

### What was tested?

<!-- Describe the tests added or updated. -->

- [ ] New unit tests added in `______________`
- [ ] Existing tests updated in `______________`
- [ ] Manual testing performed (describe below)

### Test results

```
# Paste relevant pytest output or coverage summary here
# e.g.: pipenv run pytest --cov=. --cov-report=term-missing
```

### Coverage impact

| Before this PR | After this PR |
|---|---|
| __% | __% |

---

## Screenshots / Screen Recordings (UI changes only)

<!-- If this PR changes any template or front-end behaviour, attach before/after screenshots. -->

| Before | After |
|---|---|
| _(screenshot)_ | _(screenshot)_ |

---

## Checklist

### Code quality

- [ ] Code follows the project's style guide (black, isort, flake8 pass)
- [ ] No debug statements (`print()`, `pdb`, `breakpoint()`) left in code
- [ ] New functions/classes have docstrings or inline comments where non-obvious

### Testing

- [ ] All existing tests pass (`pipenv run pytest`)
- [ ] New tests have been added for every new behaviour
- [ ] Coverage has not decreased (target ≥ 90%)
- [ ] Edge cases and error paths are covered

### Django specifics

- [ ] Database migrations are included if models were changed
- [ ] Migrations have been reviewed and are reversible
- [ ] New views are protected with `@login_required` / `LoginRequiredMixin` where appropriate
- [ ] No hardcoded secrets, passwords, or credentials

### Documentation

- [ ] `README.md` updated if user-facing behaviour changed
- [ ] `DEVELOPER_DOCUMENTATION.md` updated if architecture changed
- [ ] `TEST_DOCUMENTATION.md` updated if new test classes or bugs were found
- [ ] Inline comments added for complex logic

### Review

- [ ] Self-review completed (I have read every line of the diff)
- [ ] PR is scoped to a single logical change
- [ ] Commit messages are descriptive and follow the project convention

---

## Breaking Changes

<!-- List any breaking changes. If none, write "None." -->

---

## Deployment Notes

<!-- Any steps needed after merging (e.g. run migrations, update environment variables, clear cache). -->

- [ ] `python manage.py migrate` required
- [ ] New environment variable required: `_______________`
- [ ] Static files rebuild required: `python manage.py collectstatic`
- [ ] No special deployment steps needed

---

## Reviewer Notes

<!-- Anything specific you want reviewers to focus on or be aware of. -->