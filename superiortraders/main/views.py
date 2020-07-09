from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth import login as auth_login


from django.contrib.auth.decorators import login_required

from .forms import RegistrationForm, LoginForm

# models
from .models import Balance
from django.db.models import Sum

# password reset 
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

# time, dateteime
# import time
import datetime


def index(request):
    return render(request, 'main/index.html')

def about(request):
    return render(request, 'main/about.html')

def rules(request):
    return render(request,'main/rules-agreement.html')

@login_required(login_url='/login')
def dashboard(request):
    user = request.user
    balance = Balance.objects.filter(user=user).aggregate(amount=Sum('amount'))
    now  = datetime.datetime.now()

    # fix bug to allow time to change greeting after :59 mins
    time = now.timestamp
    print(time)
    hour = now.hour

    if hour < 11:
        greeting = 'Good Morning'

    elif hour < 17:
        greeting = 'Good Afternoon'

    else:
        greeting = 'Good Evening'

    print(f'{ greeting }')
    context = {
        'balance': balance, 
        'greeting': greeting
    }
    return render(request, 'main/dashboard.html', context)

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            user.refresh_from_db()

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


@login_required(login_url='/login')
def logout_view(request):
    logout(request)
    return redirect('main:index')

@login_required(login_url='/login')
def account(request):
    user = request.user
    balance = Balance.objects.filter(user=user).aggregate(amount=Sum('amount'))
    if request.method == 'POST':
        form = PasswordChangeForm(request.user)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            # messages.success(request, 'Password was successfully changed..')
            return redirect('main:dashboard')
        else:
            print('error in changing the password')
    else:
        form = PasswordChangeForm(request.user)
    context = {
        'balance': balance, 
        'form': form
    }
    return render(request, 'main/account.html', context)