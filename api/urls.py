from django.urls import path
from api import views

urlpatterns = [
    path('register/', views.UserRegister, name='UserRegister'),
    path('login/', views.UserLogin, name='UserLogin'),
    path('token/', views.UserToken, name='TokenUser'),
    path('<str:username>/profile/', views.UserProfileData, name='UserProfileData'),
    path('<str:username>/tracks/', views.UserTracksData, name='UserTracksData'),
]