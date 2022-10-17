from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.models import User
from django.utils.text import gettext_lazy as _

class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=101)
    last_name = forms.CharField(max_length=101)
    email = forms.EmailField()
    class Meta:
        model = User
        fields = [ 'first_name', 'last_name','email','password1','password2']
class LoginForm(AuthenticationForm):
    email = forms.CharField(label='Email Address ')
    

# class UserLoginAuthenticationForm(AuthenticationForm):
#     error_messages = {
#         "invalid_login": _(
#             "Please enter a correct email and password. Note that both "
#             "fields may be case-sensitive."
#         ),
#         "inactive": _("This account is inactive."),
#     }