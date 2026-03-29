from django import forms
from django.contrib.auth import get_user_model
from .models import Employee

User = get_user_model()


ROLE_CHOICES = (
    ("ADMIN", "Admin"),
    ("MANAGER", "Manager"),
    ("CASHIER", "Cashier"),
)


class EmployeeCreateForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Employee email"
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Password"
        })
    )

    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.Select(attrs={
            "class": "form-control"
        })
    )

    employee_code = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Employee code"
        })
    )

    phone = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Phone number"
        })
    )

    address = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "placeholder": "Address",
            "rows": 3
        })
    )

    salary = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        initial=0,
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "placeholder": "Salary"
        })
    )

    hire_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            "class": "form-control",
            "type": "date"
        })
    )

    def __init__(self, *args, **kwargs):
        self.client = kwargs.pop("client", None)
        super().__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email

    def clean_employee_code(self):
        code = self.cleaned_data["employee_code"].strip()
        if Employee.objects.filter(employee_code=code).exists():
            raise forms.ValidationError("This employee code already exists.")
        return code

    def clean_phone(self):
        return self.cleaned_data.get("phone", "").strip()

    def clean_address(self):
        return self.cleaned_data.get("address", "").strip()


class EmployeeUpdateForm(forms.ModelForm):
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.Select(attrs={
            "class": "form-control"
        })
    )

    class Meta:
        model = Employee
        fields = [
            "employee_code",
            "phone",
            "address",
            "salary",
            "hire_date",
            "is_active",
        ]
        widgets = {
            "employee_code": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Employee code"
            }),
            "phone": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Phone number"
            }),
            "address": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Address"
            }),
            "salary": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Salary"
            }),
            "hire_date": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date"
            }),
            "is_active": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),
        }

    def __init__(self, *args, **kwargs):
        self.user_instance = kwargs.pop("user_instance", None)
        super().__init__(*args, **kwargs)

        if self.user_instance:
            self.fields["role"].initial = self.user_instance.role

    def clean_employee_code(self):
        code = self.cleaned_data["employee_code"].strip()
        qs = Employee.objects.filter(employee_code=code)

        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise forms.ValidationError("This employee code already exists.")

        return code

    def clean_phone(self):
        return self.cleaned_data.get("phone", "").strip()

    def clean_address(self):
        return self.cleaned_data.get("address", "").strip()