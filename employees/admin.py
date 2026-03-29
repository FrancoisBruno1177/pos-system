from django.contrib import admin
from .models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        "employee_code",
        "user",
        "get_role",
        "phone",
        "salary",
        "hire_date",
        "is_active",
    )
    search_fields = ("employee_code", "user__email", "phone")
    list_filter = ("is_active", "hire_date", "user__role")

    def get_role(self, obj):
        return obj.user.role
    get_role.short_description = "Role"