"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import  include
from billing import views as billing_views
from django.conf.urls.i18n import i18n_patterns

from django.conf import settings
from django.conf.urls.static import static
from accounts import views
from accounts import views as accounts_views



urlpatterns = [
    path("admin/", admin.site.urls),

    path("myip/", views.my_ip, name="my_ip"),

    path("pricing/", billing_views.pricing_page, name="billing_pricing"),

    path("billing/", billing_views.billing_page, name="billing_page"),

    path("",include("accounts.urls")),

    path("inventory/",include("inventory.urls")),

    path("sales/",include("sales.urls")),

    path("ai/",include("ai.urls")),

    path('billing/', include('billing.urls')),

    path('i18n/', include('django.conf.urls.i18n')),

    path("superadmin/", views.superadmin_dashboard, name="superadmin_dashboard"),
    path("admin/", views.admin_dashboard, name="admin_dashboard"),
    path("manager/", views.manager_dashboard, name="manager_dashboard"),
    path("cashier/", views.cashier_dashboard, name="cashier_dashboard"),

    path("create-client/", views.create_client, name="create_client"),
    path("create-employee/", views.create_employee, name="create_employee"),


]

urlpatterns += i18n_patterns(
    path("dashboard/", views.dashboard, name="dashboard"),
    path('', include('accounts.urls')),
)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

