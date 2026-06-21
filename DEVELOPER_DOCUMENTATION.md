# Developer Documentation — ihatetobudget

**Project:** ihatetobudget — Open Source Personal Finance Platform  
**Course:** CSE6364 Software Maintenance and Evolution  
**Group:** Group 4  
**Maintainers:** Farah Hanim binti Mohd Zamri, Mohammed Aamena Mohammed Abdulkarem, Mohammed Yousef Mohammed Abdulkarem  
**Application version (`ihatetobudget.__version__`):** 1.5.7  
**Last Updated:** June 2026

> This document is generated strictly from the contents of the submitted codebase (models, views, templates, settings, `Pipfile`, Docker config, and CSS). Where the project's own `README.md` makes claims that could not be verified against the actual source (see Section 20), those claims are flagged separately rather than stated as fact.

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Maintenance Summary](#2-maintenance-summary)
3. [Maintenance Traceability](#3-maintenance-traceability)
4. [Screenshots](#4-screenshots)
5. [Repository Structure](#5-repository-structure)
6. [Technology Stack](#6-technology-stack)
7. [Architecture Overview](#7-architecture-overview)
8. [Data Models](#8-data-models)
9. [Views & URL Routing](#9-views--url-routing)
10. [Forms](#10-forms)
11. [Template System, Bootstrap 5 Migration & Dark Mode](#11-template-system-bootstrap-5-migration--dark-mode)
12. [Testing Infrastructure](#12-testing-infrastructure)
13. [Enhancement Details](#13-enhancement-details)
    - 13.1 [Enhancement #1 — Preventive & Corrective: Environment & Security](#131-enhancement-1--preventive--corrective-maintenance-environment--security)
    - 13.2 [Enhancement #2 — Adaptive: Models & Database](#132-enhancement-2--adaptive-enhancements-models--database)
    - 13.3 [Enhancement #3 — Adaptive: Views & Authentication](#133-enhancement-3--adaptive-enhancements-views--authentication)
    - 13.4 [Enhancement #4 — Perfective: Bootstrap 5 & Dark Mode](#134-enhancement-4--uiux-enhancements-bootstrap-5--dark-mode)
    - 13.5 [Enhancement #5 — Perfective: Testing & Quality](#135-enhancement-5--perfective-maintenance-testing--quality)
    - 13.6 [Enhancement #6 — Adaptive: Docker & Deployment](#136-enhancement-6--docker--deployment-configuration)
14. [Development Workflow](#14-development-workflow)
15. [Environment Setup (Local Development)](#15-environment-setup-local-development)
16. [Docker Setup](#16-docker-setup)
17. [Configuration Reference](#17-configuration-reference)
18. [Known Issues, Quirks & Loose Ends](#18-known-issues-quirks--loose-ends)
19. [Enhancement Log](#19-enhancement-log)

---

## 1. Project Overview

ihatetobudget is a self-hosted Django web application for tracking personal expenses, managing budget limits, uploading receipts, and visualising monthly spending patterns. The codebase's original Django settings docstring states it was generated against **Django 3.1**; it has since undergone an ISO/IEC 14764:2022-style maintenance cycle (per the project's own README framing) to address technical debt, security warnings, and missing functionality.

**Key capabilities (current codebase state):**

- Multi-user expense tracking with category assignment and receipt upload
- Monthly sheet view (per-user filtered) with day-count context for the current month
- Searchable and paginated expense history
- Budget limit tracking per category per month/year, with percentage-used calculation
- CSV export of the authenticated user's expenses
- Receipt viewing and download (single file or zipped bundle per month)
- **Bootstrap 5.3.8** front end (migrated from Bootstrap 4 — the old stylesheet is retained as a backup file, see Section 11)
- Dark mode UI toggle with `localStorage` persistence
- Self-service user registration with auto-login
- Automated test suite (`.coveragerc` scoped to `source = sheets`, `fail_under = 91`)

---

## 2. Maintenance Summary

The following maintenance activities are reflected in the current codebase, organised by **Group 4** member and by **ISO/IEC 14764:2022** maintenance type.

| # | Enhancement | Assignee | ISO/IEC 14764 Type |
|---|---|---|---|
| 1 | Preventive & Corrective Maintenance (Environment & Security) | Mohammed Aamena | Preventive + Corrective |
| 2 | Adaptive Enhancements (Models & Database) | Mohammed Yousef | Adaptive |
| 3 | Adaptive Enhancements (Views & Authentication) | Mohammed Aamena | Adaptive |
| 4 | UI/UX Enhancements (Bootstrap 5 migration & Dark Mode) | Farah Hanim | Perfective |
| 5 | Perfective Maintenance (Testing & Quality) | Farah Hanim | Perfective |
| 6 | Docker & Deployment Configuration | Mohammed Yousef | Adaptive |

### Corrective Maintenance *(Enhancement #1; Enhancement #3)*
- Resolved Django deployment-check warnings by making `SECURE_SSL_REDIRECT`, `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`, `SECURE_HSTS_SECONDS`, `SECURE_HSTS_INCLUDE_SUBDOMAINS`, and `SECURE_HSTS_PRELOAD` environment-variable driven (`ihatetobudget/settings.py`).
- Added an `IS_TEST` guard so the test client (plain HTTP) is never redirected to HTTPS during automated test runs.
- `export_csv_view` and `SheetView` scope their querysets to `request.user` so one user's data is never exposed to another.

### Adaptive Maintenance *(Enhancement #1; Enhancement #2; Enhancement #3; Enhancement #6)*
- Django pinned to **4.2.11** in `Pipfile` (comment notes the original project targeted Django 3.1).
- Added the `BudgetLimit` model and a full budget dashboard (per-category monthly spend ceilings, percentage-used calculation).
- Added receipt upload support (`Expense.receipt` `FileField`) plus dedicated receipt viewing/download views (single file and zipped bundle).
- Added a CSV export endpoint (`export_csv_view`) for the authenticated user's expenses.
- Added self-service user registration (`register_view` + `CustomUserCreationForm`) with automatic login on success.
- Containerised the application with Docker, docker-compose, Daphne (ASGI), and a Caddy reverse proxy.

### Perfective Maintenance *(Enhancement #4; Enhancement #5)*
- **Migrated the front-end from Bootstrap 4 to Bootstrap 5.3.8** (Bootswatch Litera theme). The Bootstrap 4 stylesheet is preserved on disk as `static/bootstrap4-backup.css` / `static/bootstrap4-backup.min.css` rather than deleted.
- Added a dark mode toggle using a `data-theme="dark"` attribute on `<html>`, driven by `localStorage` (`ihtb-theme` key) and an anti-flash inline script in `<head>`.
- Added a substantial automated test suite spanning view, model, form, and receipt-endpoint coverage, governed by `.coveragerc` (`fail_under = 91`).
- Implemented monthly average spend and median spend calculations on the overview page.

### Preventive Maintenance *(Enhancement #1; Enhancement #5)*
- `.pre-commit-config.yaml` configured with `isort`, `black`, and `flake8` hooks.
- `.coveragerc` scopes coverage to the `sheets` package, excluding migrations, tests, and management entry points, with a hard coverage floor (`fail_under = 91`).

---

## 3. Maintenance Traceability

| Issue/Feature ID | Maintenance Type | Enhancement # | Description | Files |
|---|---|---|---|---|
| SEC-001 | Corrective | #1 | Django `--deploy` security warnings (SSL redirect, secure cookies, HSTS) | `ihatetobudget/settings.py` |
| SEC-002 | Corrective | #1 | HTTPS redirect could break the test suite (`IS_TEST` guard added) | `ihatetobudget/settings.py` |
| TECH-001 | Adaptive | #1 | Django upgraded and pinned to 4.2.11 | `Pipfile`, `Pipfile.lock` |
| ENH-002a | Adaptive | #2 | `BudgetLimit` model added | `sheets/models.py`, `sheets/migrations/0008_*.py` |
| ENH-002b | Adaptive | #2 | Receipt upload field added to `Expense` | `sheets/models.py`, `sheets/forms.py`, `sheets/migrations/0008_*.py` |
| ENH-002c | Adaptive | #2 | Receipt viewing & download (single + zipped) | `sheets/views.py`, `sheets/urls.py`, `sheets/template/sheets/receipts_month.html` |
| ENH-002d | Adaptive | #2 | CSV export endpoint | `sheets/views.py`, `sheets/urls.py` |
| ENH-003a | Adaptive | #3 | User registration view + `CustomUserCreationForm` | `sheets/views.py`, `sheets/forms.py`, `sheets/urls.py` |
| ENH-003b | Adaptive | #3 | Budget tracking view (`budget_dashboard`) | `sheets/views.py`, `sheets/urls.py`, `sheets/template/sheets/budget.html` |
| ENH-003c | Adaptive | #3 | `SheetView` scoped to `request.user` | `sheets/views.py` |
| ENH-004a | Perfective | #4 | Bootstrap 4 → Bootstrap 5.3.8 migration | `static/bootstrap.min.css`, `ihatetobudget/template/ihatetobudget/common/base.html`, `navbar.html`; old file kept as `static/bootstrap4-backup.{css,min.css}` |
| ENH-004b | Perfective | #4 | Dark mode toggle (`data-theme`, `localStorage` key `ihtb-theme`) | `base.html`, `navbar.html`, `static/styles.css` |
| ENH-005a | Perfective | #5 | View test suite (`test_views_comprehensive.py`) — 12 classes, 55 tests | `sheets/tests/test_views_comprehensive.py` |
| ENH-005b | Perfective | #5 | Supplementary pytest view tests (`test_views.py`) — 10 tests; `test_views_extra.py` duplicates 4 of these | `sheets/tests/test_views.py`, `sheets/tests/test_views_extra.py` |
| ENH-005c | Perfective | #5 | Receipt view/download endpoint tests (`test_receipts_views.py`) — 7 tests | `sheets/tests/test_receipts_views.py` |
| ENH-005d | Perfective | #5 | Model tests (`test_models.py`) — 4 tests | `sheets/tests/test_models.py` |
| ENH-005e | Perfective | #5 | Form tests (`test_forms.py`) — 7 tests | `sheets/tests/test_forms.py` |
| ENH-006a | Adaptive | #6 | Docker + docker-compose containerised deployment | `Dockerfile`, `docker-compose.yml` |
| ENH-006b | Adaptive | #6 | Caddy reverse proxy configuration | `Caddyfile`, `Caddyfile.example` |
| ENH-006c | Adaptive | #6 | Media volume persistence for receipt uploads | `docker-compose.yml` (`media_volume`) |
| PRV-001 | Preventive | #5 | `.coveragerc` with `fail_under = 91`; `.pre-commit-config.yaml` (isort, black, flake8) | `.coveragerc`, `.pre-commit-config.yaml` |

---

## 4. Screenshots

The `screenshots/` directory contains both the original UI screenshots and a newer set with a `_new` suffix, suggesting a refreshed capture after the Bootstrap 5 migration.

| File | Likely Content |
|---|---|
| `screenshots/overview.png` | Original overview/dashboard screenshot |
| `screenshots/sheet.png` | Original monthly sheet screenshot |
| `screenshots/history.png` | Original expense history screenshot |
| `screenshots/categories.png` | Original categories list screenshot |
| `screenshots/Homepage.png` | Updated home/landing page (post Bootstrap 5) |
| `screenshots/MainDashboard.png` | Updated dashboard (post Bootstrap 5) |
| `screenshots/DarkMode.png` | Updated dashboard with **dark mode enabled** |
| `screenshots/history.png` | Updated expense history page |
| `screenshots/NewCat.png` | Updated "new category" form |

When embedding screenshots in a report, prefer the `_new` files since they reflect the current Bootstrap 5 + dark mode UI rather than the legacy Bootstrap 4 appearance.

---

## 5. Repository Structure

```
ihatetobudget/
├── ihatetobudget/                  # Django project package
│   ├── settings.py                 # Central configuration
│   ├── urls.py                     # Root URL dispatcher
│   ├── asgi.py / wsgi.py           # ASGI / WSGI entry points
│   ├── views.py                    # Project-level index view (redirect-or-landing)
│   ├── __init__.py                 # __version__ = "1.5.7"
│   ├── template/
│   │   ├── 404.html
│   │   ├── context_processors.py   # `version` context processor
│   │   ├── ihatetobudget/
│   │   │   ├── common/
│   │   │   │   ├── base.html       # Root layout; dark-mode scripts; Bootstrap 5 CDN JS
│   │   │   │   └── navbar.html     # Top navigation bar; dark-mode toggle button
│   │   │   ├── generic/
│   │   │   │   ├── new-edit-form.html
│   │   │   │   └── delete-form.html
│   │   │   └── index.html          # Public landing page (unauthenticated)
│   │   └── registration/
│   │       └── login.html
│   ├── templatetags/
│   │   └── ihatetobudget_extras.py
│   ├── tests/
│   │   ├── test_templatetags.py
│   │   ├── test_views.py
│   │   └── utils/
│   │       └── test_views.py
│   └── utils/
│       └── views.py                # Reusable view mixins
│
├── sheets/                         # Main application package
│   ├── models.py                   # Category, Expense, BudgetLimit
│   ├── models_budgetlimit_stub.txt # Stray placeholder/stub file (content: "stub") — not imported anywhere
│   ├── views.py                    # All views (functions + CBVs)
│   ├── forms.py                    # ExpenseForm, CategoryForm, BudgetLimitForm, CustomUserCreationForm
│   ├── urls.py                     # App-level URL patterns
│   ├── admin.py                    # Registers Category and Expense with Django admin
│   ├── apps.py
│   ├── cron.py                     # Monthly recurring-expense job
│   ├── migrations/                 # 0001 – 0008
│   ├── template/
│   │   ├── context_processors.py   # `sheet_date_list`, `current_sheet_date`
│   │   ├── registration/
│   │   │   └── register.html
│   │   └── sheets/
│   │       ├── index.html
│   │       ├── sheet.html
│   │       ├── history.html
│   │       ├── categories.html
│   │       ├── budget.html
│   │       ├── receipts_month.html
│   │       ├── common/
│   │       │   ├── base.html
│   │       │   └── sidebar.html
│   │       └── macros/
│   │           ├── category.html
│   │           ├── category_menu.html
│   │           ├── expense_menu.html
│   │           ├── new_expense_button.html
│   │           ├── page_header_beginning.html
│   │           ├── page_header_end.html
│   │           ├── pagination.html
│   │           ├── potential_repeated_expense_icon.html
│   │           └── sidebar_link.html
│   └── tests/
│       ├── test_forms.py
│       ├── test_models.py
│       ├── test_views.py
│       ├── test_views_comprehensive.py    # Enhancement #5 main suite
│       ├── test_views_extra.py            # Duplicates 4 tests from test_views.py
│       └── test_receipts_views.py         # Receipt view/download endpoint tests
│
├── dev/
│   ├── generate_test_data.py       # Seed script for local development
│   ├── release                     # Shell script: bumps version in README/__init__.py, tags release
│   └── README.md
├── .github/
│   ├── ISSUE_TEMPLATE/              # bug_report.md, documentation.md, feature_request.md, security.md, test_failure.md
│   └── PULL_REQUEST_TEMPLATE.md
├── media/                           # User-uploaded receipts (runtime)
├── screenshots/                     # UI screenshots (legacy + "_new" refreshed set)
├── static/
│   ├── bootstrap.min.css            # ACTIVE stylesheet — Bootstrap 5.3.8 (Bootswatch Litera)
│   ├── bootstrap4-backup.css        # Retained Bootstrap 4 stylesheet (unminified)
│   ├── bootstrap4-backup.min.css    # Retained Bootstrap 4 stylesheet (minified) — NOT referenced by any template
│   ├── styles.css                   # Custom styles + dark mode rules
│   ├── logo.png
│   └── favicon.ico
├── manage.py
├── Pipfile / Pipfile.lock
├── pyproject.toml                   # [tool.black] line-length = 80
├── Dockerfile
├── docker-compose.yml / docker-compose.yml.example
├── docker-compose.env / docker-compose.env.example
├── Caddyfile / Caddyfile.example
├── .coveragerc
├── .flake8
├── .isort.cfg
├── .pre-commit-config.yaml
├── .coverage                        # Committed coverage data file (binary; stray artifact, see Section 18)
├── db.sqlite3                       # Committed SQLite database (stray artifact, see Section 18)
├── Installation Guide.pdf           # Supplementary install guide (binary, not parsed for this document)
├── launch-instructions.txt          # Quick Docker launch notes (scratch file, see Section 18)
├── TEMPLATE_DEBUG_register.txt      # Debugging shell-command notes for register.html template resolution (scratch file, see Section 18)
├── README.md
├── CONTRIBUTING.md
└── COPYING                          # License text (MIT, per README badge)
```

---

## 6. Technology Stack

| Layer | Technology | Version |
|---|---|---|
| Language | Python | 3.10 |
| Web framework | Django | 4.2.11 (pinned in `Pipfile`) |
| ASGI server | Daphne | latest (per `Pipfile`, unpinned) |
| Database (dev) | SQLite | bundled (`db.sqlite3`) |
| Dependency manager | Pipenv | latest |
| CSS framework | **Bootstrap 5.3.8** | Bootswatch Litera theme (`static/bootstrap.min.css`) |
| Bootstrap JS | Bootstrap 5 bundle | `bootstrap@5.3.7` (CDN, `base.html`) — note the minor version mismatch with the CSS (5.3.8); both are 5.3.x and compatible |
| Color picker widget | `django-colorfield` | latest |
| Crontab integration | `django-crontab` | latest |
| Date math | `python-dateutil` | latest |
| Testing | pytest + pytest-django + Django `TestCase` | — (dev-only, per `Pipfile [dev-packages]`) |
| Coverage | pytest-cov / coverage.py | — (dev-only) |
| Linting | flake8, isort, black | via `.pre-commit-config.yaml` (dev-only, via `pre-commit`) |
| Container | Docker + docker-compose | — |
| Reverse proxy | Caddy | 2.0.0 |

> **Note:** `django-mathfilters` is listed in `Pipfile` for template arithmetic filters but is **not** registered in `INSTALLED_APPS` (confirmed by a comment in `settings.py`: *"mathfilters" is optional in some environments... if it's not installed, we can still run the app's core tests*). `django-bootstrap4` is **not present** in `Pipfile` at all in the current codebase — `INSTALLED_APPS` has a commented-out `# "bootstrap4",` line with the note *"bootstrap4 is only needed for template tag libraries (used in base.html)"*, but `base.html` no longer loads `{% load bootstrap4 %}` (see Section 11).

---

## 7. Architecture Overview

ihatetobudget follows a standard Django MTV (Model-Template-View) pattern.

```
Browser
  │
  ▼
Caddy (reverse proxy, port 80, image caddy:2.0.0)
  │
  ▼
Daphne ASGI Server
  (pipenv run daphne -b 0.0.0.0 ihatetobudget.asgi:application)
  preceded by: pipenv run python manage.py collectstatic --noinput
  │
  ├── Root URLconf  (ihatetobudget/urls.py)
  │       ├── "" → ihatetobudget.views.index
  │       │       (redirects to sheets:index if authenticated,
  │       │        else renders ihatetobudget/index.html landing page)
  │       ├── "sheets/" → include("sheets.urls")
  │       ├── "admin/" → admin.site.urls
  │       ├── "accounts/" → django.contrib.auth.urls
  │       └── "budget/", "budget/<year>/<month>/" → sheets.views.budget_dashboard
  │             (also registered, redundantly, inside sheets/urls.py
  │              under /sheets/budget/)
  │
  ├── Views (sheets/views.py)
  │       ├── Function-based: register_view, export_csv_view, index,
  │       │     receipts_month_view, receipts_month_download_view,
  │       │     receipt_download_view, budget_dashboard
  │       └── Class-based: SheetView, Expense{Create,Update,Delete}View,
  │                        Category{List,Create,Update,Delete}View, ExpenseListView
  │
  ├── Models (sheets/models.py)
  │       └── Category ← Expense → User (Django auth)
  │                         BudgetLimit → User, Category
  │
  └── Templates (ihatetobudget/template/ + sheets/template/)
          └── base.html (Bootstrap 5 CDN JS + dark-mode anti-flash inline script)
```

Authentication is handled entirely by Django's built-in `django.contrib.auth`. All application views except `register_view` and the project-level `index` require login (`@login_required` / `LoginRequiredMixin`).

**Settings note:** `ihatetobudget/settings.py` defines `WSGI_APPLICATION = "ihatetobudget.wsgi.application"` even though the Docker deployment actually runs Daphne (ASGI). Both `wsgi.py` and `asgi.py` exist in the project; the `WSGI_APPLICATION` setting is effectively unused in the containerised deployment path but does not cause any conflict, since Django keeps the two independent.

> **Note:** `budget_dashboard` URLs are registered in *two* places — once in `ihatetobudget/urls.py` (project root, e.g. `/budget/`) and once in `sheets/urls.py` (app-scoped, `/sheets/budget/`). Both resolve to the same view function. The navbar links to the `sheets:budget_dashboard` name (i.e. the `/sheets/budget/` path).

---

## 8. Data Models

### 8.0 UML Class Diagram

```
User (django.contrib.auth)
  id, username, password, email
       │ 1
       │ owns
       ├──────────────────┐
       │ *                │ *
   Expense             BudgetLimit
   id (PK)             id (PK)
   user FK→User        user FK→User (CASCADE)
     (null, blank, CASCADE)   category FK→Category (CASCADE)
   category FK→Category       limit_amount (Decimal)
     (null, blank, SET_NULL)  month (Integer)
   date (DateField)           year (Integer)
   description (Char)
   amount (Decimal)           unique_together:
   receipt (File,             (user, category, month, year)
     null, blank)
   repeat_next_month (Bool)
       │ *                       │ *
       │ belongs to              │ applies to
       └──────────┬───────────────┘
                  │ *
              Category
              id (PK)
              name (Char)
              color (ColorField, default "#FFFFFF")
```

**Relationship summary:**

- A `User` may own many `Expense` and many `BudgetLimit` records. On `Expense`, `user` is `on_delete=CASCADE`. On `BudgetLimit`, `user` is also `on_delete=CASCADE`.
- An `Expense` belongs to one `Category` (nullable; `on_delete=SET_NULL`, so deleting a category does not delete its expenses).
- A `BudgetLimit` links one `User` to one `Category` for a specific `month`/`year`; the combination `(user, category, month, year)` is enforced unique via `Meta.unique_together`, with `on_delete=CASCADE` for both `user` and `category`.

### 8.1 `Category`

| Field | Type | Notes |
|---|---|---|
| `id` | BigAutoField (PK) | Implicit, via `DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"` |
| `name` | CharField(200) | Display label |
| `color` | ColorField | Default `#FFFFFF` |

`get_absolute_url()` → `reverse("sheets:categories")`

### 8.2 `Expense`

| Field | Type | Notes |
|---|---|---|
| `id` | BigAutoField (PK) | — |
| `user` | FK → User | `null=True, blank=True`; `on_delete=CASCADE` |
| `category` | FK → Category | `null=True, blank=True`; `on_delete=SET_NULL` |
| `date` | DateField | Defaults to `date.today` |
| `description` | CharField(200) | Free-text label |
| `amount` | DecimalField(8,2) | `MinValueValidator(Decimal("0.01"))` |
| `receipt` | FileField | `upload_to="receipts/%Y/%m/"`; `blank=True, null=True` |
| `repeat_next_month` | BooleanField | `default=False`; when `True`, `cron.py` clones the expense one month forward |

`get_absolute_url()` → `reverse("sheets:sheet", kwargs={"year": self.date.year, "month": self.date.month})`

### 8.3 `BudgetLimit`

| Field | Type | Notes |
|---|---|---|
| `id` | BigAutoField (PK) | — |
| `user` | FK → User | `on_delete=CASCADE` |
| `category` | FK → Category | `on_delete=CASCADE` |
| `limit_amount` | DecimalField(10,2) | Monthly spend ceiling |
| `month` | IntegerField | **No range validation** at the model or form level — `month=0` and `month=13` are both accepted (confirmed by `test_budgetlimit_form_accepts_edge_month_values_as_int`) |
| `year` | IntegerField | 4-digit year, no validation |

`Meta.unique_together = ("user", "category", "month", "year")`

---

## 9. Views & URL Routing

### 9.1 URL Table

All `sheets:` names are mounted under the `/sheets/` prefix (e.g. `/sheets/register/`), per `ihatetobudget/urls.py`.

| URL Pattern | View | Name | Auth |
|---|---|---|---|
| `/` | `ihatetobudget.views.index` | `index` | Public; redirects authenticated users |
| `/sheets/` (app root) | `sheets.views.index` | `sheets:index` | ✅ |
| `/sheets/register/` | `register_view` | `sheets:register` | ❌ |
| `/sheets/export/csv/` | `export_csv_view` | `sheets:export_csv` | ✅ |
| `/sheets/budget/` | `budget_dashboard` | `sheets:budget_dashboard` | ✅ |
| `/sheets/budget/<year>/<month>/` | `budget_dashboard` | `sheets:budget_dashboard_monthly` | ✅ |
| `/budget/` | `budget_dashboard` | `budget_dashboard` (root-level) | ✅ |
| `/budget/<year>/<month>/` | `budget_dashboard` | `budget_dashboard_monthly` (root-level) | ✅ |
| `/sheets/<year>/<month>/` | `SheetView` | `sheets:sheet` | ✅ |
| `/sheets/receipts/month/<year>/<month>/` | `receipts_month_view` | `sheets:receipts_month_view` | ✅ |
| `/sheets/receipts/month/<year>/<month>/download/` | `receipts_month_download_view` | `sheets:receipts_month_download` | ✅ (queryset-scoped, no `@login_required` decorator on the function itself) |
| `/sheets/receipts/download/<pk>/` | `receipt_download_view` | `sheets:receipt_download` | ✅ |
| `/sheets/expense/new/` | `ExpenseCreateView` | `sheets:expense-new` | ✅ |
| `/sheets/expense/<pk>/` | `ExpenseUpdateView` | `sheets:expense-edit` | ✅ |
| `/sheets/expense/<pk>/delete/` | `ExpenseDeleteView` | `sheets:expense-delete` | ✅ |
| `/sheets/expense/history/` | `ExpenseListView` | `sheets:history` | ✅ |
| `/sheets/categories/` | `CategoryListView` | `sheets:categories` | ✅ |
| `/sheets/category/new/` | `CategoryCreateView` | `sheets:category-new` | ✅ |
| `/sheets/category/<pk>/` | `CategoryUpdateView` | `sheets:category-edit` | ✅ |
| `/sheets/category/<pk>/delete/` | `CategoryDeleteView` | `sheets:category-delete` | ✅ |

### 9.2 View Descriptions

**`ihatetobudget.views.index`** — Public-facing root. Redirects to `sheets:index` if `request.user.is_authenticated`, otherwise renders `ihatetobudget/index.html` (the public landing page) with `title="Home"`.

**`sheets.views.index`** — `@login_required`. Renders the overview dashboard. Computes:
- `monthly_average_spend` — the average of total spend across all complete months strictly before the current calendar month, across **all expenses** (not filtered to `request.user` — see Section 18).
- `median_spend` — the median of **all** individual expense amounts across **all users** (also not filtered to `request.user`).
- `monthly_insights_dict` — per-category monthly totals keyed by `year → category → [12 monthly sums]`, built by iterating every year that has at least one expense (across all users) and every registered `Category`, plus an implicit `None` category bucket for uncategorised expenses.
- Currency display context variables (`currency_group_separator`, `currency_decimal_separator`, `currency_prefix`, `currency_suffix`) sourced from `settings.CURRENCY_*`.

**`register_view`** — Public endpoint. Builds `CustomUserCreationForm` from `request.POST` (or unbound on GET). On valid POST, saves the user, calls `login(request, user)`, then renders `sheets/index.html` directly (a `render()`, not a `redirect()` — the URL bar stays at `/sheets/register/`). On GET or invalid POST, renders `registration/register.html`.

**`export_csv_view`** — `@login_required`. Streams a `text/csv` attachment (`expenses.csv`) of `Expense.objects.filter(user=request.user).order_by("date")`. Columns: `Date`, `Category`, `Amount`, `Description`.

**`budget_dashboard(request, year=None, month=None)`** — `@login_required`. Defaults `year`/`month` to today's values when not supplied via URL kwargs. Filters `BudgetLimit` to `(user=request.user, year, month)`, computes `spent_amount` per category in one aggregated query, then for each budget row computes `remaining_amount = limit_amount - spent_amount` and `percent_used = (spent_amount / limit_amount) * 100` (`None` if `limit_amount` is zero/falsy), quantized to one decimal place when not `None`.

**`SheetView`** — `LoginRequiredMixin` + `MonthArchiveView` subclass. Overrides `get_queryset()` to filter `Expense.objects.all()` down to `qs.filter(user=self.request.user)`. Injects `days_left` into context only when the requested month/year matches the current calendar month.

**`ExpenseListView`** — Paginated at 50 items; supports free-text search via `?q=` across `date`, `category__name`, `amount`, and `description` (all via `icontains`), combined with `Q` OR-logic. Uses `SortableListViewMixin` (`sortable_fields = ["date", "category", "amount"]`). **Note:** unlike `SheetView`, this view does not explicitly scope its base queryset to `request.user` in the view code itself.

**`receipts_month_view(request, year, month)`** — `@login_required`. Filters the user's expenses for the given month and collects those with a non-empty `receipt` field; renders `sheets/receipts_month.html` with the receipt list and count (shows an empty state if none).

**`receipts_month_download_view(request, year, month)`** — Not decorated with `@login_required` directly, but filters by `request.user`. Returns a single `FileResponse` if exactly one receipt exists for the month, otherwise streams a ZIP archive (`receipts_<year>_<month>.zip`) of all receipts for that month. Raises `Http404` if no receipts exist.

**`receipt_download_view(request, pk)`** — `@login_required`. Looks up a single `Expense` by `pk` scoped to `request.user`; returns `Http404` if not found or has no receipt, otherwise streams the file as an attachment.

---

## 10. Forms

| Form | Model | Key behaviour |
|---|---|---|
| `ExpenseForm` | `Expense` | `fields = "__all__"`; `required_css_class = "form-group-required"` |
| `CategoryForm` | `Category` | `fields = "__all__"`; `required_css_class = "form-group-required"` |
| `BudgetLimitForm` | `BudgetLimit` | `fields = ["category", "limit_amount", "month", "year"]`; no range validation on `month` |
| `CustomUserCreationForm` | `User` (Django) | Extends `UserCreationForm`; adds an optional `email` field (`required=False`); `Meta.fields = ("username", "email")` — `password1`/`password2` are inherited automatically from `UserCreationForm` |

---

## 11. Template System, Bootstrap 5 Migration & Dark Mode

### 11.1 Template Inheritance

```
ihatetobudget/template/ihatetobudget/common/base.html
  └── (includes navbar.html; provides {% block title %} and {% block body %})
        ├── sheets/template/sheets/index.html
        ├── sheets/template/sheets/sheet.html
        ├── sheets/template/sheets/history.html
        ├── sheets/template/sheets/categories.html
        ├── sheets/template/sheets/budget.html
        └── sheets/template/sheets/receipts_month.html
```

`sheets/template/sheets/common/base.html` and `sidebar.html` also exist as app-level layout helpers used by the sheet/budget/history pages.

### 11.2 Bootstrap 4 → Bootstrap 5 Migration (Enhancement #4)

**This is a significant, verified change from earlier versions of this codebase.** The application has been migrated to Bootstrap 5:

- `static/bootstrap.min.css` is now **Bootswatch Litera v5.3.8**, built on **Bootstrap v5.3.8**, confirmed by the file's own header comment (`Bootswatch v5.3.8`, `Bootstrap v5.3.8`).
- `base.html` no longer loads `{% load bootstrap4 %}` — only `{% load static %}`.
- The Bootstrap JS bundle is loaded from CDN as `bootstrap@5.3.7` (`cdn.jsdelivr.net/npm/bootstrap@5.3.7/dist/js/bootstrap.bundle.min.js`) — a minor version behind the CSS (5.3.8) but within the same 5.3.x line and fully compatible.
- Templates use Bootstrap 5 attribute conventions: `data-bs-toggle="collapse"`, `data-bs-target`, `data-bs-dismiss="alert"`, `me-auto`, `me-3`, `ms-1` (in `navbar.html` and `base.html`).
- `INSTALLED_APPS` in `settings.py` has the `bootstrap4` app **commented out** with the note: *"bootstrap4 is only needed for template tag libraries (used in base.html)"* — but `base.html` itself no longer uses any `bootstrap4` template tags, so this commented-out line is now historical/inert.
- `Pipfile` does **not** list `django-bootstrap4` as a dependency in the current codebase.
- The original Bootstrap 4 stylesheet has been **preserved, not deleted**, at `static/bootstrap4-backup.css` and `static/bootstrap4-backup.min.css`. Neither file is referenced by any template — they exist purely as a rollback/reference copy.
- One legacy artifact remains in `navbar.html`: the badge class `badge-pill` is Bootstrap 4 syntax (Bootstrap 5 renamed this utility to `rounded-pill`). This does not break rendering — `badge-pill` is simply an unstyled, unused class name under Bootstrap 5 — but it is a leftover from the pre-migration markup that was not fully cleaned up.

### 11.3 Dark Mode Implementation (Enhancement #4)

Dark mode is implemented entirely client-side using a `data-theme` attribute on `<html>`, a dedicated `localStorage` key, and CSS rules scoped under `[data-theme="dark"]` in `static/styles.css`. There is **no server-side state** for theme preference. This mechanism is independent of Bootstrap 5's own built-in `data-bs-theme` dark mode support — the two are not connected.

**Anti-flash script (in `<head>` of `base.html`), runs before any CSS loads:**

```html
<script>
  (function() {
    var theme = localStorage.getItem('ihtb-theme');
    if (theme === 'dark') {
      document.documentElement.setAttribute('data-theme', 'dark');
    }
  })();
</script>
```

**Toggle logic (inline `<script>` near the end of `base.html`, after the Bootstrap 5 JS bundle):**

```javascript
(function () {
  var STORAGE_KEY = 'ihtb-theme';

  function getTheme() {
    return localStorage.getItem(STORAGE_KEY) || 'light';
  }

  function applyTheme(theme) {
    if (theme === 'dark') {
      document.documentElement.setAttribute('data-theme', 'dark');
    } else {
      document.documentElement.removeAttribute('data-theme');
    }
    document.querySelectorAll('.dark-mode-toggle').forEach(function(btn) {
      btn.setAttribute('title', theme === 'dark' ? 'Switch to Light Mode' : 'Switch to Dark Mode');
      btn.querySelector('i').className = theme === 'dark' ? 'fa fa-sun-o' : 'fa fa-moon-o';
    });
  }

  function toggleTheme() {
    var current = getTheme();
    var next = current === 'dark' ? 'light' : 'dark';
    localStorage.setItem(STORAGE_KEY, next);
    applyTheme(next);
  }

  document.querySelectorAll('.dark-mode-toggle').forEach(function(btn) {
    btn.addEventListener('click', toggleTheme);
  });
  applyTheme(getTheme());
})();
```

**Toggle button markup (`navbar.html`):**

```html
<button class="dark-mode-toggle" id="darkModeToggle" title="Switch to Dark Mode" aria-label="Toggle dark mode">
  <i class="fa fa-moon-o"></i>
</button>
```

The button uses Font Awesome moon/sun icons (`fa-moon-o` / `fa-sun-o`), swapped by the toggle script.

**CSS rules (`static/styles.css`, under a clearly marked "Dark Mode (Enhancement #4 - Farah Hanim)" comment block, ~53 selector occurrences):**

CSS variables and overrides are defined inside `[data-theme="dark"] { ... }` and component-scoped selectors (e.g. `[data-theme="dark"] .navbar`, `[data-theme="dark"] .card`, `[data-theme="dark"] .form-control`, `[data-theme="dark"] .table`, `[data-theme="dark"] .dropdown-menu`, `[data-theme="dark"] .alert-info/.alert-success/.alert-danger`, `[data-theme="dark"] .badge-info`, `[data-theme="dark"] .progress`, `[data-theme="dark"] .jumbotron`, `[data-theme="dark"] .list-group-item`, `[data-theme="dark"] .btn-secondary`, and the `.dark-mode-toggle` button itself).

> **Important:** the dark-mode CSS variables are scoped *inside* `[data-theme="dark"]` (not on `:root`), meaning light mode relies entirely on Bootstrap 5's own default colour scheme with no custom override variables defined for the light theme.

---

## 12. Testing Infrastructure

### 12.1 Test Layout

```
ihatetobudget/tests/
  test_templatetags.py         # Tests for ihatetobudget_extras template tags (8 tests)
  test_views.py                # Project-level auth/redirect smoke test (1 test)
  utils/test_views.py          # View mixin unit tests (3 tests)

sheets/tests/
  test_models.py               # pytest: Category, Expense, BudgetLimit model behaviour (4 tests)
  test_forms.py                # pytest: form validation tests (7 tests)
  test_views.py                # pytest: views — CSV parsing, registration, zero-division guard, etc. (10 tests)
  test_views_comprehensive.py  # Django TestCase: 12 classes, 55 tests — main view suite
  test_views_extra.py          # 4 pytest tests — duplicates a subset of test_views.py (see 12.7)
  test_receipts_views.py       # Django TestCase: receipt view/download endpoints (1 class, 7 tests)
```

### 12.2 Running Tests

```bash
# Run all tests with coverage report (enforces fail_under = 91 from .coveragerc)
pipenv run pytest --cov=. --cov-report=term-missing

# Run only the main comprehensive suite
pipenv run pytest sheets/tests/test_views_comprehensive.py -v

# Generate HTML coverage report
pipenv run pytest --cov=. --cov-report=html
# Open htmlcov/index.html in browser
```

### 12.3 Coverage Configuration (`.coveragerc`)

```ini
[run]
source = sheets
omit =
    */migrations/*
    */tests/*
    */test_*.py
    */__init__.py
    sheets/cron.py
    manage.py
    ihatetobudget/asgi.py
    ihatetobudget/wsgi.py

[report]
show_missing = True
fail_under = 91
```

Coverage is scoped to the `sheets` package only (`source = sheets`); the `ihatetobudget` project package's tests run but are not counted toward the coverage gate. `fail_under = 91` causes `coverage report` to exit non-zero if total coverage on `sheets` drops below 91%.

> **Note:** the repository contains a committed `.coverage` binary data file in its root. This is a stray build artifact from a prior local test run rather than a tracked source file — see Section 18.

### 12.4 Test Classes (`test_views_comprehensive.py`)

| Test Class | View(s) Covered | Test Methods |
|---|---|---|
| `IndexViewTestCase` | `index` | 9 |
| `ExpenseCreateViewTestCase` | `ExpenseCreateView` | 4 |
| `ExpenseUpdateViewTestCase` | `ExpenseUpdateView` | 2 |
| `ExpenseDeleteViewTestCase` | `ExpenseDeleteView` | 6 |
| `ExpenseListViewTestCase` | `ExpenseListView` | 4 |
| `CategoryListViewTestCase` | `CategoryListView` | 3 |
| `CategoryCreateViewTestCase` | `CategoryCreateView` | 3 |
| `CategoryUpdateViewTestCase` | `CategoryUpdateView` | 2 |
| `CategoryDeleteViewTestCase` | `CategoryDeleteView` | 3 |
| `ExportCSVViewTestCase` | `export_csv_view` | 6 |
| `BudgetDashboardTestCase` | `budget_dashboard` | 7 |
| `RegisterViewTestCase` | `register_view` | 6 |

**Total: 12 classes, 55 test methods.**

### 12.5 Supplementary Test Files

| File | Framework | Test Count | Purpose |
|---|---|---|---|
| `test_views.py` | pytest | 10 | CSV row-by-row parsing, registration flow, zero-division guard on `budget_dashboard`, plus 4 tests duplicated in `test_views_extra.py` |
| `test_views_extra.py` | pytest | 4 | Identical duplicates of 4 tests already present in `test_views.py` — see Section 12.7 |
| `test_receipts_views.py` | Django `TestCase` | 7 | Receipt viewing, single-file download, bulk ZIP/single-file download, 404 handling for missing receipts |
| `test_models.py` | pytest | 4 | `Category`/`Expense` string & URL behaviour; `BudgetLimit` uniqueness constraint |
| `test_forms.py` | pytest | 7 | `CustomUserCreationForm` and `BudgetLimitForm` validation paths |

### 12.6 Notable Design Decisions in the Test Suite

- `test_sheet_view_days_left_condition_matches_today` does **not** render `sheet.html` through the test client, because the template depends on `django-mathfilters` template tags that are not registered in `INSTALLED_APPS`. It instead re-implements the relevant `days_left` branch inline as a standalone function and asserts on its output.
- `ExportCSVViewTestCase.test_csv_only_contains_current_user_data` (and pytest counterpart `test_export_csv_view_returns_csv_for_user_expenses`) verify that `export_csv_view` correctly scopes its queryset to `request.user`.
- `BudgetDashboardTestCase.test_budget_status_reflects_partial_spending` asserts `percent_used == Decimal("40.0")` for a 200/500 spend ratio, exercising the `Decimal`-based percentage calculation and its `.quantize(Decimal("0.1"))` rounding.
- `test_budget_dashboard_defensive_zero_division_when_limit_is_zero` confirms that when `BudgetLimit.limit_amount == 0`, `percent_used` is explicitly `None` rather than raising a division error.

### 12.7 Test Duplication Finding

`sheets/tests/test_views_extra.py`'s 4 tests (`test_index_renders_monthly_average_and_median_branches`, `test_sheet_view_days_left_condition_matches_today`, `test_expense_list_queryset_search_q`, `test_budget_dashboard_percent_used_quantize_branch_non_zero_limit`) are **byte-for-byte identical** to 4 of the 10 tests in `test_views.py`. Both files are independently discovered and executed by pytest, so these 4 assertions currently run twice per test invocation. This does not affect correctness but is a maintenance item: `test_views_extra.py` contributes no coverage beyond what `test_views.py` already provides and could be retired.

---

## 13. Enhancement Details

---

### 13.1 Enhancement #1 — Preventive & Corrective Maintenance: Environment & Security
**Assignee:** Mohammed Aamena Mohammed Abdulkarem  
**ISO/IEC 14764 Type:** Preventive + Corrective

#### Changes Made

**`Pipfile`** — Django pinned to `==4.2.11`; other dependencies left unpinned (`"*"`).

**`ihatetobudget/settings.py`**

```python
IS_TEST = (os.environ.get("PYTEST_CURRENT_TEST") is not None) or ("test" in sys.argv[0])

SECURE_HSTS_SECONDS = int(os.environ.get("DJANGO_SECURE_HSTS_SECONDS", "31536000"))

SECURE_SSL_REDIRECT = (
    os.environ.get("DJANGO_SECURE_SSL_REDIRECT", "False") == "True"
) and (not IS_TEST)

SESSION_COOKIE_SECURE = os.environ.get("DJANGO_SESSION_COOKIE_SECURE", "True") == "True"
CSRF_COOKIE_SECURE = os.environ.get("DJANGO_CSRF_COOKIE_SECURE", "True") == "True"
SECURE_HSTS_INCLUDE_SUBDOMAINS = os.environ.get("DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", "True") == "True"
SECURE_HSTS_PRELOAD = os.environ.get("DJANGO_SECURE_HSTS_PRELOAD", "True") == "True"
```

All environment-variable driven, defaulting to secure values in production while being safely disabled (`SECURE_SSL_REDIRECT`) during local development and tests. `docker-compose.yml` explicitly overrides `DJANGO_SECURE_SSL_REDIRECT=False` since Caddy is currently HTTP-only (port 80).

#### Verification

```bash
pipenv run python manage.py check --deploy
```

---

### 13.2 Enhancement #2 — Adaptive Enhancements: Models & Database
**Assignee:** Mohammed Yousef Mohammed Abdulkarem  
**ISO/IEC 14764 Type:** Adaptive

#### Changes Made

- `BudgetLimit` model and the `receipt`/`user` fields on `Expense` (see Section 8).
- `sheets/migrations/0008_expense_receipt_expense_user_alter_category_id_and_more.py` — combined migration adding the `receipt` field, the `user` FK, promoting PKs to `BigAutoField`, and creating `BudgetLimit`.
- `BudgetLimitForm` (fields: `category`, `limit_amount`, `month`, `year`); `ExpenseForm` picks up `receipt` automatically via `fields = "__all__"`.
- `export_csv_view`, `receipts_month_view`, `receipts_month_download_view`, `receipt_download_view` in `sheets/views.py`.
- `MEDIA_URL = "/media/"`, `MEDIA_ROOT = BASE_DIR / "media"` in `settings.py`; `ihatetobudget/urls.py` serves media via Django's static helper when `DEBUG=True`.

#### Database Migration Commands

```bash
pipenv run python manage.py makemigrations
pipenv run python manage.py migrate
```

---

### 13.3 Enhancement #3 — Adaptive Enhancements: Views & Authentication
**Assignee:** Mohammed Aamena Mohammed Abdulkarem  
**ISO/IEC 14764 Type:** Adaptive

#### Changes Made

**User Registration (`sheets/views.py`, `sheets/forms.py`)**

```python
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=False)
    class Meta:
        model = User
        fields = ("username", "email")

def register_view(request):
    form = CustomUserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        return render(request, "sheets/index.html")
    return render(request, "registration/register.html", {"form": form})
```

> **Implementation note:** on success, the view directly `render()`s `sheets/index.html` rather than redirecting to `sheets:index`. The URL bar stays at `/sheets/register/` after a successful registration even though the dashboard is rendered. `test_valid_registration_logs_user_in` confirms the session is authenticated regardless.

- `budget_dashboard` — see Section 9.2 for the `Decimal`-safe `percent_used` calculation with a zero-limit guard.
- `export_csv_view` filters `Expense.objects.filter(user=request.user)`.
- `SheetView.get_queryset()` filters `qs.filter(user=self.request.user)`.

**Monthly spend calculation**, implemented in the `index` view: `monthly_average_spend`, `median_spend`, `monthly_insights_dict` (see Section 9.2 for exact scoping behaviour).

---

### 13.4 Enhancement #4 — UI/UX Enhancements: Bootstrap 5 & Dark Mode
**Assignee:** Farah Hanim binti Mohd Zamri  
**ISO/IEC 14764 Type:** Perfective

See **Section 11** for the full implementation of the Bootstrap 5 migration and the dark mode mechanism.

**Summary of files changed:**

| File | Change |
|---|---|
| `static/bootstrap.min.css` | Replaced with Bootswatch Litera v5.3.8 (was Bootstrap 4) |
| `static/bootstrap4-backup.css`, `static/bootstrap4-backup.min.css` | New — retained copies of the pre-migration Bootstrap 4 stylesheet |
| `ihatetobudget/template/ihatetobudget/common/base.html` | Dropped `{% load bootstrap4 %}`; added Bootstrap 5 CDN JS bundle; anti-flash inline script in `<head>`; theme-toggle logic script before `</body>` |
| `ihatetobudget/template/ihatetobudget/common/navbar.html` | Converted to Bootstrap 5 attributes (`data-bs-toggle`, `me-auto`, etc.); `.dark-mode-toggle` button with Font Awesome moon/sun icon |
| `static/styles.css` | `[data-theme="dark"]` variable block and component-level dark-mode overrides |

---

### 13.5 Enhancement #5 — Perfective Maintenance: Testing & Quality
**Assignee:** Farah Hanim binti Mohd Zamri
**ISO/IEC 14764 Type:** Perfective

See **Section 12** for the full test class catalogue, exact test counts, and coverage configuration.

**Summary of files added:**

| File | Contents |
|---|---|
| `sheets/tests/test_views_comprehensive.py` | 12 test classes, 55 test methods |
| `sheets/tests/test_views.py` | 10 pytest tests |
| `sheets/tests/test_views_extra.py` | 4 pytest tests (duplicate subset of `test_views.py`) |
| `sheets/tests/test_receipts_views.py` | 7 Django `TestCase` tests for receipt endpoints |
| `sheets/tests/test_models.py` | 4 model tests |
| `sheets/tests/test_forms.py` | 7 form validation tests |
| `.coveragerc` | `source = sheets`; relevant omissions; `fail_under = 91` |
| `.pre-commit-config.yaml` | isort, black, flake8 hooks |

**Testing Summary**: The final automated test suite consists of 99 discovered tests, of which 95 passed and 4 were skipped (pre-existing placeholder tests marked with @not_implemented). No test failures were recorded. The suite achieved 91% code coverage, meeting the configured fail_under = 91 quality threshold.

---

### 13.6 Enhancement #6 — Docker & Deployment Configuration
**Assignee:** Mohammed Yousef Mohammed Abdulkarem  
**ISO/IEC 14764 Type:** Adaptive

#### Stack Overview

```
docker-compose.yml
  ├── Service: ihatetobudget
  │     Build:   . (Dockerfile)
  │     Command: sh -c "pipenv run python manage.py collectstatic --noinput &&
  │                      pipenv run daphne -b 0.0.0.0 ihatetobudget.asgi:application"
  │     env_file: docker-compose.env
  │     Environment override: DJANGO_SECURE_SSL_REDIRECT=False
  │     Volumes: .  → /usr/src/app
  │              static → /static
  │              media_volume → /usr/src/app/media
  │
  └── Service: caddy
        Image:   caddy:2.0.0
        Port:    80:80
        Volumes: ./Caddyfile → /etc/caddy/Caddyfile
                 caddy_data → /data
                 static → /var/www/static
        depends_on: ihatetobudget

volumes: caddy_data, static, media_volume
```

#### Dockerfile

```dockerfile
FROM python:3.10

ENV PYTHONUNBUFFERED=1
ENV DJANGO_SECRET_KEY=change-me

WORKDIR /usr/src/app
COPY . .

RUN apt-get update && apt-get -y install cron rustc

RUN pip install pipenv
RUN pipenv install --deploy --ignore-pipfile

RUN pipenv run python manage.py collectstatic --noinput
RUN pipenv run python manage.py crontab add
```

> `cron` supports `sheets/cron.py`'s monthly recurring-expense job (`CRONJOBS` in `settings.py`, runs at `5 0 1 * *`). `rustc` is required to build the `cryptography` package used transitively by Django.

#### Environment Configuration

Copy `docker-compose.env.example` to `docker-compose.env` and set at minimum `DJANGO_SECRET_KEY` and `DJANGO_ALLOWED_HOSTS`.

#### Quick-Start

```bash
cp docker-compose.env.example docker-compose.env
docker-compose up --build -d
docker-compose exec ihatetobudget pipenv run python manage.py migrate
docker-compose exec ihatetobudget pipenv run python manage.py createsuperuser
```

> **Note:** the service name in `docker-compose.yml` is `ihatetobudget`, not `web` — commands referencing `docker compose exec web ...` (as seen in the project's README) will fail against this `docker-compose.yml`; use `ihatetobudget` as the service name instead.

---

## 14. Development Workflow

```
1. Pick up an issue from the issue tracker
         │
         ▼
2. Create a feature branch from main
   git checkout -b feature/ENH-004-bootstrap5-darkmode
         │
         ▼
3. Implement the enhancement or bug fix
   - Write or update code
   - Add/update tests in sheets/tests/
         │
         ▼
4. Run the automated test suite locally
   pipenv run pytest --cov=. --cov-report=term-missing
   (must pass with coverage ≥ 91%, per .coveragerc fail_under)
         │
         ▼
5. Run linters / pre-commit hooks
   pipenv run pre-commit run --all-files
         │
         ▼
6. Submit a Pull Request / Merge Request
   - Use the templates in .github/ISSUE_TEMPLATE/ and .github/PULL_REQUEST_TEMPLATE.md
         │
         ▼
7. Peer review by at least one other Group 4 member
         │
         ▼
8. Merge into main branch after approval
```

**Branch naming convention:**

| Type | Pattern | Example |
|---|---|---|
| Enhancement | `feature/ENH-<n>-<slug>` | `feature/ENH-004-bootstrap5-darkmode` |
| Bug fix | `fix/BUG-<n>-<slug>` | `fix/BUG-001-csv-user-filter` |
| Dependency update | `chore/update-<package>` | `chore/update-django-4.2` |

---

## 15. Environment Setup (Local Development)

### Prerequisites

- Python 3.10
- Pipenv (`pip install pipenv`)
- Git
- `rustc` if installing dependencies from scratch (required transitively by `cryptography`)

### Steps

```bash
# 1. Clone the repository
git clone <repo-url>
cd ihatetobudget

# 2. Install dependencies
pipenv install --dev

# 3. Set required environment variable
export DJANGO_SECRET_KEY="your-local-dev-secret-key"

# 4. Apply migrations
pipenv run python manage.py migrate

# 5. Create a superuser (optional)
pipenv run python manage.py createsuperuser

# 6. Seed sample data (optional)
pipenv run python dev/generate_test_data.py

# 7. Start the development server
pipenv run python manage.py runserver
```

Open `http://127.0.0.1:8000/` in your browser.

> **Note:** `DJANGO_SECRET_KEY` is mandatory — `settings.py` raises `RuntimeError("Missing required environment variable: DJANGO_SECRET_KEY")` at startup if it is absent. There is no `.env.example` file in this codebase (despite the README referencing one) — the actual example file is `docker-compose.env.example`.

---

## 16. Docker Setup

```bash
cp docker-compose.env.example docker-compose.env
# Edit docker-compose.env: set DJANGO_SECRET_KEY at minimum

docker-compose up --build

docker-compose exec ihatetobudget pipenv run python manage.py migrate
```

`Caddyfile.example` is provided as a starting point; copy it to `Caddyfile` and adjust as needed (the committed `Caddyfile` in this repo is configured for local/demo use on port 80, HTTP-only).

---

## 17. Configuration Reference

All configuration is in `ihatetobudget/settings.py` and driven by environment variables.

| Variable | Required | Default | Description |
|---|---|---|---|
| `DJANGO_SECRET_KEY` | ✅ | — | Django secret key; raises `RuntimeError` if absent |
| `DJANGO_DEBUG` | ❌ | `"True"` | Set to `"False"` to disable debug mode |
| `DJANGO_ALLOWED_HOSTS` | ❌ | `"127.0.0.1,localhost"` | Comma-separated hostnames |
| `DJANGO_SECURE_SSL_REDIRECT` | ❌ | `"False"` | Forces HTTPS redirect; automatically disabled during tests via `IS_TEST` |
| `DJANGO_SESSION_COOKIE_SECURE` | ❌ | `"True"` | Session cookie HTTPS-only flag |
| `DJANGO_CSRF_COOKIE_SECURE` | ❌ | `"True"` | CSRF cookie HTTPS-only flag |
| `DJANGO_SECURE_HSTS_SECONDS` | ❌ | `"31536000"` | HSTS max-age |
| `DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS` | ❌ | `"True"` | HSTS subdomain flag |
| `DJANGO_SECURE_HSTS_PRELOAD` | ❌ | `"True"` | HSTS preload flag |
| `CURRENCY_GROUP_SEPARATOR` | ❌ | `","` | Thousands separator |
| `CURRENCY_DECIMAL_SEPARATOR` | ❌ | `"."` | Decimal separator |
| `CURRENCY_PREFIX` | ❌ | `"RM "` | Prepended to amounts (default is Malaysian Ringgit) |
| `CURRENCY_SUFFIX` | ❌ | `""` | Appended to amounts |

---

## 18. Known Issues, Quirks & Loose Ends

These are observations made directly from the source, not assumptions:

| ID | Area | Description |
|---|---|---|
| OBS-001 | `sheets.views.index` | `monthly_average_spend` and `median_spend` are computed across **all expenses in the database**, not scoped to `request.user`. In a multi-tenant deployment, one user's overview dashboard reflects every user's spending. This differs from `SheetView` and `export_csv_view`, which are correctly user-scoped. |
| OBS-002 | `ExpenseListView` | Unlike `SheetView`, the History page's `get_queryset()` does not filter by `request.user`, so search results could include other users' expenses depending on deployment usage patterns. |
| OBS-003 | `register_view` | Renders `sheets/index.html` directly via `render()` instead of issuing a redirect to `sheets:index` after successful registration. The URL bar remains at `/sheets/register/`. |
| OBS-004 | URL routing | `budget_dashboard` is registered at both `/budget/` (project root) and `/sheets/budget/` (app-scoped) — duplicate routes resolving to the same view. |
| OBS-005 | `static/bootstrap4-backup.min.css` | Present on disk but not referenced by any template — a pure backup artifact from the Bootstrap 5 migration. |
| OBS-006 | `sheets/models_budgetlimit_stub.txt` | A one-line placeholder file (content: `stub`) not imported or referenced anywhere in the codebase. Appears to be leftover scaffolding from development. |
| OBS-007 | `TEMPLATE_DEBUG_register.txt` | A scratch file containing shell commands used to debug template resolution for `register_view`; not part of the application itself. |
| OBS-008 | `launch-instructions.txt` | A scratch file with quick Docker launch notes; informational only, duplicates content already in Section 16 of this document. |
| OBS-009 | `.coverage`, `db.sqlite3` | Both files are committed to the repository root. `.coverage` is a binary coverage-run artifact and `db.sqlite3` is a live SQLite database — neither should typically be version-controlled, but both are present in the submitted zip. |
| OBS-010 | `test_views_extra.py` | 4 of its 4 tests are exact duplicates of tests already in `test_views.py` (see Section 12.7). |
| OBS-011 | Bootstrap JS/CSS version mismatch | `base.html` loads Bootstrap JS `5.3.7` from CDN while `static/bootstrap.min.css` is built from Bootstrap `5.3.8`. Both are within the same minor release line and compatible, but the versions are not pinned identically. |
| OBS-012 | `navbar.html` | Retains the Bootstrap-4-era class `badge-pill` (renamed to `rounded-pill` in Bootstrap 5) on the date badge. Cosmetically inert under Bootstrap 5 but not cleaned up during the migration. |

---

## 19. Enhancement Log

| # | ISO/IEC 14764 Type | Assignee | Addresses | Key Deliverables |
|---|---|---|---|---|
| 1 | Preventive + Corrective | Mohammed Aamena Mohammed Abdulkarem | Dependency upgrades, technical debt, `--deploy` security warnings | Django pinned to 4.2.11; environment-driven `SECURE_SSL_REDIRECT`, `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`, HSTS settings; `IS_TEST` guard |
| 2 | Adaptive | Mohammed Yousef Mohammed Abdulkarem | Budget Management, Receipt Uploads, Data Export | `BudgetLimit` model + migration 0008; `Expense.receipt` FileField; `export_csv_view`; receipt view/download/zip endpoints; `MEDIA_ROOT`/`MEDIA_URL` configuration |
| 3 | Adaptive | Mohammed Aamena Mohammed Abdulkarem | User Registration, CSV Export, Budget Tracking | `register_view` + `CustomUserCreationForm` with auto-login; `budget_dashboard` view with `Decimal`-safe percentage calculation; `SheetView` user-scoped queryset |
| 4 | Perfective | Farah Hanim binti Mohd Zamri | Bootstrap 5 migration, Dark Mode toggle | Bootstrap 4 → 5.3.8 migration (old stylesheet retained as backup); `data-theme` attribute mechanism; `ihtb-theme` `localStorage` key; anti-flash `<head>` script; `.dark-mode-toggle` button; dark-mode CSS in `static/styles.css` |
| 5 | Perfective | Farah Hanim binti Mohd Zamri | Automated test coverage (`fail_under = 91`), monthly spend calculation, automated validation | 12 test classes / 55 tests in `test_views_comprehensive.py`; 10 pytest tests in `test_views.py`; 7 receipt-view tests; 4 model tests; 7 form tests; 8 template-tag tests; 1 application view test; 3 utility view tests; `.coveragerc`; `.pre-commit-config.yaml`; 91% coverage achieved (95 passed, 4 skipped) |
| 6 | Adaptive | Mohammed Yousef Mohammed Abdulkarem | Containerised deployment, media volume persistence | `Dockerfile` (Python 3.10, Daphne ASGI, cron); `docker-compose.yml` (app + Caddy services, `media_volume`, `static` volume); `Caddyfile.example` |

---