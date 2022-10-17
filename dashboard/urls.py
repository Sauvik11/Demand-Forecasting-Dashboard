from django.contrib import admin
from django.urls import path
from . import views
from accounts.views import LoginView,logoutPage


urlpatterns = [
    path('', views.ForecastDashboardView.as_view(), name='index'),
    
    path('signup', LoginView.as_view(), name='signup'),
    
    # print ("after login"),
    
]