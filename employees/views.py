from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from .forms import EmployeeCreateForm, EmployeeUpdateForm
from .models import Employee

User = get_user_model()


def admin_required(user):
    return user.is_authenticated and (user.is_superuser or user.role == "ADMIN")


@login_required
def employee_list(request):
    if not admin_required(request.user):
        messages.error(request, "You are not allowed to access this page.")
        return redirect("dashboard")

    employees = (
        Employee.objects
        .select_related("user")
        .filter(user__client=request.user.client)
        .order_by("user__email")
    )

    return render(request, "employees/employee_list.html", {
        "employees": employees
    })


@login_required
@transaction.atomic
def employee_create(request):
    if not admin_required(request.user):
        messages.error(request, "You are not allowed to access this page.")
        return redirect("dashboard")

    if not request.user.client and not request.user.is_superuser:
        messages.error(request, "Your account is not linked to a company.")
        return redirect("dashboard")

    form = EmployeeCreateForm(request.POST or None, client=request.user.client)

    if request.method == "POST" and form.is_valid():
        user = User.objects.create_user(
            email=form.cleaned_data["email"],
            password=form.cleaned_data["password"],
            role=form.cleaned_data["role"],
            client=request.user.client,
            is_active=True,
        )

        Employee.objects.create(
            user=user,
            employee_code=form.cleaned_data["employee_code"],
            phone=form.cleaned_data.get("phone", ""),
            address=form.cleaned_data.get("address", ""),
            salary=form.cleaned_data.get("salary") or 0,
            hire_date=form.cleaned_data.get("hire_date"),
            is_active=True,
        )

        messages.success(request, "Employee created successfully.")
        return redirect("employee_list")

    return render(request, "employees/employee_form.html", {
        "form": form,
        "page_title": "Create Employee"
    })


@login_required
def employee_detail(request, pk):
    if not admin_required(request.user):
        messages.error(request, "You are not allowed to access this page.")
        return redirect("dashboard")

    employee = get_object_or_404(
        Employee.objects.select_related("user"),
        pk=pk,
        user__client=request.user.client
    )

    return render(request, "employees/employee_detail.html", {
        "employee": employee
    })


@login_required
@transaction.atomic
def employee_update(request, pk):
    if not admin_required(request.user):
        messages.error(request, "You are not allowed to access this page.")
        return redirect("dashboard")

    employee = get_object_or_404(
        Employee.objects.select_related("user"),
        pk=pk,
        user__client=request.user.client
    )

    form = EmployeeUpdateForm(
        request.POST or None,
        instance=employee,
        user_instance=employee.user
    )

    if request.method == "POST" and form.is_valid():
        employee = form.save(commit=False)
        employee.save()

        employee.user.role = form.cleaned_data["role"]
        employee.user.save(update_fields=["role"])

        messages.success(request, "Employee updated successfully.")
        return redirect("employee_list")

    return render(request, "employees/employee_form.html", {
        "form": form,
        "page_title": "Edit Employee",
        "employee": employee
    })


@login_required
@transaction.atomic
def employee_delete(request, pk):
    if not admin_required(request.user):
        messages.error(request, "You are not allowed to access this page.")
        return redirect("dashboard")

    employee = get_object_or_404(
        Employee.objects.select_related("user"),
        pk=pk,
        user__client=request.user.client
    )

    if request.method == "POST":
        user = employee.user
        employee.delete()
        user.delete()

        messages.success(request, "Employee deleted successfully.")
        return redirect("employee_list")

    return render(request, "employees/employee_confirm_delete.html", {
        "employee": employee
    })