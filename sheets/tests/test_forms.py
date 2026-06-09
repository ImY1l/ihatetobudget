import pytest

from django.contrib.auth.models import User

from sheets.forms import BudgetLimitForm, CustomUserCreationForm
from sheets.models import BudgetLimit, Category


@pytest.mark.django_db
def test_custom_user_creation_form_valid():
    form = CustomUserCreationForm(
        data={
            "username": "alice",
            "email": "alice@example.com",
            "password1": "complex-pass-123",
            "password2": "complex-pass-123",
        }
    )
    assert form.is_valid()
    user = form.save()
    assert isinstance(user, User)
    assert user.email == "alice@example.com"


@pytest.mark.django_db
def test_custom_user_creation_form_rejects_password_mismatch():
    form = CustomUserCreationForm(
        data={
            "username": "alice",
            "email": "alice@example.com",
            "password1": "complex-pass-123",
            "password2": "different-pass-123",
        }
    )
    assert not form.is_valid()


@pytest.mark.django_db
def test_custom_user_creation_form_rejects_duplicate_username():
    User.objects.create_user(username="alice", password="something")

    form = CustomUserCreationForm(
        data={
            "username": "alice",
            "email": "new@example.com",
            "password1": "complex-pass-123",
            "password2": "complex-pass-123",
        }
    )
    assert not form.is_valid()


@pytest.mark.django_db
def test_budgetlimit_form_valid():
    user = User.objects.create_user(username="u", password="p")
    c = Category.objects.create(name="Food", color="#ff0000")

    form = BudgetLimitForm(
        data={
            "category": c.id,
            "limit_amount": "123.45",
            "month": 1,
            "year": 2024,
        }
    )
    assert form.is_valid()


@pytest.mark.django_db
def test_budgetlimit_form_rejects_missing_required_fields():
    form = BudgetLimitForm(data={})
    assert not form.is_valid()


@pytest.mark.django_db
def test_budgetlimit_form_rejects_invalid_month_type_range():
    c = Category.objects.create(name="Food", color="#ff0000")

    form = BudgetLimitForm(
        data={
            "category": c.id,
            "limit_amount": "10.00",
            "month": "not-a-number",
            "year": 2024,
        }
    )
    assert not form.is_valid()


@pytest.mark.django_db
def test_budgetlimit_form_accepts_edge_month_values_as_int():
    # Model uses IntegerField without validation; ensure we cover acceptance.
    c = Category.objects.create(name="Food", color="#ff0000")

    for month in [0, 13]:
        form = BudgetLimitForm(
            data={
                "category": c.id,
                "limit_amount": "10.00",
                "month": month,
                "year": 2024,
            }
        )
        assert form.is_valid()

