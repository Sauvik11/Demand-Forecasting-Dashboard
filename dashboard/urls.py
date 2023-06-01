from django.contrib import admin
from django.urls import path
from . import views

from accounts.views import LoginView,logoutPage



urlpatterns = [
    path('', views.ForecastDashboardView.as_view(), name='index'),
    # path('onload/', views.ForecastDashboardView.as_view(), name='onload'),
    path('weather/', views.WeatherPostView.as_view(), name='weatherchart'),
    path('weather2/', views.Weather2PostView.as_view(), name='weatherchart2'),
    path('weather3/', views.Weather3PostView.as_view(), name='weatherchart3'),
    path('preview/', views.ForecastDashboardView.as_view(), name='operations'),
    path('signup', LoginView.as_view(), name='signup'),
    
    # print ("after login"),
    
]