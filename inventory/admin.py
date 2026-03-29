from django.contrib import admin
from .models import Category, Supplier, Product, StockMovement


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "created_at")
    search_fields = ("name",)
    list_filter = ("is_active",)


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "is_active", "created_at")
    search_fields = ("name", "email", "phone")
    list_filter = ("is_active",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "sku",
        "category",
        "supplier",
        "selling_price",
        "quantity",
        "low_stock_threshold",
        "is_active",
    )
    search_fields = ("name", "sku")
    list_filter = ("is_active", "category", "supplier")


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "movement_type",
        "quantity",
        "previous_quantity",
        "new_quantity",
        "reference",
        "created_by",
        "created_at",
    )
    search_fields = ("product__name", "product__sku", "reference", "note")
    list_filter = ("movement_type", "created_at")