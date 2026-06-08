from django.urls import path

from . import views

app_name = "sheets"
urlpatterns = [
    path("", views.index, name="index"),
    path("register/", views.register_view, name="register"),
    path("export/csv/", views.export_csv_view, name="export_csv"),
    #  Budget
    path("budget/", views.budget_dashboard, name="budget_dashboard"),
    path(
        "budget/<int:year>/<int:month>/",
        views.budget_dashboard,
        name="budget_dashboard_monthly",
    ),
    #  Sheets

    path(
        "<int:year>/<int:month>/",
        views.SheetView.as_view(month_format="%m"),
        name="sheet",
    ),
    path("expense/new/", views.ExpenseCreateView.as_view(), name="expense-new"),
    path(
        "expense/<int:pk>/",
        views.ExpenseUpdateView.as_view(),
        name="expense-edit",
    ),
    path(
        "expense/<int:pk>/delete/",
        views.ExpenseDeleteView.as_view(),
        name="expense-delete",
    ),
    #  History
    path("expense/history/", views.ExpenseListView.as_view(), name="history"),
    #  Categories
    path("categories/", views.CategoryListView.as_view(), name="categories"),
    path(
        "category/new/",
        views.CategoryCreateView.as_view(),
        name="category-new",
    ),
    path(
        "category/<int:pk>/",
        views.CategoryUpdateView.as_view(),
        name="category-edit",
    ),
    path(
        "category/<int:pk>/delete/",
        views.CategoryDeleteView.as_view(),
        name="category-delete",
    ),
]

