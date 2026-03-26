from django.urls import path
from .views import SaaSDashboardAPIView

urlpatterns = [
    path("dashboard/", SaaSDashboardAPIView.as_view()),
]