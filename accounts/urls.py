from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_view, name="login"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    path("dashboard/", views.dashboard, name="dashboard"),
    path("dashboard/cashier/", views.cashier_dashboard, name="cashier_dashboard"),
    path("dashboard/manager/", views.manager_dashboard, name="manager_dashboard"),
    path("dashboard/admin/", views.admin_dashboard, name="admin_dashboard"),
    path("dashboard/superadmin/", views.superadmin_dashboard, name="superadmin_dashboard"),

    path("clients/create/", views.create_client, name="create_client"),
    path("my-ip/", views.my_ip, name="my_ip"),
]