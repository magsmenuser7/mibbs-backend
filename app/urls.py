# accounts/urls.py
from django.urls import path
from .views import RegisterUser, LoginUser

urlpatterns = [
    path('registerUser', RegisterUser.as_view(), name='register'),
    path('login', LoginUser.as_view(), name='login'),
]
