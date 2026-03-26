from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns=[   

path("login/", views.login_view, name="login"),

path("dashboard/", views.dashboard, name="dashboard"),

path('dashboard/cashier/', views.cashier_dashboard),

path('dashboard/manager/', views.manager_dashboard),

path('dashboard/admin/', views.admin_dashboard),

path('dashboard/superadmin/', views.superadmin_dashboard),

path('logout/', views.logout_view, name='logout'),

path("create-client/", views.create_client, name="create_client"),

path("create-employee/", views.create_employee, name="create_employee"),

path(
"password_reset/",
auth_views.PasswordResetView.as_view(),
name="password_reset"
),

path(
"password_reset/done/",
auth_views.PasswordResetDoneView.as_view(),
name="password_reset_done"
),

path(
"reset/<uidb64>/<token>/",
auth_views.PasswordResetConfirmView.as_view(),
name="password_reset_confirm"
),

path(
"reset/done/",
auth_views.PasswordResetCompleteView.as_view(),
name="password_reset_complete"
),


]
