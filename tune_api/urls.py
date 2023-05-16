from django.urls import path
from tune_api.views import userdata, playlistsdata, tracksdata

urlpatterns = [
    path('<str:username>/', userdata.UserData, name='UserData'),
    path('<str:username>/tracks/', userdata.UserTracksData, name='UserTracksData'),
    path('<str:username>/playlists/', userdata.UserPlaylistsData, name='UserPlaylistsData'),

    path('playlists/', playlistsdata.AllPlaylistsData, name='AllPlaylistsData'),
    path('playlists/<int:playlist_id>/', playlistsdata.PlaylistData, name='PlaylistData'),
    path('playlists/<int:playlist_id>/tracks/', playlistsdata.TrackToPlaylistData, name='TracksToPlaylist'),

    path('tracks/', tracksdata.AllTracksData, name='AllTracksData'),
    path('tracks/<int:track_id>/', tracksdata.TrackData, name='TrackData'),
    path('tracks/<int:track_id>.mp3/', tracksdata.TrackFile, name='TrackFile'),

    path('images/users/<str:username>/', userdata.UserImage, name='UserImage'),
    path('images/users/', userdata.UserImageUpload, name='UserImageUpload'),
]