from django.urls import path
from . import views

urlpatterns = [
    path("cashier/", views.cashier_dashboard, name="sales_cashier_dashboard"),
    path("pos/", views.pos_view, name="pos_view"),
    path("create/", views.create_sale, name="create_sale"),
    path("", views.sale_list, name="sale_list"),
    path("<int:pk>/", views.sale_detail, name="sale_detail"),
    path("<int:pk>/receipt/", views.sale_receipt, name="sale_receipt"),
]