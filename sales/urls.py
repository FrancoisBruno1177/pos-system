from django.urls import path
from . import views

urlpatterns=[

path("pos/",views.pos_page),

path("dashboard/",views.sales_dashboard),

path("receipt/<int:id>/",views.receipt),

]
