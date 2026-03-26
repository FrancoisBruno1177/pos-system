from django.urls import path
from . import views 
from .views import pricing_page
from .views import PlanListAPIView, CreateCheckoutAPIView, billing_page

urlpatterns = [

    path("", billing_page),

    path("plans/", PlanListAPIView.as_view()),

    path("checkout/", CreateCheckoutAPIView.as_view()),

     path("", views.billing_page, name="billing_page"),  
             
    path("pricing/", views.pricing_page, name="billing_pricing") 


]
