from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.forms import AuthenticationForm
from .forms import SignupForm, CustomAuthenticationForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView

# Create your views here.

def login_view(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = CustomAuthenticationForm(request, data=request.POST) 
            if form.is_valid():
                # username = form.cleaned_data.get('username')
                # password = form.cleaned_data.get('password')
                # 
                user = form.get_user()
                if user is not None:
                    login(request,user)
                    return redirect('/')
        else:
            form = CustomAuthenticationForm(request)

        context = {'form': form}
        return render(request,'accounts/login.html',context)
    else:
        return redirect('/')



@login_required
def logout_view(request):
    logout(request)
    return redirect('/')



def signup_view(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = SignupForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('/')
        else:
            form = SignupForm()

        context = {'form': form}
        return render(request,'accounts/signup.html', context)
    else:
            return redirect('/')
        
        
class CustomPasswordResetView(PasswordResetView):
    template_name = 'accounts/forget-password.html'
    email_template_name = 'accounts/reset-password-email.html'
    success_url = reverse_lazy('accounts:password_reset_done')
    
