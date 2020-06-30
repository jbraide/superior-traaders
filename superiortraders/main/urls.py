from django.urls import path
from .views import index, login, logout_view, dashboard, account, register

app_name = 'main'

urlpatterns = [
    path('', index, name="index"), 
    path('dashboard/', dashboard, name="dashboard"), 
    path('login/', login, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register, name='register'),
    path('account/', account, name='account')
]
