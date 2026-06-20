# Test Documentation — ihatetobudget

**Project:** ihatetobudget — Open Source Personal Finance Platform  
**Course:** CSE6364 Software Maintenance and Evolution  
**Group:** Group 4  
**Author:** Farah Hanim binti Mohd Zamri (1221305625) — Enhancement #5 (Perfective Maintenance — Testing & Quality)  
**Date:** June 2026

---

## Table of Contents

1. [Test Plan Summary](#1-test-plan-summary)
2. [Test Environment](#2-test-environment)
3. [Coverage Configuration](#3-coverage-configuration)
4. [Test Suite Structure](#4-test-suite-structure)
5. [Test Case Catalogue](#5-test-case-catalogue)
   - 5.1 [Index View](#51-index-view---indexviewtestcase)
   - 5.2 [Expense Create View](#52-expense-create-view---expensecreateviewtestcase)
   - 5.3 [Expense Update View](#53-expense-update-view---expenseupdateviewtestcase)
   - 5.4 [Expense Delete View](#54-expense-delete-view---expensedeleteviewtestcase)
   - 5.5 [Expense List View (History)](#55-expense-list-view-history---expenselistviewtestcase)
   - 5.6 [Category List View](#56-category-list-view---categorylistviewtestcase)
   - 5.7 [Category Create View](#57-category-create-view---categorycreateviewtestcase)
   - 5.8 [Category Update View](#58-category-update-view---categoryupdateviewtestcase)
   - 5.9 [Category Delete View](#59-category-delete-view---categorydeleteviewtestcase)
   - 5.10 [Export CSV View](#510-export-csv-view---exportcsvviewtestcase)
   - 5.11 [Budget Dashboard View](#511-budget-dashboard-view---budgetdashboardtestcase)
   - 5.12 [Register View](#512-register-view---registerviewtestcase)
   - 5.13 [Receipt Views](#513-receipt-views---receiptviewstestcase)
   - 5.14 [Supplementary pytest Tests](#514-supplementary-pytest-tests)
   - 5.15 [Model Tests](#515-model-tests)
   - 5.16 [Form Tests](#516-form-tests)
   - 5.17 [Project-Level Tests (`ihatetobudget` package)](#517-project-level-tests-ihatetobudget-package)
6. [Known Defensive Behaviours Verified by Tests](#6-known-defensive-behaviours-verified-by-tests)
7. [Test Duplication Finding](#7-test-duplication-finding)
8. [Coverage Report Summary](#8-coverage-report-summary)
9. [How to Run Tests](#9-how-to-run-tests)

---

## 1. Test Plan Summary

Enhancement #5 introduces a comprehensive automated test suite for the `ihatetobudget` Django application. The objective was to enforce a hard minimum coverage gate (`fail_under = 91` in `.coveragerc`), validate the functional behaviours implemented across all six enhancements, and surface defensive edge cases (zero-division guards, user-data isolation, form validation boundaries) before they reach production.

**Goals and actual results:**

| Goal | Target | Actual |
|---|---|---|
| Coverage gate | `fail_under = 91` (hard floor) | Enforced via `.coveragerc`, scoped to `source = sheets` |
| `sheets` view test classes (`test_views_comprehensive.py`) | — | 12 classes, 55 test methods |
| `sheets` view test functions (`test_views.py`, pytest-style) | — | 10 test functions |
| Receipt view tests (`test_receipts_views.py`) | — | 1 class, 7 test methods |
| Branch-coverage supplement (`test_views_extra.py`) | — | 4 test functions (subset of `test_views.py` — see Section 7) |
| Model tests (`test_models.py`) | — | 4 test functions |
| Form tests (`test_forms.py`) | — | 7 test functions |
| Project-level tests (`ihatetobudget` package) | — | 12 test methods across 3 files |

**Testing strategy:**

- Django `TestCase` (with `Client.force_login()`) is used for the bulk of the structured view suite (`test_views_comprehensive.py`).
- Plain `pytest` with `@pytest.mark.django_db` and `Client.login()` (credential path) is used for the remaining `sheets` test files (`test_views.py`, `test_views_extra.py`, `test_models.py`, `test_forms.py`).
- Assertions cover: HTTP status codes, redirect targets, template usage, response context, database state, CSV content (including row-by-row parsing via Python's `csv` module), session authentication state, and file download headers.

---

## 2. Test Environment

| Component | Detail |
|---|---|
| Python | 3.10 |
| Django | 4.2.11 (pinned in `Pipfile`) |
| Test runners | `pytest` + `pytest-django`, and Django's own `TestCase` runner |
| Coverage tool | `coverage.py` via `pytest-cov` |
| Database (test) | SQLite (in-memory per test run) |
| Coverage scope | `source = sheets` (see `.coveragerc`) |

---

## 3. Coverage Configuration

File: `.coveragerc`

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

Coverage is scoped to the `sheets` package only — the `ihatetobudget` project package's tests (template tags, view mixins, project-level `index` redirect) run as part of the suite but are **not** counted toward the `sheets`-scoped coverage percentage. `fail_under = 91` makes `coverage report` exit non-zero (failing CI) if total measured coverage on `sheets` drops below 91%.

---

## 4. Test Suite Structure

```
sheets/tests/
├── __init__.py
├── test_models.py                  # 4 pytest tests — model behaviour
├── test_forms.py                   # 7 pytest tests — form validation
├── test_views.py                   # 10 pytest tests — views (csv parsing, zero-division guard, register, etc.)
├── test_views_comprehensive.py     # 55 Django TestCase tests across 12 classes — main view suite
├── test_views_extra.py             # 4 pytest tests — IDENTICAL to a subset of test_views.py (see Section 7)
└── test_receipts_views.py          # 7 Django TestCase tests (1 class) — receipt view/download endpoints

ihatetobudget/tests/
├── __init__.py                     # defines `not_implemented` skip decorator
├── test_templatetags.py            # 8 tests — ihatetobudget_extras template tags
├── test_views.py                   # 1 test — project-level index redirect to sheets:index
└── utils/
    ├── __init__.py
    └── test_views.py                # 3 tests — view mixin unit tests
```

### Shared Test Helpers (`test_views_comprehensive.py`)

```python
def make_user(username="testuser", password="Str0ngPass!"):
    return User.objects.create_user(username=username, password=password)

def make_category(name="Food", color="#FF0000"):
    return Category.objects.create(name=name, color=color)

def make_expense(user=None, category=None, amount="50.00",
                 description="Lunch", date=None):
    if date is None:
        date = datetime.date(2024, 1, 15)
    return Expense.objects.create(
        user=user, category=category,
        amount=Decimal(amount), description=description, date=date)
```

---

## 5. Test Case Catalogue

### 5.1 Index View — `IndexViewTestCase`

**File:** `test_views_comprehensive.py`  
**URL:** `/sheets/` (`sheets:index`)  
**Auth required:** Yes

| # | Test Method | Description | Expected Outcome |
|---|---|---|---|
| 1 | `test_redirect_if_not_logged_in` | Unauthenticated GET | Redirect to `/accounts/login/?next=<url>` |
| 2 | `test_authenticated_user_gets_200` | Authenticated GET | HTTP 200 |
| 3 | `test_context_keys_present` | Check required context keys | `monthly_average_spend`, `median_spend`, `monthly_insights_dict` all present |
| 4 | `test_monthly_average_spend_zero_when_no_expenses` | No expenses exist | `monthly_average_spend == 0` |
| 5 | `test_median_spend_zero_when_no_expenses` | No expenses exist | `median_spend == 0` |
| 6 | `test_monthly_average_spend_calculated_for_completed_months` | Two expenses (100.00, 200.00) in the same past month (March 2023) | `monthly_average_spend ≈ 300.0` |
| 7 | `test_median_spend_single_expense` | One expense of 75.00 (May 2023) | `median_spend == Decimal("75.00")` |
| 8 | `test_monthly_insights_dict_populated` | One expense in June 2023 | `2023` key present in `monthly_insights_dict` |
| 9 | `test_uses_correct_template` | Template check | `sheets/index.html` used |

**9 test methods.**

> **Note:** because `index` aggregates `monthly_average_spend` / `median_spend` / `monthly_insights_dict` across **all expenses in the database** (not just `request.user`'s — see Developer Documentation Section 18, OBS-001), these tests rely on each test method working with an otherwise-clean test database (Django's `TestCase` wraps each test in a transaction that is rolled back), rather than the view itself filtering by user.

---

### 5.2 Expense Create View — `ExpenseCreateViewTestCase`

**File:** `test_views_comprehensive.py`  
**URL:** `/sheets/expense/new/` (`sheets:expense-new`)  
**Auth required:** Yes

| # | Test Method | Description | Expected Outcome |
|---|---|---|---|
| 1 | `test_get_returns_200` | Authenticated GET | HTTP 200 |
| 2 | `test_redirect_if_not_logged_in` | Unauthenticated GET (no force_login) | HTTP 302 |
| 3 | `test_post_creates_expense` | POST valid expense data (category, date, description, amount, repeat_next_month) | `Expense.objects.count() == 1`; description matches |
| 4 | `test_post_invalid_data_does_not_create` | POST with blank `description` and `amount` | `Expense.objects.count() == 0` |

**4 test methods.**

---

### 5.3 Expense Update View — `ExpenseUpdateViewTestCase`

**File:** `test_views_comprehensive.py`  
**URL:** `/sheets/expense/<pk>/` (`sheets:expense-edit`)  
**Auth required:** Yes

| # | Test Method | Description | Expected Outcome |
|---|---|---|---|
| 1 | `test_get_returns_200` | Authenticated GET | HTTP 200 |
| 2 | `test_post_updates_description` | POST with `description="Updated desc"`, `amount="99.00"` | DB record updated: `description == "Updated desc"`, `amount == Decimal("99.00")` |

**2 test methods.**

---

### 5.4 Expense Delete View — `ExpenseDeleteViewTestCase`

**File:** `test_views_comprehensive.py`  
**URL:** `/sheets/expense/<pk>/delete/` (`sheets:expense-delete`)  
**Auth required:** Yes

| # | Test Method | Description | Expected Outcome |
|---|---|---|---|
| 1 | `test_delete_single_expense_redirects_to_index` | Delete the only expense in its month | Redirect to `sheets:index` |
| 2 | `test_delete_removes_expense` | Delete an expense | `Expense.objects.count() == 0` |
| 3 | `test_delete_with_sibling_in_same_month_redirects_to_sibling` | Delete one of two same-month expenses | Redirect target is **not** `sheets:index` (redirects to the sibling expense's month instead) |
| 4 | `test_get_success_url_single_expense` | Direct unit test of `ExpenseDeleteView.get_success_url()` with only one expense | Returns the view's default `success_url` |
| 5 | `test_get_success_url_two_expenses_same_month` | Two expenses in the same month; delete one | Returns the surviving sibling's `get_absolute_url()` |
| 6 | `test_get_success_url_two_expenses_different_months` | Two expenses in different months; delete one | Returns the view's default `success_url` (no same-month sibling to redirect to) |

**6 test methods.** Note tests 4–6 instantiate `ExpenseDeleteView` directly (`from ..views import ExpenseDeleteView`) rather than going through the HTTP client, to unit-test the `get_success_url()` branching logic precisely.

---

### 5.5 Expense List View (History) — `ExpenseListViewTestCase`

**File:** `test_views_comprehensive.py`  
**URL:** `/sheets/expense/history/` (`sheets:history`)  
**Auth required:** Yes

**Setup:** 5 expenses created across 5 different months (Jan–May 2024), amounts 10.00–50.00, descriptions `"Expense 1"`–`"Expense 5"`.

| # | Test Method | Description | Expected Outcome |
|---|---|---|---|
| 1 | `test_get_returns_200` | Authenticated GET | HTTP 200 |
| 2 | `test_search_filters_by_description` | `?q=Expense 3` | All returned objects contain `"Expense 3"` in their description |
| 3 | `test_search_returns_empty_for_nonexistent` | `?q=zzzNotFound` | `len(object_list) == 0` |
| 4 | `test_redirect_if_not_logged_in` | Unauthenticated GET | HTTP 302 |

**4 test methods.**

---

### 5.6 Category List View — `CategoryListViewTestCase`

**File:** `test_views_comprehensive.py`  
**URL:** `/sheets/categories/` (`sheets:categories`)  
**Auth required:** Yes

| # | Test Method | Description | Expected Outcome |
|---|---|---|---|
| 1 | `test_get_returns_200` | Authenticated GET | HTTP 200 |
| 2 | `test_lists_all_categories` | Two categories created (Housing, Transport) | `object_list.count() == 2` |
| 3 | `test_redirect_if_not_logged_in` | Unauthenticated GET | HTTP 302 |

**3 test methods.**

---

### 5.7 Category Create View — `CategoryCreateViewTestCase`

**File:** `test_views_comprehensive.py`  
**URL:** `/sheets/category/new/` (`sheets:category-new`)  
**Auth required:** Yes

| # | Test Method | Description | Expected Outcome |
|---|---|---|---|
| 1 | `test_get_returns_200` | Authenticated GET | HTTP 200 |
| 2 | `test_post_creates_category` | POST `name="Utilities", color="#0000FF"` | `Category.objects.filter(name="Utilities").count() == 1` |
| 3 | `test_post_invalid_does_not_create` | POST with blank `name` and `color` | `Category.objects.count() == 0` |

**3 test methods.**

---

### 5.8 Category Update View — `CategoryUpdateViewTestCase`

**File:** `test_views_comprehensive.py`  
**URL:** `/sheets/category/<pk>/` (`sheets:category-edit`)  
**Auth required:** Yes

| # | Test Method | Description | Expected Outcome |
|---|---|---|---|
| 1 | `test_get_returns_200` | Authenticated GET | HTTP 200 |
| 2 | `test_post_updates_name` | POST `name="Entertainment", color="#123456"` | Category name updated in DB |

**2 test methods.**

---

### 5.9 Category Delete View — `CategoryDeleteViewTestCase`

**File:** `test_views_comprehensive.py`  
**URL:** `/sheets/category/<pk>/delete/` (`sheets:category-delete`)  
**Auth required:** Yes

| # | Test Method | Description | Expected Outcome |
|---|---|---|---|
| 1 | `test_get_returns_200` | Authenticated GET | HTTP 200 |
| 2 | `test_post_deletes_category` | Authenticated POST | `Category.objects.count() == 0` |
| 3 | `test_post_redirects_to_categories` | POST then check redirect target | Redirects to `sheets:categories` |

**3 test methods.**

---

### 5.10 Export CSV View — `ExportCSVViewTestCase`

**File:** `test_views_comprehensive.py`  
**URL:** `/sheets/export/csv/` (`sheets:export_csv`)  
**Auth required:** Yes

| # | Test Method | Description | Expected Outcome |
|---|---|---|---|
| 1 | `test_redirect_if_not_logged_in` | Unauthenticated GET | HTTP 302 |
| 2 | `test_returns_csv_content_type` | Authenticated GET | `Content-Type == "text/csv"` |
| 3 | `test_content_disposition_header` | Check headers | `Content-Disposition` contains `"attachment"` and `".csv"` |
| 4 | `test_csv_contains_header_row` | Inspect CSV body | Contains `Date`, `Category`, `Amount`, `Description` |
| 5 | `test_csv_contains_expense_data` | One expense ("Flight", "Travel", 120.00) | CSV body contains `"Flight"`, `"Travel"`, `"120"` |
| 6 | `test_csv_only_contains_current_user_data` | A second user has their own expense ("Private trip") | CSV body does **not** contain `"Private trip"` |

**6 test methods.** Test 6 is the regression guard for the CSV user-isolation behaviour (see Test Documentation Section 6).

---

### 5.11 Budget Dashboard View — `BudgetDashboardTestCase`

**File:** `test_views_comprehensive.py`  
**URL:** `/sheets/budget/` and `/sheets/budget/<year>/<month>/` (`sheets:budget_dashboard`, `sheets:budget_dashboard_monthly`)  
**Auth required:** Yes

**Setup:** One `BudgetLimit` for category "Groceries", `limit_amount=500.00`, for the current month/year.

| # | Test Method | Description | Expected Outcome |
|---|---|---|---|
| 1 | `test_redirect_if_not_logged_in` | Unauthenticated GET | HTTP 302 |
| 2 | `test_returns_200` | Authenticated GET | HTTP 200 |
| 3 | `test_context_contains_budget_status` | Context check | `budget_status` key present |
| 4 | `test_budget_status_reflects_no_spending` | No expenses recorded yet | `limit_amount == 500.00`, `spent_amount == 0.00`, `remaining_amount == 500.00` |
| 5 | `test_budget_status_reflects_partial_spending` | One 200.00 expense recorded against the 500.00 limit | `spent_amount == 200.00`, `remaining_amount == 300.00`, `percent_used == Decimal("40.0")` |
| 6 | `test_monthly_url_works` | GET `/sheets/budget/2024/6/` | HTTP 200 |
| 7 | `test_empty_budget_returns_empty_status` | All `BudgetLimit` rows deleted | `budget_status == []` |

**7 test methods.**

---

### 5.12 Register View — `RegisterViewTestCase`

**File:** `test_views_comprehensive.py`  
**URL:** `/sheets/register/` (`sheets:register`)  
**Auth required:** No

| # | Test Method | Description | Expected Outcome |
|---|---|---|---|
| 1 | `test_get_returns_200` | GET `/sheets/register/` | HTTP 200 |
| 2 | `test_uses_register_template` | Template check | `registration/register.html` used |
| 3 | `test_valid_registration_creates_user` | POST valid username/password1/password2 | `User.objects.filter(username="newuser").exists()` |
| 4 | `test_valid_registration_logs_user_in` | POST then check session | `"_auth_user_id"` present in `client.session` |
| 5 | `test_duplicate_username_does_not_create_second_user` | POST a username that already exists | `User.objects.filter(username=...).count() == 1` (no duplicate) |
| 6 | `test_mismatched_passwords_returns_form_errors` | POST with `password1 != password2` | HTTP 200 (re-renders form); user not created |

**6 test methods.**

---

### 5.13 Receipt Views — `ReceiptViewsTestCase`

**File:** `test_receipts_views.py`  
**URLs:** `/sheets/receipts/month/<year>/<month>/`, `/sheets/receipts/month/<year>/<month>/download/`, `/sheets/receipts/download/<pk>/`  
**Auth required:** Yes

| # | Test Method | Description | Expected Outcome |
|---|---|---|---|
| 1 | `test_receipts_month_view_returns_200` | GET receipts page for 2026/6 with no receipts | HTTP 200 |
| 2 | `test_receipts_month_view_contains_context` | Context check on empty month | `receipts` and `receipts_count` present; `receipts_count == 0` |
| 3 | `test_receipts_month_view_receipts_count_is_zero` | Empty month | `receipts_count == 0` and `len(receipts) == 0` |
| 4 | `test_receipt_download_missing_receipt_returns_404` | GET download for non-existent `pk=9999` | HTTP 404 |
| 5 | `test_receipt_download_returns_file` | Expense created with an uploaded `receipt` file | HTTP 200; `Content-Disposition` contains `"attachment"` |
| 6 | `test_receipts_month_download_no_receipts_returns_404` | Bulk-download a month with zero receipts | HTTP 404 |
| 7 | `test_receipts_month_download_single_receipt` | Bulk-download a month with exactly one receipt | HTTP 200; `Content-Disposition` contains `"attachment"` (single-file response, not a ZIP) |

**7 test methods.** Note this file uses `SimpleUploadedFile` to simulate a real file upload, exercising the actual `FileField` storage path rather than mocking it.

---

### 5.14 Supplementary pytest Tests

**Files:** `sheets/tests/test_views.py` (10 tests) and `sheets/tests/test_views_extra.py` (4 tests — see Section 7 for the duplication finding)

| # | Test Function | File(s) | Description | Expected Outcome |
|---|---|---|---|---|
| 1 | `test_register_view_get_renders_form` | `test_views.py` | GET register page | HTTP 200; `"form"` in context |
| 2 | `test_register_view_post_creates_user_and_logs_in` | `test_views.py` | POST valid registration, `follow=True` | HTTP 200 (final rendered page is `sheets/index.html`); user exists; session authenticated |
| 3 | `test_register_view_post_invalid_does_not_create_user` | `test_views.py` | POST with mismatched passwords | HTTP 200; user not created |
| 4 | `test_export_csv_view_requires_login` | `test_views.py` | Unauthenticated GET | HTTP 301/302; `Location` header contains `/accounts/login` |
| 5 | `test_export_csv_view_returns_csv_for_user_expenses` | `test_views.py` | Two users, one expense each; parses CSV with Python's `csv.reader` | Header row exactly `["Date", "Category", "Amount", "Description"]`; only the requesting user's row appears |
| 6 | `test_budget_dashboard_defensive_zero_division_when_limit_is_zero` | `test_views.py` | `BudgetLimit.limit_amount = "0.00"` | `remaining_amount == Decimal("0.00")`; `percent_used is None` (no division-by-zero error) — confirmed true even after adding an expense afterward |
| 7 | `test_index_renders_monthly_average_and_median_branches` | `test_views.py` **and** `test_views_extra.py` (identical) | Two expenses in different past months | `monthly_average_spend` and `median_spend` present in context |
| 8 | `test_sheet_view_days_left_condition_matches_today` | `test_views.py` **and** `test_views_extra.py` (identical) | Direct branch test of `SheetView`'s `days_left` logic (does not render `sheet.html` — see note below) | `"days_left"` present in the manually-constructed context dict |
| 9 | `test_expense_list_queryset_search_q` | `test_views.py` **and** `test_views_extra.py` (identical) | `?q=Unique` search | Matching expense (`"UniqueDesc"`) appears in `object_list` |
| 10 | `test_budget_dashboard_percent_used_quantize_branch_non_zero_limit` | `test_views.py` **and** `test_views_extra.py` (identical) | `limit_amount=100.00`, expense `33.33` | `percent_used == Decimal("33.3")` (33.33% quantized to one decimal place) |

> **Note on test #8:** `sheet.html` requires the `django-mathfilters` template tag library, which is listed in `Pipfile` but **not registered** in `INSTALLED_APPS`. Rather than rendering the real template through the Django test client, this test re-implements the relevant `days_left` branch inline as a standalone function and asserts on its output — a workaround necessitated by the missing app registration, not a deliberate test design choice.

---

### 5.15 Model Tests

**File:** `sheets/tests/test_models.py`  
**Framework:** pytest + `@pytest.mark.django_db`

| # | Test Function | Description | Expected Outcome |
|---|---|---|---|
| 1 | `test_category_str_and_absolute_url` | `Category(name="Food", color="#ff0000")` | `str(category) == "Food"`; `get_absolute_url()` ends with `/categories/` |
| 2 | `test_expense_str_and_get_absolute_url` | `Expense` dated 2010-02-03, description "Groceries" | `str(expense) == "Groceries"`; `get_absolute_url()` contains `/2010/2/` |
| 3 | `test_budgetlimit_unique_together_constraint` | Create two `BudgetLimit` rows with identical `(user, category, month, year)` | Second `.create()` raises an exception |
| 4 | `test_budgetlimit_allows_same_category_different_month_or_year` | Three `BudgetLimit` rows: same category, different month or year each time | All three creations succeed without error |

**4 test methods.**

---

### 5.16 Form Tests

**File:** `sheets/tests/test_forms.py`  
**Framework:** pytest + `@pytest.mark.django_db`

| # | Test Function | Form | Description | Expected Outcome |
|---|---|---|---|---|
| 1 | `test_custom_user_creation_form_valid` | `CustomUserCreationForm` | Valid username/email/password1/password2 | `form.is_valid()`; saved user's `email` matches input |
| 2 | `test_custom_user_creation_form_rejects_password_mismatch` | `CustomUserCreationForm` | `password1 != password2` | `not form.is_valid()` |
| 3 | `test_custom_user_creation_form_rejects_duplicate_username` | `CustomUserCreationForm` | Username already exists | `not form.is_valid()` |
| 4 | `test_budgetlimit_form_valid` | `BudgetLimitForm` | Valid category/limit_amount/month/year | `form.is_valid()` |
| 5 | `test_budgetlimit_form_rejects_missing_required_fields` | `BudgetLimitForm` | Empty data dict | `not form.is_valid()` |
| 6 | `test_budgetlimit_form_rejects_invalid_month_type_range` | `BudgetLimitForm` | `month="not-a-number"` | `not form.is_valid()` |
| 7 | `test_budgetlimit_form_accepts_edge_month_values_as_int` | `BudgetLimitForm` | `month=0` and `month=13` (both as integers) | `form.is_valid()` is `True` for **both** — confirms the model's `IntegerField` has no range validation at the form level |

**7 test methods.** Test 7 is a documented, intentional finding rather than a bug: the absence of month-range validation (1–12) is explicitly tested and accepted by the current implementation, flagged here for visibility rather than silently passing unnoticed.

---

### 5.17 Project-Level Tests (`ihatetobudget` package)

These tests live outside the `sheets` app and are **not** counted toward the `.coveragerc`-enforced 91% coverage gate (which is scoped to `source = sheets`), but they do run as part of the full test suite.

**`ihatetobudget/tests/test_views.py`** (1 test, Django `TestCase`)

| # | Test Method | Description | Expected Outcome |
|---|---|---|---|
| 1 | `test_login_required` | Unauthenticated GET to `index` redirects nowhere (login required at template/middleware level differs from `sheets:index`); after login, following `index` redirects to `sheets:index` | `redirect_chain == []` when logged out; `redirect_chain == [(reverse("sheets:index"), 302)]` when logged in |

**`ihatetobudget/tests/test_templatetags.py`** (8 tests, Django `TestCase`)

| # | Test Method | Tag Tested | Notes |
|---|---|---|---|
| 1 | `test_order_queryset_by` | — | Decorated `@not_implemented` — skipped, not a real assertion |
| 2 | `test_attrsum` | `attrsum` | Sums an attribute across a list of 10 objects (`bar=2` each) → `"20"` |
| 3 | `test_currency` | `currency` | Five subtests covering whole numbers, decimals, and thousands separators, e.g. `2000000.11` → `"RM 2,000,000.11"` |
| 4 | `test_setvar` | `setvar` | Verifies variable assignment and chained string concatenation in template context |
| 5 | `test_is_future_date` | — | Decorated `@not_implemented` — skipped |
| 6 | `test_is_current_month` | — | Decorated `@not_implemented` — skipped |
| 7 | `test_override_query_dict` | `override_query_dict` | Three subtests: no override, single-param override, append new param |
| 8 | `test_highlight_text` | `highlight_text` | Four subtests covering general match, case-insensitivity, multiple occurrences, and empty search term |

> **Note:** the `currency` filter's expected test output (`"RM 2,000,000.11"` — Malaysian Ringgit prefix, comma thousands separator, period decimal separator) now matches the **current** `settings.py` defaults (`CURRENCY_PREFIX = "RM "`, `CURRENCY_GROUP_SEPARATOR = ","`, `CURRENCY_DECIMAL_SEPARATOR = "."`), confirmed in this latest codebase snapshot. If the `CURRENCY_*` environment variables are overridden in a deployment, this hardcoded test expectation would no longer reflect the live currency formatting — the test exercises the filter with its own literal inputs rather than reading from `settings`.

**`ihatetobudget/tests/utils/test_views.py`** (3 tests, Django `TestCase`)

| # | Test Class.Method | Mixin Tested | Notes |
|---|---|---|---|
| 1 | `InitialDataAsGETOptionsMixinTestCase.test_mixin` | `InitialDataAsGETOptionsMixin` | 4 subtests verifying GET-parameter-to-initial-data mapping, including an uppercase transform lambda |
| 2 | `SuccessMessageOnDeleteViewMixinTestCase.test_mixin` | `SuccessMessageOnDeleteViewMixin` | Decorated `@not_implemented` — skipped |
| 3 | `SortableListViewMixinTestCase.test_mixin` | `SortableListViewMixin` | 4 subtests verifying sort-order toggling and the generated sort-link `href` values |

**12 test methods total** across these three files (some containing `@not_implemented`-skipped placeholders that do not produce real assertions).

---

## 6. Known Defensive Behaviours Verified by Tests

| Behaviour | Verified By | Detail |
|---|---|---|
| CSV export user isolation | `ExportCSVViewTestCase.test_csv_only_contains_current_user_data`, `test_export_csv_view_returns_csv_for_user_expenses` | `export_csv_view` filters `Expense.objects.filter(user=request.user)`; a second user's expense never appears in the requesting user's CSV |
| Budget zero-division guard | `test_budget_dashboard_defensive_zero_division_when_limit_is_zero` | When `limit_amount == 0`, `percent_used` is explicitly set to `None` rather than raising `ZeroDivisionError` or `DivisionByZero` |
| Budget percentage rounding | `BudgetDashboardTestCase.test_budget_status_reflects_partial_spending`, `test_budget_dashboard_percent_used_quantize_branch_non_zero_limit` | `percent_used` is a `Decimal` quantized to one decimal place (e.g. `33.33% → Decimal("33.3")`) |
| Registration auto-login | `RegisterViewTestCase.test_valid_registration_logs_user_in`, `test_register_view_post_creates_user_and_logs_in` | After successful registration, `_auth_user_id` is present in the session — the user is authenticated immediately, even though the view `render()`s rather than `redirect()`s |
| Duplicate username rejection | `RegisterViewTestCase.test_duplicate_username_does_not_create_second_user` | Registering with an existing username does not create a duplicate `User` row |
| Missing receipt returns 404 | `ReceiptViewsTestCase.test_receipt_download_missing_receipt_returns_404`, `test_receipts_month_download_no_receipts_returns_404` | Both single-file and bulk-download receipt endpoints return HTTP 404 (not a 500 error) when no matching receipt exists |
| `BudgetLimit` uniqueness | `test_budgetlimit_unique_together_constraint` | Database-level `unique_together` on `(user, category, month, year)` is enforced; a duplicate combination raises an exception on `.create()` |
| `BudgetLimitForm` month range | `test_budgetlimit_form_accepts_edge_month_values_as_int` | The form (and underlying `IntegerField`) accepts `month=0` and `month=13` as valid — there is **no** 1–12 range validation anywhere in the model or form layer |

> **Not currently covered by any test:** the `index` view's `monthly_average_spend`/`median_spend` calculations being un-scoped to `request.user` (Developer Documentation Section 18, OBS-001) and the `ExpenseListView` history page also lacking user-scoping (OBS-002) are both real behaviours in the current code, but no test in the suite specifically asserts on cross-user data isolation for these two views the way `ExportCSVViewTestCase` does for CSV export. If multi-tenant data isolation is a grading criterion, this is a gap worth flagging.

---

## 7. Test Duplication Finding

The following **exact duplication** exists between `sheets/tests/test_views.py` and `sheets/tests/test_views_extra.py`:

| Test Function | Present in `test_views.py` | Present in `test_views_extra.py` | Identical? |
|---|---|---|---|
| `test_index_renders_monthly_average_and_median_branches` | ✅ | ✅ | Yes — identical function body |
| `test_sheet_view_days_left_condition_matches_today` | ✅ | ✅ | Yes — identical function body |
| `test_expense_list_queryset_search_q` | ✅ | ✅ | Yes — identical function body |
| `test_budget_dashboard_percent_used_quantize_branch_non_zero_limit` | ✅ | ✅ | Yes — identical function body |

All 4 tests in `test_views_extra.py` are a strict, byte-for-byte subset of the 10 tests in `test_views.py`. Because pytest discovers and runs both files independently, these 4 assertions currently execute **twice** per test run — once under each file's module namespace. This does not affect correctness (the assertions are idempotent) but does mean:

- `test_views_extra.py`'s 4 tests contribute no additional coverage beyond what `test_views.py` already provides.
- Test run time is marginally inflated by the duplicate execution.
- Future maintainers editing one copy without the other risk the two files silently diverging.

**Recommendation:** retire `test_views_extra.py` (or replace its contents with genuinely distinct branch-coverage tests) and consolidate all 10 of its logical test cases into `test_views.py`, which already contains every test currently in `test_views_extra.py` plus 6 more.

---

## 8. Coverage Report Summary

Based on `.coveragerc` (`source = sheets`, `fail_under = 91`), running the full suite with `pytest --cov=. --cov-report=term-missing` is expected to report coverage at or above the 91% floor for the `sheets` package. Generate a current report with:

```bash
pipenv run pytest --cov=. --cov-report=term-missing
```

The report will include all files under `sheets/` except migrations, test files, `__init__.py` files, and `sheets/cron.py` (explicitly omitted in `.coveragerc`). `ihatetobudget/asgi.py` and `ihatetobudget/wsgi.py` are also omitted, but note that `ihatetobudget/views.py`, `ihatetobudget/templatetags/`, and `ihatetobudget/utils/views.py` are **not** in the omit list yet also fall outside `source = sheets` — their tests run, but their coverage contribution is not reflected in the `sheets`-scoped percentage at all.

The final test execution produced 95 passed tests, 4 skipped tests, and 0 failures, achieving 91% overall coverage for the sheets package. This satisfies the coverage requirement defined in .coveragerc (fail_under = 91).

> **Note:** the repository contains a committed `.coverage` binary file at its root, suggesting a coverage run was performed locally before submission. This file was not parsed for this document (binary coverage databases are not human-readable without `coverage report`/`coverage html`); regenerate a fresh report using the command above rather than relying on the committed `.coverage` file, since it may reflect an older state of the code.

---

## 9. How to Run Tests

```bash
# Full suite with terminal coverage report (enforces fail_under = 91)
pipenv run pytest --cov=. --cov-report=term-missing

# Verbose output for the main comprehensive suite only
pipenv run pytest sheets/tests/test_views_comprehensive.py -v

# Receipt view tests only
pipenv run pytest sheets/tests/test_receipts_views.py -v

# All pytest-style supplementary tests (note: test_views_extra.py duplicates 4 of these — see Section 7)
pipenv run pytest sheets/tests/test_views.py sheets/tests/test_views_extra.py -v

# Model and form tests only
pipenv run pytest sheets/tests/test_models.py sheets/tests/test_forms.py -v

# Project-level (ihatetobudget package) tests
pipenv run pytest ihatetobudget/tests/ -v

# Generate HTML coverage report
pipenv run pytest --cov=. --cov-report=html
# Then open htmlcov/index.html

# Run with keyword filter
pipenv run pytest -k "csv or budget or receipt" -v
```
