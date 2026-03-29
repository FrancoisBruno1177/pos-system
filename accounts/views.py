from datetime import timedelta

from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.csrf import ensure_csrf_cookie

from .forms import CreateClientForm, LoginForm
from .models import Client, Subscription
from employees.models import Employee
from inventory.models import Product, Category, Supplier
from sales.models import Sale

User = get_user_model()


def redirect_dashboard_by_role(user):
    if user.is_superuser or user.role == "SUPER_ADMIN":
        return "superadmin_dashboard"
    if user.role == "ADMIN":
        return "admin_dashboard"
    if user.role == "MANAGER":
        return "manager_dashboard"
    return "cashier_dashboard"


def is_super_admin(user):
    return user.is_authenticated and (user.is_superuser or user.role == "SUPER_ADMIN")


@ensure_csrf_cookie
def login_view(request):
    if request.user.is_authenticated:
        return redirect(redirect_dashboard_by_role(request.user))

    form = LoginForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            email = form.cleaned_data["email"].strip().lower()
            password = form.cleaned_data["password"]

            try:
                user = User.objects.get(email=email)

                if user.is_locked():
                    messages.error(request, "Your account is locked. Try again later.")
                    return render(request, "accounts/login.html", {"form": form})

                authenticated_user = authenticate(
                    request,
                    username=email,
                    password=password,
                )

                if authenticated_user is not None:
                    user.reset_attempts()
                    login(request, authenticated_user)
                    messages.success(request, "Login successful.")
                    return redirect(redirect_dashboard_by_role(authenticated_user))

                user.register_failed_attempt()
                messages.error(request, "Invalid email or password.")

            except User.DoesNotExist:
                messages.error(request, "No account found with this email address.")
        else:
            messages.error(request, "Please correct the form errors below.")

    return render(request, "accounts/login.html", {"form": form})


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("login")


@login_required
def dashboard(request):
    return redirect(redirect_dashboard_by_role(request.user))


@login_required
def manager_dashboard(request):
    context = {
        "total_sales": Sale.objects.count(),
        "total_products": Product.objects.count(),
        "low_stock_count": Product.objects.filter(quantity__lte=5).count(),
    }
    return render(request, "dashboards/manager.html", context)


@login_required
def cashier_dashboard(request):
    return redirect("sales_cashier_dashboard")


@login_required
def admin_dashboard(request):
    employees = Employee.objects.select_related("user").all()
    products = Product.objects.all()
    sales = Sale.objects.all()
    categories = Category.objects.all()
    suppliers = Supplier.objects.all()

    context = {
        "total_employees": employees.count(),
        "total_products": products.count(),
        "total_sales": sales.count(),
        "total_categories": categories.count(),
        "total_suppliers": suppliers.count(),
        "low_stock_count": products.filter(quantity__lte=5).count(),
        "recent_products": products.order_by("-id")[:5],
        "recent_sales": sales.order_by("-id")[:5],
    }
    return render(request, "dashboards/admin.html", context)


@login_required
def superadmin_dashboard(request):
    context = {
        "total_clients": Client.objects.count(),
        "active_subscriptions": Subscription.objects.filter(active=True).count(),
        "total_users": User.objects.count(),
    }
    return render(request, "dashboards/superadmin.html", context)


@login_required
@user_passes_test(is_super_admin)
def create_client(request):
    form = CreateClientForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        client = Client.objects.create(
            name=form.cleaned_data["name"],
            schema_name=form.cleaned_data["schema_name"],
            domain=form.cleaned_data["domain"],
            is_active=True,
        )

        User.objects.create_user(
            email=form.cleaned_data["admin_email"],
            password=form.cleaned_data["admin_password"],
            role="ADMIN",
            client=client,
            is_staff=True,
            is_active=True,
        )

        subscription_days = form.cleaned_data["subscription_days"]

        Subscription.objects.create(
            client=client,
            plan=form.cleaned_data["plan"],
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=subscription_days),
            active=True,
        )

        messages.success(request, "Client created successfully.")
        return redirect("superadmin_dashboard")

    return render(request, "accounts/create_client.html", {"form": form})


def my_ip(request):
    ip = request.META.get("REMOTE_ADDR", "Unknown")
    return HttpResponse(f"Your IP is: {ip}")