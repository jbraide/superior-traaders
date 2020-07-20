from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth import login as auth_login


from django.contrib.auth.decorators import login_required

from .forms import RegistrationForm, LoginForm, DepositForm, ProfileForm

# models
from .models import Balance, Signals, AccountType, InvestedAmount
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
    signals_amount = Signals.objects.filter(user=user).aggregate(amount=Sum('amount'))
    invested = InvestedAmount.objects.filter(user=user).aggregate(amount=Sum('amount'))
    type = AccountType.objects.filter(user=user)

    # greeting 
    now  = datetime.datetime.now()
    current_time = now.strftime("%H:%M")
    

    if current_time < '11:59':
        greeting = 'Good Morning'

    elif current_time < '17:59':
        greeting = 'Good Afternoon'

    else:
        greeting = 'Good Evening'


    context = {
        'balance': balance, 
        'greeting': greeting, 
        'signals': signals_amount, 
        'invested': invested, 
        'type': type
    }
    return render(request, 'main/dashboard.html', context)

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        picture = ProfileForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if form.is_valid() and picture.is_valid:
            user = form.save()
            
            user.refresh_from_db()

            # save form data to profile forms
            user.profile.first_name = form.cleaned_data.get('first_name')
            user.profile.last_name = form.cleaned_data.get('last_name')
            user.profile.email = form.cleaned_data.get('email')

            # id = user.id
            # print(id)
            # user.profile.profile_picture = picture.cleaned_data['profile_picture']
            picture.save()
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
        picture = ProfileForm()
    context = {
        'form': form, 
        'picture': picture
    }
    return render(request, 'main/register.html', context)

# def login(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             authenticated = authenticate(request,username=username,password=password)
#             auth_login(request, authenticated)
#             return redirect('main:dashboard')
#         else:
#             print(form.errors)
#     else: 
#         form = LoginForm()
#     context = {
#         'form': form
#     }
#     return render(request, 'main/login.html', context)


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


from django.contrib import messages
# Deposit function 
def deposit(request):
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            form.save
            messages.error(request,'Deposit error Contact admin at support@superior-traders.com')
            return redirect('main:dashboard')

        else: 
            errors = form.errors
            print(errors)


    else:
        form = DepositForm()

    context = {
        'form': form
    }
    return render(request, 'main/deposit.html', context)