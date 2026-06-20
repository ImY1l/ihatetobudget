# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Maintenance activities are systematically categorized according to the **ISO/IEC 14764:2022** software engineering maintenance taxonomy.

---

## [2.0.0] - 2026-06-21 (Academic Evolution Release)

This release represents a comprehensive 12-week software evolution cycle, modernizing a legacy single-tenant application into a secure, multi-tenant financial management platform with improved test coverage, deployment reliability, and maintainability.

### Security (Preventive Maintenance)
- Upgraded backend framework from **Django 3.1.14 (EOL)** to **Django 4.2 LTS**, ensuring security support until April 2026.
- Reduced known security vulnerabilities (CVEs) by **97%** (from 92 down to 3 low-severity issues) through dependency upgrades and automated scanning.
- Integrated automated security tooling into the development workflow:
  - `bandit` for static security analysis of Python code.
  - `safety` for dependency vulnerability scanning.
  - `pre-commit` hooks for automated enforcement of quality and security checks prior to integration.

### Configuration & Deployment (Corrective Maintenance)
- Externalized sensitive infrastructure configuration using `django-environ` (12-Factor App methodology).
- Removed all hardcoded secrets (including `SECRET_KEY`); the application now triggers a `RuntimeError` if required environment variables are missing.
- Resolved all 5 critical Django `manage.py check --deploy` production security warnings:
  - Enabled HTTP Strict Transport Security (HSTS).
  - Secured session and CSRF cookies (`SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`).
  - Enforced strict `ALLOWED_HOSTS` validation.
- Added a persistent named Docker volume (`media_volume`) mapped to `/usr/src/app/media` to ensure uploaded receipt files survive container restarts.

### Functional Enhancements (Adaptive Maintenance)
- Implemented a secure multi-tenant authentication system:
  - Self-service user registration with email verification.
  - OWASP-aligned password validation (PBKDF2 hashing, complexity requirements).
- Introduced the **BudgetLimit** model for proactive financial planning:
  - Category-based monthly budget tracking.
  - Database-level constraint enforcement using `unique_together` to prevent duplicate entries.
- Added authenticated CSV export functionality (`export_csv_view`) for user financial data portability.
- Enabled receipt upload functionality using a `FileField` on the `Expense` model, backed by persistent Docker storage.

### Quality Improvements (Perfective Maintenance)
- Increased automated test coverage from a **42% baseline to 91%** on core modules using `pytest` and `coverage.py`.
- Implemented a persistent dark mode toggle utilizing `localStorage` and the `data-bs-theme` attribute for improved accessibility (WCAG AA compliance).
- Enforced strict PEP 8 compliance and standardized codebase formatting using `black` and `flake8`.

### Breaking Changes
- **Environment Configuration:** A `.env` file is now strictly required. The application will fail to start without the necessary environment variables defined (see `.env.example`).
- **Database Schema:** - New model added: `BudgetLimit`.
  - Updated model: `Expense` (added `receipt` and `user` fields).
  - Migration required: `python manage.py migrate`.
- **Runtime Requirements:** Minimum Python version updated from 3.8 to **3.10+** to support modern cryptographic libraries and Django 4.2 LTS.

### Migration Guide
1. Clone the updated repository and navigate to the project root.
2. Create a `.env` file based on the provided `.env.example` and populate the required variables (e.g., `SECRET_KEY`, `DEBUG`).
3. Install updated dependencies via Pipenv:
   ```bash
   pipenv install --deploy
   ```

4. Apply the backward-compatible database migrations:
```bash
pipenv run python manage.py migrate
```

5. Restart application services (Docker Compose or local runtime).

---

### Contributors (CSE6364 Group 4)

* Mohammed Yousef Mohammed Abdulkarem — Preventive Maintenance & Budget Module Design
* Mohammed Aamena Mohammed Abdulkarem — Corrective Maintenance & Infrastructure Hardening
* Farah Hanim Binti Mohd Zamri — Perfective Testing QA Gates, Authentication & UI Enhancement

---

## [1.5.7] - 2022-12-24 (Legacy Baseline Archive)

### System State (Pre-Academic Refactor)

* Single-tenant architecture without user isolation or self-service registration.
* Core framework: Django 3.1.14 (Reached End-of-Life in April 2022).
* No budget tracking, financial planning, or data export capabilities.
* Initial automated test coverage measured at approximately 42%.
* Presence of multiple unresolved security and deployment risks:
* 92 known CVEs in locked dependencies.
* Hardcoded production secrets in settings.py.
* Stateless file storage in the containerized environment.
* 5 critical warnings from `manage.py check --deploy`.
