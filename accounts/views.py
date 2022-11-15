from django.contrib.auth import views as auth_views
from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.contrib import messages
from .forms import LoginForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib import messages
from .forms import UserRegistrationForm
from django.contrib.auth import get_user_model

# from accounts.forms import UserLoginAuthenticationForm
# Create your views here.

def signup (request):
    return render(request,"accounts/sigup.html")

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



# class RegisterView(generic.CreateView):
#     form_class = RegisterForm
#     template_name = 'accounts/assets/templates/register.html'
#     success_url = reverse_lazy('login')


def logoutPage(request):
    logout(request)
    return redirect('/login')

# class LoginView(BaseLoginView):
#     template_name = 'accounts/assets/templates/login.html'
#     redirect_authenticated_user = True
#     form_class = UserLoginAuthenticationForm


def register(request):
    print("in register view")
    if request.method == 'POST':
        print("in post")
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()

            messages.success(request, f'Your account has been created. You can log in now!')    
            return redirect('login')
    else:
        form = UserRegistrationForm()
        print("in get")
    context = {'form': form}
    return render(request, 'accounts/assets/templates/register.html', context)