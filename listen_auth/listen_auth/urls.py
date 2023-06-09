from django.urls import path
from listen_auth.views import auth

urlpatterns = [
    path('register/', auth.UserRegister, name='UserRegister'),
    path('login/', auth.UserLogin, name='UserLogin'),
    path('verify/', auth.AccessTokenVerification, name='AccessTokenVerification'),
    path('update/', auth.AccessTokenUpdate, name='AccessTokenUpdate'),
    path('check/<str:username>/', auth.IsExistsCheck, name='UserExistsCheck'),
]