from django.urls import path
from api import views

urlpatterns = [
    path('register/', views.UserRegister, name='UserRegister'),
    path('login/', views.UserLogin, name='UserLogin'),
    path('tokendata/', views.TokenFromCookieData, name='TokenFromCookieVerification'),
]