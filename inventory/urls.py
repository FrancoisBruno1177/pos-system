from django.urls import path
from . import views

urlpatterns=[

path("dashboard/",views.inventory_dashboard),

path("products/", views.product_list, name="product_list"),

path("suppliers/", views.supplier_list, name="supplier_list"),

path('', views.inventory_home, name='inventory_home'),

path('products/', views.products, name='products'),

path('suppliers/', views.suppliers, name='suppliers'),

path('products/delete/<int:id>/', views.delete_product, name='delete_product'),

]
