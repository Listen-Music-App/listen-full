from django.contrib import admin
from .models import Album, Profile, Track, Playlist, TrackToPlaylist, TrackToUser

# Register your models here.
admin.site.register(Profile)
admin.site.register(Track)
admin.site.register(Playlist)
admin.site.register(Album)
admin.site.register(TrackToPlaylist)
admin.site.register(TrackToUser)