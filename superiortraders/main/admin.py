from django.contrib import admin
from .models import Profile, Balance, Deposit

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['first_name', ]

@admin.register(Balance)
class BalanceAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount']

@admin.register(Deposit)
class DepositAdmin(admin.ModelAdmin):
    list_display = ['amount',]

