import calendar
import datetime
import statistics
from collections import defaultdict
from django.contrib.auth import login as auth_login
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Avg, Q, Sum
from django.db.models.functions import TruncMonth
from django.shortcuts import render
from decimal import Decimal
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.dates import MonthArchiveView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from ihatetobudget.utils.views import (
    InitialDataAsGETOptionsMixin,
    SortableListViewMixin,
    SuccessMessageOnDeleteViewMixin,
)

import csv
import io
import zipfile

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .forms import BudgetLimitForm, CategoryForm, CustomUserCreationForm, ExpenseForm
from .models import BudgetLimit, Category, Expense


def register_view(request):
    form = CustomUserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        return render(request, "sheets/index.html")


    return render(request, "registration/register.html", {"form": form})


@login_required
def export_csv_view(request):
    import csv
    from django.http import HttpResponse

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="expenses.csv"'

    writer = csv.writer(response)
    writer.writerow(["Date", "Category", "Amount", "Description"])

    qs = Expense.objects.filter(user=request.user).order_by("date")
    for e in qs:
        writer.writerow([e.date, e.category.name if e.category else "", e.amount, e.description])

    return response


@login_required
def index(request):
    # XXX: this whole section can probably be optimized/rewritten.
    # <>
    monthly_insights = defaultdict(lambda: defaultdict(list))

    if years := [e.year for e in Expense.objects.dates("date", "year")]:
        categories = Category.objects.all()
        for year in years:
            for month in range(1, 13):
                for category in [None] + list(categories):
                    monthly_insights[year][category].append(
                        Expense.objects.filter(
                            date__year=year,
                            date__month=month,
                            category=category,
                        ).aggregate(Sum("amount"))["amount__sum"]
                        or 0
                    )

        # Django templates don't work well with defaultdicts
        monthly_insights.default_factory = None
        for category_dict in monthly_insights.values():
            category_dict.default_factory = None
    # </>

    first_day_of_current_month = datetime.datetime.today().replace(day=1)

    return render(
        request,
        "sheets/index.html",
        dict(
            title="Overview",
            monthly_average_spend=(
                x
                if (
                    x := Expense.objects.filter(
                        date__lt=first_day_of_current_month
                    )
                    .annotate(period=TruncMonth("date"))
                    .values("period")
                    .annotate(amount__sum=Sum("amount"))
                    .aggregate(Avg("amount__sum"))["amount__sum__avg"]
                )
                else 0
            ),
            median_spend=(
                statistics.median(e.amount for e in x)
                if (x := Expense.objects.all())
                else 0
            ),
            monthly_insights_dict=monthly_insights,
            # Currency related
            currency_group_separator=settings.CURRENCY_GROUP_SEPARATOR,
            currency_decimal_separator=settings.CURRENCY_DECIMAL_SEPARATOR,
            currency_prefix=settings.CURRENCY_PREFIX,
            currency_suffix=settings.CURRENCY_SUFFIX,
        ),
    )


class SheetView(LoginRequiredMixin, MonthArchiveView):
    template_name = "sheets/sheet.html"
    queryset = Expense.objects.all()
    date_field = "date"
    allow_future = True

    def get_queryset(self):
        # Ensure the month page shows only the logged-in user's uploaded expenses
        # while keeping MonthArchiveView's month/year filtering behavior.
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = datetime.datetime.today()
        month = context["month"]
        if today.month == month.month and today.year == month.year:
            context["days_left"] = (
                calendar.monthrange(year=today.year, month=today.month)[1]
                - today.day
            ) + 1
        return context


class ExpenseCreateView(
    LoginRequiredMixin,
    InitialDataAsGETOptionsMixin,
    SuccessMessageMixin,
    CreateView,
):
    template_name = "ihatetobudget/generic/new-edit-form.html"
    form_class = ExpenseForm
    extra_context = {"title": "New Expense"}

    # After adding an expense, redirect back to the overview page.
    success_url = reverse_lazy("sheets:index")



    # InitialDataAsGETOptionsMixin
    fields_with_initial_data_as_get_option = {
        "category": lambda option_value: Category.objects.get(
            name=option_value
        ),
        "date": None,
        "description": None,
        "amount": None,
        "repeat_next_month": lambda option_value: option_value == "True",
    }

    # SuccessMessageMixin
    success_message = "Expense added!"


class ExpenseUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = "ihatetobudget/generic/new-edit-form.html"
    model = Expense
    form_class = ExpenseForm
    extra_context = {"title": "Edit Expense"}

    # SuccessMessageMixin
    success_message = "Expense modified!"


class ExpenseDeleteView(
    LoginRequiredMixin, SuccessMessageOnDeleteViewMixin, DeleteView
):
    #  XXX: a `template_name` must be defined if we want to delete via GET.
    #  Currently, we delete via POST (no need to render a template, since we
    #  redirect).

    model = Expense
    success_url = reverse_lazy("sheets:index")

    # SuccessMessageMixin
    success_message = "Expense deleted!"

    def get_success_url(self):
        object = self.object
        # XXX: this can probably be optimized
        if similar_object := (
            self.model.objects.exclude(pk=object.pk)
            .filter(date__year=object.date.year, date__month=object.date.month)
            .first()
        ):
            #  There's a least one other object with the same year and month
            return similar_object.get_absolute_url()
        return super().get_success_url()


