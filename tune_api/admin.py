from django.contrib import admin
from .models import Album, Track, Playlist, TrackToPlaylist, TrackToUser, PlaylistToUser

# Register your models here.
admin.site.register(Track)
admin.site.register(Playlist)
admin.site.register(Album)
admin.site.register(TrackToPlaylist)
admin.site.register(TrackToUser)
admin.site.register(PlaylistToUser)