from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import BudgetLimit, Category, Expense



class ExpenseForm(forms.ModelForm):
    required_css_class = "form-group-required"

    class Meta:
        model = Expense
        fields = "__all__"


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = "__all__"

        widgets = {
            "color": forms.TextInput(
                attrs={
                    "type": "color",
                    "class": "form-control form-control-color",
                }
            )
        }

class BudgetLimitForm(forms.ModelForm):
    class Meta:
        model = BudgetLimit
        fields = ["category", "limit_amount", "month", "year"]


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ("username", "email")