class ExpenseListView(LoginRequiredMixin, SortableListViewMixin, ListView):
    template_name = "sheets/history.html"
    paginate_by = 50
    model = Expense
    ordering = ["-date"]
    extra_context = {"title": "Expense History"}

    # SortableListViewMixin
    sortable_fields = ["date", "category", "amount"]

    def get_queryset(self):
        queryset = super().get_queryset()
        if query := self.request.GET.get("q"):
            return queryset.filter(
                Q(date__icontains=query)
                | Q(category__name__icontains=query)
                | Q(amount__icontains=query)
                | Q(description__icontains=query)
            )
        return queryset


class CategoryListView(LoginRequiredMixin, ListView):
    template_name = "sheets/categories.html"
    model = Category
    extra_context = {"title": "Categories"}


class CategoryCreateView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    CreateView,
):
    template_name = "ihatetobudget/generic/new-edit-form.html"
    form_class = CategoryForm
    extra_context = {"title": "New Category"}

    # SuccessMessageMixin
    success_message = "Category added!"


class CategoryUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = "ihatetobudget/generic/new-edit-form.html"
    model = Category
    form_class = CategoryForm
    extra_context = {"title": "Edit Category"}

    # SuccessMessageMixin
    success_message = "Category modified!"


class CategoryDeleteView(
    LoginRequiredMixin, SuccessMessageOnDeleteViewMixin, DeleteView
):
    template_name = "ihatetobudget/generic/delete-form.html"
    model = Category
    extra_context = {"title": "Delete Category"}
    success_url = reverse_lazy("sheets:categories")

    # SuccessMessageMixin
    success_message = "Category deleted!"


@login_required
def receipts_month_view(request, year: int, month: int):
    if not request.user.is_authenticated:
        # login_required decorator covers this in routing, but keep it safe
        return render(request, "404.html", status=404)

    qs = Expense.objects.filter(user=request.user, date__year=year, date__month=month)
    receipts = [e for e in qs if e.receipt]
    receipts_count = len(receipts)

    # If receipts exist, show them. If none, still show empty state.
    return render(
        request,
        "sheets/receipts_month.html",
        {
            "title": "Receipts",
            "year": year,
            "month": month,
            "receipts": receipts,
            "receipts_count": receipts_count,
        },
    )


def receipts_month_download_view(request, year: int, month: int):
    from django.http import FileResponse, Http404, HttpResponse

    # Only logged-in users can reach this route (via urls.py usage with views here).
    qs = Expense.objects.filter(user=request.user, date__year=year, date__month=month)
    receipts = [e.receipt for e in qs if e.receipt]

    if not receipts:
        raise Http404("No receipts found for this month")

    def _filename_from_field(receipt_field):
        # receipt_field.name is the storage key like "receipts/2026/06/abc.pdf"
        # Use the last path segment as the download filename.
        return receipt_field.name.rsplit("/", 1)[-1] if receipt_field.name else "receipt"

    if len(receipts) == 1:
        receipt_field = receipts[0]
        return FileResponse(
            receipt_field.open("rb"),
            as_attachment=True,
            filename=_filename_from_field(receipt_field),
        )

    # Multiple: zip them.
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for receipt_field in receipts:
            f = receipt_field.open("rb")
            try:
                zf.writestr(_filename_from_field(receipt_field), f.read())
            finally:
                f.close()

    buffer.seek(0)
    filename = f"receipts_{year}_{month:02d}.zip"
    resp = HttpResponse(buffer.getvalue(), content_type="application/zip")
    resp["Content-Disposition"] = f"attachment; filename={filename}"
    return resp


@login_required
def receipt_download_view(request, pk: int):
    from django.http import FileResponse, Http404

    expense = Expense.objects.filter(pk=pk, user=request.user).first()
    if not expense or not expense.receipt:
        raise Http404("Receipt not available")

    receipt_field = expense.receipt
    filename = receipt_field.name.rsplit("/", 1)[-1] if receipt_field.name else "receipt"
    return FileResponse(
        receipt_field.open("rb"),
        as_attachment=True,
        filename=filename,
    )


@login_required
def budget_dashboard(request, year=None, month=None):
    today = datetime.date.today()
    year = year or today.year
    month = month or today.month

    # Only show budgets configured by this user.
    budgets = BudgetLimit.objects.filter(
        user=request.user,
        year=year,
        month=month,
    ).select_related("category")

    # Compute spent per category in one query.
    spent_by_category = (
        Expense.objects.filter(
            user=request.user,
            date__year=year,
            date__month=month,
        )
        .values("category")
        .annotate(spent_amount=Sum("amount"))
    )
    spent_map = {
        row["category_id"] if "category_id" in row else row["category"]: row[
            "spent_amount"
        ]
        for row in spent_by_category
    }

    budget_status = []
    for b in budgets:
        spent_amount = spent_map.get(b.category_id, Decimal("0.00"))
        remaining_amount = b.limit_amount - spent_amount
        percent_used = None
        if b.limit_amount and b.limit_amount != 0:
            percent_used = (spent_amount / b.limit_amount) * Decimal("100")

        budget_status.append(
            {
                "category": b.category.name,
                "color": b.category.color,
                "limit_amount": b.limit_amount,
                "spent_amount": spent_amount,
                "remaining_amount": remaining_amount,
                "percent_used": percent_used.quantize(Decimal("0.1"))
                if percent_used is not None
                else None,
            }
        )

    return render(
        request,
        "sheets/budget.html" if "sheets/budget.html" else "sheets/sheet.html",
        {
            "title": "Budget",
            "month": month,
            "year": year,
            "budget_status": budget_status,
        },
    )
