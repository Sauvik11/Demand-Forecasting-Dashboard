from django.contrib import admin
from django.urls import path
from . import views
from accounts.views import LoginView, RegisterView,logoutPage


urlpatterns = [
    path('', views.ForecastDashboardView.as_view(), name='index'),
    path('login', LoginView.as_view(), name='login'),
    # print ("after login"),
    path('logout', logoutPage, name='logout'),
]