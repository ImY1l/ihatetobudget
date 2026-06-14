# Issue Templates — ihatetobudget
---

## Template: Security Vulnerability

**File:** `.github/ISSUE_TEMPLATE/security.md`

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
---