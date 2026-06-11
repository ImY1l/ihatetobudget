"""
Comprehensive test suite for sheets app views.
Enhancement #5 – Perfective Maintenance (Testing & Quality)
Author: Farah Hanim binti Mohd Zamri (1221305625)

Coverage targets:
  - index view (monthly_average_spend, median_spend, login-required redirect)
  - SheetView (days_left context, current-month vs. other-month)
  - ExpenseCreateView / ExpenseUpdateView / ExpenseDeleteView
  - ExpenseListView (search, pagination)
  - CategoryListView / CategoryCreateView / CategoryUpdateView / CategoryDeleteView
  - export_csv_view
  - budget_dashboard
  - register_view
"""

import datetime
from decimal import Decimal

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from ..models import BudgetLimit, Category, Expense


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_user(username="testuser", password="Str0ngPass!"):
    return User.objects.create_user(username=username, password=password)


def make_category(name="Food", color="#FF0000"):
    return Category.objects.create(name=name, color=color)


def make_expense(user=None, category=None, amount="50.00",
                 description="Lunch", date=None):
    if date is None:
        date = datetime.date(2024, 1, 15)
    return Expense.objects.create(
        user=user,
        category=category,
        amount=Decimal(amount),
        description=description,
        date=date,
    )


# ---------------------------------------------------------------------------
# index view
# ---------------------------------------------------------------------------

