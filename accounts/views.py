from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth import logout
from django.contrib.admin.views.decorators import staff_member_required
from .models import Client, User, Plan, Subscription
from django.http import HttpResponse






@ensure_csrf_cookie
def login_view(request):

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)

            if user.is_locked():
                messages.error(request, "Account locked .")
                return redirect("login")

            user_auth = authenticate(request, username=email, password=password)

            if user_auth:
                user.reset_attempts()
                login(request, user_auth)
                return redirect("dashboard")
            else:
                user.register_failed_attempt()
                messages.error(request, "Invalid credentials.")

        except User.DoesNotExist:
            messages.error(request, "Invalid credentials.")

    return render(request, "accounts/login.html")



@login_required
def dashboard(request):

    user = request.user

   
    if user.is_superuser:
        return render(request, "dashboards/superadmin.html")

   
    if user.role == "ADMIN":
        return render(request, "dashboards/admin.html")

    elif user.role == "MANAGER":
        return render(request, "dashboards/manager.html")

    elif user.role == "CASHIER":
        return render(request, "dashboards/cashier.html")

    
    return render(request, "dashboards/cashier.html")



@login_required
def cashier_dashboard(request):
    return render(request, "dashboards/cashier.html")

@login_required
def manager_dashboard(request):
    return render(request, "dashboards/manager.html")


@login_required
def admin_dashboard(request):
    return render(request, "dashboards/admin.html")


@login_required
def superadmin_dashboard(request):
    return render(request, "dashboards/superadmin.html")    


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def create_client(request):
    if not request.user.is_superuser:
        return redirect("dashboard")

    if request.method == "POST":
        name = request.POST.get("name")
        schema_name = request.POST.get("schema_name")
        domain = request.POST.get("domain")
        admin_email = request.POST.get("admin_email")
        admin_password = request.POST.get("admin_password")
        plan_id = request.POST.get("plan")

        # Create client
        client = Client.objects.create(
            name=name,
            schema_name=schema_name,
            domain=domain
        )

        # Create admin for this client
        User.objects.create_user(
            username=admin_email,
            email=admin_email,
            password=admin_password,
            role="ADMIN",
            client=client
        )

        # Assign plan
        plan = Plan.objects.get(id=plan_id)
        Subscription.objects.create(
            client=client,
            plan=plan,
            active=True
        )

        return redirect("dashboard")

    plans = Plan.objects.all()
    return render(request, "superadmin/create_client.html", {"plans": plans})


# ================= ADMIN =================

@login_required
def create_employee(request):
    if request.user.role != "ADMIN":
        return redirect("dashboard")

    if not can_create_user(request.user.client):
        return render(request, "error.html", {
            "message": "User limit reached for your plan"
        })

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        role = request.POST.get("role")

        User.objects.create_user(
            username=email,
            email=email,
            password=password,
            role=role,
            client=request.user.client
        )

        return redirect("dashboard")

    return render(request, "accounts/create_employee.html")


# ================= LIMIT LOGIC =================

def can_create_user(client):
    subscription = Subscription.objects.filter(client=client, active=True).first()

    if not subscription:
        return False

    max_users = subscription.plan.max_users
    current_users = User.objects.filter(client=client).count()

    return current_users < max_users   



def my_ip(request):
    ip = request.META.get('REMOTE_ADDR')
    return HttpResponse(f"Your IP is: {ip}")


