from django.urls import path
from api.views import auth, userdata

urlpatterns = [
    path('register/', auth.UserRegister, name='UserRegister'),
    path('login/', auth.UserLogin, name='UserLogin'),
    path('token/', auth.UserToken, name='TokenUser'),
    path('<str:username>/profile/', userdata.UserProfileData, name='UserProfileData'),
    path('<str:username>/tracks/', userdata.UserTracksData, name='UserTracksData'),
    path('<str:username>/playlists/', userdata.UserPlaylistsData, name='UserPlaylistsData'),
]