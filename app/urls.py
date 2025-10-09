# accounts/urls.py
from django.urls import path
from .views import RegisterView, LoginView,logout_view,google_login,Register,Login,AssessmentCreateView

urlpatterns = [
    path('registerUser', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', logout_view, name='logout'),
    path('google-login/', google_login, name='google_login'),
    path('register/', Register.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
    path('assessment/', AssessmentCreateView.as_view(), name='assessment'),
]
