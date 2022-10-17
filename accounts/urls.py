from django.contrib.auth.views import (
    PasswordResetCompleteView, PasswordChangeView, PasswordChangeDoneView,
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, LogoutView
)
from django.urls import path, include, reverse_lazy

from accounts import views

app_name = 'accounts'

urlpatterns = [ 
     path('login/', views.LoginView.as_view(), name='login'),
   path('logout/', LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
     path('register/', views.registerPage, name="register"),
     path('password_change/', PasswordChangeView.as_view(success_url=reverse_lazy("accounts:password_change_done")),
          name="password_change"),
     path('password_change_done/', PasswordChangeDoneView.as_view(), name="password_change_done"),
     path('password_reset/', PasswordResetView.as_view(success_url=reverse_lazy("accounts:password_reset_done")),
          name="password_reset"),
     path('password_reset_done/', PasswordResetDoneView.as_view(), name="password_reset_done"),
     path('password_reset_confirm/<uidb64>/<token>/',
          PasswordResetConfirmView.as_view(success_url=reverse_lazy("accounts:password_reset_complete")),
          name="password_reset_confirm"),
     path('password_reset_complete/', PasswordResetCompleteView.as_view(), name="password_reset_complete"),
 ]