class IndexViewTestCase(TestCase):
    def setUp(self):
        self.user = make_user()
        self.client = Client()
        self.url = reverse("sheets:index")

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, f"/accounts/login/?next={self.url}")

    def test_authenticated_user_gets_200(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_context_keys_present(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        for key in ("monthly_average_spend", "median_spend",
                    "monthly_insights_dict"):
            self.assertIn(key, response.context)

    def test_monthly_average_spend_zero_when_no_expenses(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.context["monthly_average_spend"], 0)

    def test_median_spend_zero_when_no_expenses(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.context["median_spend"], 0)

    def test_monthly_average_spend_calculated_for_completed_months(self):
        """Only expenses in months strictly before the current month count."""
        self.client.force_login(self.user)
        # Two expenses in the same past month
        past_month = datetime.date(2023, 3, 10)
        make_expense(self.user, amount="100.00", date=past_month)
        make_expense(self.user, amount="200.00",
                     date=past_month.replace(day=20))
        response = self.client.get(self.url)
        avg = response.context["monthly_average_spend"]
        self.assertAlmostEqual(float(avg), 300.0, places=2)

    def test_median_spend_single_expense(self):
        self.client.force_login(self.user)
        make_expense(self.user, amount="75.00",
                     date=datetime.date(2023, 5, 1))
        response = self.client.get(self.url)
        self.assertEqual(response.context["median_spend"], Decimal("75.00"))

    def test_monthly_insights_dict_populated(self):
        self.client.force_login(self.user)
        make_expense(self.user, amount="10.00",
                     date=datetime.date(2023, 6, 1))
        response = self.client.get(self.url)
        self.assertIn(2023, response.context["monthly_insights_dict"])

    def test_uses_correct_template(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "sheets/index.html")

# ---------------------------------------------------------------------------
# ExpenseCreateView
# ---------------------------------------------------------------------------

class ExpenseCreateViewTestCase(TestCase):
    def setUp(self):
        self.user = make_user()
        self.client = Client()
        self.client.force_login(self.user)
        self.url = reverse("sheets:expense-new")
        self.category = make_category()

    def test_get_returns_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_redirect_if_not_logged_in(self):
        c = Client()
        response = c.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_post_creates_expense(self):
        data = {
            "category": self.category.pk,
            "date": "2024-03-01",
            "description": "Groceries",
            "amount": "45.50",
            "repeat_next_month": False,
        }
        response = self.client.post(self.url, data)
        self.assertEqual(Expense.objects.count(), 1)
        expense = Expense.objects.first()
        self.assertEqual(expense.description, "Groceries")

    def test_post_invalid_data_does_not_create(self):
        data = {
            "date": "2024-03-01",
            "description": "",  # blank — violates model CharField
            "amount": "",
        }
        self.client.post(self.url, data)
        self.assertEqual(Expense.objects.count(), 0)


# ---------------------------------------------------------------------------
# ExpenseUpdateView
# ---------------------------------------------------------------------------

class ExpenseUpdateViewTestCase(TestCase):
    def setUp(self):
        self.user = make_user()
        self.client = Client()
        self.client.force_login(self.user)
        self.category = make_category()
        self.expense = make_expense(self.user, self.category)
        self.url = reverse("sheets:expense-edit",
                           kwargs={"pk": self.expense.pk})

    def test_get_returns_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_post_updates_description(self):
        data = {
            "category": self.category.pk,
            "date": str(self.expense.date),
            "description": "Updated desc",
            "amount": "99.00",
            "repeat_next_month": False,
        }
        self.client.post(self.url, data)
        self.expense.refresh_from_db()
        self.assertEqual(self.expense.description, "Updated desc")
        self.assertEqual(self.expense.amount, Decimal("99.00"))


# ---------------------------------------------------------------------------
# ExpenseDeleteView
# ---------------------------------------------------------------------------

class ExpenseDeleteViewTestCase(TestCase):
    def setUp(self):
        self.user = make_user()
        self.client = Client()
        self.client.force_login(self.user)

    def _make_and_delete(self, *dates):
        expenses = [make_expense(self.user,
                                 date=datetime.date(*d)) for d in dates]
        url = reverse("sheets:expense-delete",
                      kwargs={"pk": expenses[0].pk})
        return self.client.post(url), expenses

    def test_delete_single_expense_redirects_to_index(self):
        response, _ = self._make_and_delete((2023, 5, 1))
        self.assertRedirects(response, reverse("sheets:index"),
                             fetch_redirect_response=False)

    def test_delete_removes_expense(self):
        _, expenses = self._make_and_delete((2023, 5, 1))
        self.assertEqual(Expense.objects.count(), 0)

    def test_delete_with_sibling_in_same_month_redirects_to_sibling(self):
        e1 = make_expense(self.user, date=datetime.date(2023, 5, 1))
        e2 = make_expense(self.user, date=datetime.date(2023, 5, 10))
        url = reverse("sheets:expense-delete", kwargs={"pk": e1.pk})
        response = self.client.post(url)
        # Should redirect to the sibling expense's sheet, not the index
        self.assertEqual(response.status_code, 302)
        self.assertNotEqual(response["Location"], reverse("sheets:index"))

    def test_get_success_url_single_expense(self):
        from ..views import ExpenseDeleteView
        expense = make_expense(self.user, date=datetime.date(2010, 1, 1))
        view = ExpenseDeleteView(object=expense)
        self.assertEqual(view.get_success_url(), view.success_url)

    def test_get_success_url_two_expenses_same_month(self):
        from ..views import ExpenseDeleteView
        e2 = make_expense(self.user, date=datetime.date(2010, 2, 1))
        e3 = make_expense(self.user, date=datetime.date(2010, 2, 2))
        view = ExpenseDeleteView(object=e2)
        self.assertEqual(view.get_success_url(), e3.get_absolute_url())

    def test_get_success_url_two_expenses_different_months(self):
        from ..views import ExpenseDeleteView
        e4 = make_expense(self.user, date=datetime.date(2010, 3, 1))
        make_expense(self.user, date=datetime.date(2010, 4, 1))
        view = ExpenseDeleteView(object=e4)
        self.assertEqual(view.get_success_url(), view.success_url)


# ---------------------------------------------------------------------------
# ExpenseListView (History)
# ---------------------------------------------------------------------------

class ExpenseListViewTestCase(TestCase):
    def setUp(self):
        self.user = make_user()
        self.client = Client()
        self.client.force_login(self.user)
        self.url = reverse("sheets:history")
        self.cat = make_category()
        for i in range(1, 6):
            make_expense(self.user, self.cat, amount=f"{i * 10}.00",
                         description=f"Expense {i}",
                         date=datetime.date(2024, i, 1))

    def test_get_returns_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_search_filters_by_description(self):
        response = self.client.get(self.url, {"q": "Expense 3"})
        self.assertEqual(response.status_code, 200)
        qs = response.context["object_list"]
        self.assertTrue(all("Expense 3" in e.description for e in qs))

    def test_search_returns_empty_for_nonexistent(self):
        response = self.client.get(self.url, {"q": "zzzNotFound"})
        self.assertEqual(len(response.context["object_list"]), 0)

    def test_redirect_if_not_logged_in(self):
        c = Client()
        response = c.get(self.url)
        self.assertEqual(response.status_code, 302)


# ---------------------------------------------------------------------------
# CategoryListView
# ---------------------------------------------------------------------------

class CategoryListViewTestCase(TestCase):
    def setUp(self):
        self.user = make_user()
        self.client = Client()
        self.client.force_login(self.user)
        self.url = reverse("sheets:categories")

    def test_get_returns_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_lists_all_categories(self):
        make_category("Housing")
        make_category("Transport")
        response = self.client.get(self.url)
        self.assertEqual(response.context["object_list"].count(), 2)

    def test_redirect_if_not_logged_in(self):
        c = Client()
        response = c.get(self.url)
        self.assertEqual(response.status_code, 302)


# ---------------------------------------------------------------------------
# CategoryCreateView
# ---------------------------------------------------------------------------

class CategoryCreateViewTestCase(TestCase):
    def setUp(self):
        self.user = make_user()
        self.client = Client()
        self.client.force_login(self.user)
        self.url = reverse("sheets:category-new")

    def test_get_returns_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_post_creates_category(self):
        self.client.post(self.url, {"name": "Utilities", "color": "#0000FF"})
        self.assertEqual(Category.objects.filter(name="Utilities").count(), 1)

    def test_post_invalid_does_not_create(self):
        self.client.post(self.url, {"name": "", "color": ""})
        self.assertEqual(Category.objects.count(), 0)


# ---------------------------------------------------------------------------
# CategoryUpdateView
# ---------------------------------------------------------------------------

class CategoryUpdateViewTestCase(TestCase):
    def setUp(self):
        self.user = make_user()
        self.client = Client()
        self.client.force_login(self.user)
        self.cat = make_category()
        self.url = reverse("sheets:category-edit",
                           kwargs={"pk": self.cat.pk})

    def test_get_returns_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_post_updates_name(self):
        self.client.post(self.url, {"name": "Entertainment",
                                    "color": "#123456"})
        self.cat.refresh_from_db()
        self.assertEqual(self.cat.name, "Entertainment")


# ---------------------------------------------------------------------------
# CategoryDeleteView
# ---------------------------------------------------------------------------

class CategoryDeleteViewTestCase(TestCase):
    def setUp(self):
        self.user = make_user()
        self.client = Client()
        self.client.force_login(self.user)
        self.cat = make_category()
        self.url = reverse("sheets:category-delete",
                           kwargs={"pk": self.cat.pk})

    def test_get_returns_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_post_deletes_category(self):
        self.client.post(self.url)
        self.assertEqual(Category.objects.count(), 0)

    def test_post_redirects_to_categories(self):
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse("sheets:categories"),
                             fetch_redirect_response=False)


# ---------------------------------------------------------------------------
# export_csv_view
# ---------------------------------------------------------------------------

class ExportCSVViewTestCase(TestCase):
    def setUp(self):
        self.user = make_user()
        self.client = Client()
        self.client.force_login(self.user)
        self.url = reverse("sheets:export_csv")
        self.cat = make_category("Travel")
        make_expense(self.user, self.cat, amount="120.00",
                     description="Flight", date=datetime.date(2024, 2, 14))

    def test_redirect_if_not_logged_in(self):
        c = Client()
        response = c.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_returns_csv_content_type(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/csv")

    def test_content_disposition_header(self):
        response = self.client.get(self.url)
        self.assertIn("attachment", response["Content-Disposition"])
        self.assertIn(".csv", response["Content-Disposition"])

    def test_csv_contains_header_row(self):
        response = self.client.get(self.url)
        content = b"".join(response.streaming_content
                           if hasattr(response, "streaming_content")
                           else [response.content]).decode()
        self.assertIn("Date", content)
        self.assertIn("Category", content)
        self.assertIn("Amount", content)
        self.assertIn("Description", content)

    def test_csv_contains_expense_data(self):
        response = self.client.get(self.url)
        content = response.content.decode()
        self.assertIn("Flight", content)
        self.assertIn("Travel", content)
        self.assertIn("120", content)

    def test_csv_only_contains_current_user_data(self):
        other_user = make_user("other", "Pass1234!")
        make_expense(other_user, self.cat, description="Private trip",
                     date=datetime.date(2024, 3, 1))
        response = self.client.get(self.url)
        content = response.content.decode()
        self.assertNotIn("Private trip", content)


# ---------------------------------------------------------------------------
# budget_dashboard
# ---------------------------------------------------------------------------

class BudgetDashboardTestCase(TestCase):
    def setUp(self):
        self.user = make_user()
        self.client = Client()
        self.client.force_login(self.user)
        self.url = reverse("sheets:budget_dashboard")
        self.cat = make_category("Groceries")
        today = datetime.date.today()
        BudgetLimit.objects.create(
            user=self.user,
            category=self.cat,
            limit_amount=Decimal("500.00"),
            month=today.month,
            year=today.year,
        )

    def test_redirect_if_not_logged_in(self):
        c = Client()
        response = c.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_returns_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_context_contains_budget_status(self):
        response = self.client.get(self.url)
        self.assertIn("budget_status", response.context)

    def test_budget_status_reflects_no_spending(self):
        response = self.client.get(self.url)
        status = response.context["budget_status"]
        self.assertEqual(len(status), 1)
        self.assertEqual(status[0]["limit_amount"], Decimal("500.00"))
        self.assertEqual(status[0]["spent_amount"], Decimal("0.00"))
        self.assertEqual(status[0]["remaining_amount"], Decimal("500.00"))

    def test_budget_status_reflects_partial_spending(self):
        today = datetime.date.today()
        make_expense(self.user, self.cat, amount="200.00", date=today)
        response = self.client.get(self.url)
        status = response.context["budget_status"]
        self.assertEqual(status[0]["spent_amount"], Decimal("200.00"))
        self.assertEqual(status[0]["remaining_amount"], Decimal("300.00"))
        self.assertEqual(status[0]["percent_used"], Decimal("40.0"))

    def test_monthly_url_works(self):
        url = reverse("sheets:budget_dashboard_monthly",
                      kwargs={"year": 2024, "month": 6})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_empty_budget_returns_empty_status(self):
        BudgetLimit.objects.all().delete()
        response = self.client.get(self.url)
        self.assertEqual(response.context["budget_status"], [])


# ---------------------------------------------------------------------------
# register_view
# ---------------------------------------------------------------------------

class RegisterViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("sheets:register")

    def test_get_returns_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_uses_register_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "registration/register.html")

    def test_valid_registration_creates_user(self):
        data = {
            "username": "newuser",
            "password1": "Str0ng@Pass99",
            "password2": "Str0ng@Pass99",
        }
        self.client.post(self.url, data)
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_valid_registration_logs_user_in(self):
        data = {
            "username": "autouser",
            "password1": "Str0ng@Pass99",
            "password2": "Str0ng@Pass99",
        }
        response = self.client.post(self.url, data)
        # After registration user should be authenticated (session set)
        user = User.objects.get(username="autouser")
        self.assertIn("_auth_user_id", self.client.session)

    def test_duplicate_username_does_not_create_second_user(self):
        make_user("existinguser", "Pass1234!")
        data = {
            "username": "existinguser",
            "password1": "Str0ng@Pass99",
            "password2": "Str0ng@Pass99",
        }
        self.client.post(self.url, data)
        self.assertEqual(User.objects.filter(username="existinguser").count(), 1)

    def test_mismatched_passwords_returns_form_errors(self):
        data = {
            "username": "baduser",
            "password1": "Str0ng@Pass99",
            "password2": "WrongPass99!",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="baduser").exists())
