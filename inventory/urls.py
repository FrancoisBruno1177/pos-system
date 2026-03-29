from django.urls import path
from . import views

urlpatterns = [
    path("", views.inventory_dashboard, name="inventory_dashboard"),

    path("products/", views.product_list, name="product_list"),
    path("products/create/", views.product_create, name="product_create"),
    path("products/<int:pk>/", views.product_detail, name="product_detail"),
    path("products/<int:pk>/edit/", views.product_update, name="product_update"),
    path("products/<int:pk>/delete/", views.product_delete, name="product_delete"),
    path("products/<int:pk>/adjust-stock/", views.stock_adjustment_create, name="stock_adjustment_create"),

    path("categories/", views.category_list, name="category_list"),
    path("categories/create/", views.category_create, name="category_create"),
    path("categories/<int:pk>/edit/", views.category_update, name="category_update"),
    path("categories/<int:pk>/delete/", views.category_delete, name="category_delete"),

    path("suppliers/", views.supplier_list, name="supplier_list"),
    path("suppliers/create/", views.supplier_create, name="supplier_create"),
    path("suppliers/<int:pk>/edit/", views.supplier_update, name="supplier_update"),
    path("suppliers/<int:pk>/delete/", views.supplier_delete, name="supplier_delete"),

    path("stock-history/", views.stock_movement_list, name="stock_movement_list"),
]