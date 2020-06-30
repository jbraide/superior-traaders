from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth import login as auth_login


from django.contrib.auth.decorators import login_required

from .forms import RegistrationForm, LoginForm


def index(request):
    return render(request, 'main/index.html')

@login_required(login_url='/login')
def dashboard(request):
    return render(request, 'main/dashboard.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        print('I passed test 1')
        if form.is_valid():
            user = form.save()
            print('I passed test 2')
            
            user.refresh_from_db()
            print('I passed test 3')

            # save form data to profile forms
            user.profile.first_name = form.cleaned_data.get('first_name')
            user.profile.last_name = form.cleaned_data.get('last_name')
            user.profile.email = form.cleaned_data.get('email')
            user.save()

            # auto login
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user_login = authenticate(request,username=username, password=password)
            auth_login(request, user_login)
            print('I did get here')
            return redirect('main:dashboard')
        else:
            print('Something went wrong')
            print(form.errors)


    else:
        form = RegistrationForm()
    context = {
        'form': form
    }
    return render(request, 'main/register.html', context)

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            authenticated = authenticate(request,username=username,password=password)
            auth_login(request, authenticated)
            return redirect('main:dashboard')
        else:
            print(form.errors)
    else: 
        form = LoginForm()
    context = {
        'form': form
    }
    return render(request, 'main/login.html', context)

def logout_view(request):
    logout(request)
    return redirect('main:index')


def account(request):
    return render(request, 'main/account.html')