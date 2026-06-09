import pytest

from django.contrib.auth.models import User

from sheets.models import BudgetLimit, Category, Expense


@pytest.mark.django_db
def test_category_str_and_absolute_url():
    c = Category.objects.create(name="Food", color="#ff0000")
    assert str(c) == "Food"
    assert c.get_absolute_url().endswith("/categories/")


@pytest.mark.django_db
def test_expense_str_and_get_absolute_url():
    user = User.objects.create_user(username="u", password="p")
    c = Category.objects.create(name="Food", color="#ff0000")
    e = Expense.objects.create(
        user=user,
        category=c,
        date="2010-02-03",
        description="Groceries",
        amount="20.00",
    )
    # Ensure DB returns a real date instance
    e.refresh_from_db()

    assert str(e) == "Groceries"
    url = e.get_absolute_url()
    assert "/2010/2/" in url


@pytest.mark.django_db
def test_budgetlimit_unique_together_constraint():
    user = User.objects.create_user(username="u", password="p")
    c = Category.objects.create(name="Food", color="#ff0000")

    BudgetLimit.objects.create(
        user=user, category=c, limit_amount="100.00", month=1, year=2024
    )

    # Same (user, category, month, year) should fail.
    with pytest.raises(Exception):
        BudgetLimit.objects.create(
            user=user,
            category=c,
            limit_amount="200.00",
            month=1,
            year=2024,
        )


@pytest.mark.django_db
def test_budgetlimit_allows_same_category_different_month_or_year():
    user = User.objects.create_user(username="u", password="p")
    c = Category.objects.create(name="Food", color="#ff0000")

    BudgetLimit.objects.create(
        user=user, category=c, limit_amount="100.00", month=1, year=2024
    )
    BudgetLimit.objects.create(
        user=user, category=c, limit_amount="200.00", month=2, year=2024
    )
    BudgetLimit.objects.create(
        user=user, category=c, limit_amount="300.00", month=1, year=2025
    )

