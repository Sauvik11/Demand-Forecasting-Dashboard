from django.contrib.auth import views as auth_views
from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from .forms import LoginForm, RegisterForm
from django.contrib.auth import login, logout, authenticate

# Create your views here.


class LoginView(auth_views.LoginView):
    print("in login view")
    form_class = LoginForm
    template_name = 'accounts/assets/templates/login.html'

    # form_class = LoginForm
    def get(self, request):
        if request.user.is_authenticated:
            print("in if........")
            return redirect('/')
        else:
            if request.method == "POST":
                username = request.POST.get('username')
                password = request.POST.get('password')
                user = authenticate(request, username=username, password=password)
                
                print("user is ........",user)
                if user is not None:
                    login(request, user)
                    return redirect('accounts/candidateintro.html')
                    # return redirect('accounts/starttest.html')
                

            return render(request, 'accounts/assets/templates/login.html')



class RegisterView(generic.CreateView):
    form_class = RegisterForm
    template_name = 'accounts/assets/templates/register.html'
    success_url = reverse_lazy('login')


def logoutPage(request):
    logout(request)
    return redirect('/login')
