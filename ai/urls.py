from django.urls import path
from .views import ai_dashboard
from . import views

urlpatterns=[

path("dashboard/",ai_dashboard),

path('', views.ai_dashboard, name='ai_dashboard'),

]
