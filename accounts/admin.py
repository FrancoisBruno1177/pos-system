from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Client, Plan, Subscription


class UserAdmin(BaseUserAdmin):
    model = User

    list_display = ("email", "role", "client", "is_staff", "is_superuser")
    list_filter = ("role", "is_staff", "is_superuser")

    ordering = ("email",)
    search_fields = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Role & Client", {"fields": ("role", "client")}),
        ("Security", {"fields": ("failed_attempts", "lock_until")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "role", "client", "is_staff", "is_superuser"),
        }),
    )


admin.site.register(User, UserAdmin)
admin.site.register(Client)
admin.site.register(Plan)
admin.site.register(Subscription)

