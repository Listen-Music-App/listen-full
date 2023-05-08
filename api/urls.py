from django.urls import path
from api import views

urlpatterns = [
    path('register/', views.UserRegister, name='UserRegister'),
    path('login/', views.UserLogin, name='UserLogin'),
    path('token/', views.TokenUser, name='TokenUser'),
    path('<str:username>/profile/', views.ProfileData, name='ProfileData'),
    # path('<str:username>/tracks/', views.TracksData, name='TracksData'),
]