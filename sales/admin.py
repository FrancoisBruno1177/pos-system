from django.contrib import admin
from .models import Sale, SaleItem


class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 0
    readonly_fields = ("product_name", "quantity", "unit_price", "line_total")


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "cashier",
        "customer_name",
        "payment_method",
        "total_amount",
        "created_at",
    )
    search_fields = ("id", "customer_name", "cashier__email")
    list_filter = ("payment_method", "created_at")
    inlines = [SaleItemInline]


@admin.register(SaleItem)
class SaleItemAdmin(admin.ModelAdmin):
    list_display = ("sale", "product_name", "quantity", "unit_price", "line_total")
    search_fields = ("product_name",)