from django.urls import path
from tune_auth.views import auth

urlpatterns = [
    path('register/', auth.UserRegister, name='UserRegister'),
    path('login/', auth.UserLogin, name='UserLogin'),
    path('token/', auth.UserToken, name='TokenUser'),
]