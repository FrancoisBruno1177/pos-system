from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect


def root_redirect(request):
    return redirect("login")


urlpatterns = [
    path("admin/", admin.site.urls),

    path("", root_redirect, name="root"),

    path("", include("accounts.urls")),
    path("employees/", include("employees.urls")),
    path("inventory/", include("inventory.urls")),
    path("sales/", include("sales.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)