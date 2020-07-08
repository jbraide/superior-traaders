from django.urls import path
from .views import index, login, logout_view, dashboard, account, register,rules

app_name = 'main'

urlpatterns = [
    path('', index, name="index"),
    path('rules-agreement/', rules, name='rules'),
    path('dashboard/', dashboard, name="dashboard"), 
    path('login/', login, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register, name='register'),
    path('account/', account, name='account')
]
