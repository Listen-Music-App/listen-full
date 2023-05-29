from django.urls import path
from tune_api.views import tagsdata, userdata, playlistsdata, tracksdata

urlpatterns = [
    path('user/<str:username>/tracks/', userdata.UserTracksData, name='UserTracksData'),
    path('user/<str:username>/playlists/', userdata.UserPlaylistsData, name='UserPlaylistsData'),

    path('playlists/', playlistsdata.AllPlaylistsData, name='AllPlaylistsData'),
    path('playlists/<int:playlist_id>/', playlistsdata.PlaylistData, name='PlaylistData'),
    path('playlists/<int:playlist_id>/tracks/', playlistsdata.TrackToPlaylistData, name='TracksToPlaylist'),

    path('tracks/', tracksdata.AllTracksData, name='AllTracksData'),
    path('tracks/<int:track_id>/', tracksdata.TrackData, name='TrackData'),
    path('tracks/<int:track_id>/file/', tracksdata.TrackFile, name='TrackFile'),

    path('tags/', tagsdata.AllTagsData, name='AllTagsData'),

    path('images/users/<str:username>/', userdata.UserImage, name='UserImage'),
    path('images/playlists/<int:playlist_id>/', playlistsdata.PlaylistImage, name='PlaylistImage')
]