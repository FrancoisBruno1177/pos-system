from datetime import timedelta

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm

from .models import Client, Plan, Subscription

User = get_user_model()


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Email",
            "autocomplete": "email",
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Password",
            "autocomplete": "current-password",
        })
    )


class CreateClientForm(forms.Form):
    name = forms.CharField(max_length=255)
    schema_name = forms.CharField(max_length=63)
    domain = forms.CharField(max_length=255)
    admin_email = forms.EmailField()
    admin_password = forms.CharField(widget=forms.PasswordInput)
    plan = forms.ModelChoiceField(queryset=Plan.objects.all())
    subscription_days = forms.IntegerField(min_value=1, initial=30)

    def clean_admin_email(self):
        email = self.cleaned_data["admin_email"].lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email

    def clean_schema_name(self):
        schema_name = self.cleaned_data["schema_name"].strip().lower()
        if Client.objects.filter(schema_name=schema_name).exists():
            raise forms.ValidationError("This schema name already exists.")
        return schema_name

    def clean_domain(self):
        domain = self.cleaned_data["domain"].strip().lower()
        if Client.objects.filter(domain=domain).exists():
            raise forms.ValidationError("This domain already exists.")
        return domain


class CreateEmployeeForm(forms.Form):
    ROLE_CHOICES = (
        ("MANAGER", "Manager"),
        ("CASHIER", "Cashier"),
    )

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=ROLE_CHOICES)

    def __init__(self, *args, **kwargs):
        self.client = kwargs.pop("client", None)
        super().__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email