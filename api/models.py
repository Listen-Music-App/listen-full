from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, blank=True, null=True)
    surname = models.CharField(max_length=20, blank=True, null=True)
    description = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self) -> str:
        return self.user.username



class Album(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self) -> str:
        return f'{self.author.username} - {self.name}'



class Playlist(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self) -> str:
        return self.name



class Track(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=60)
    tags = models.CharField(max_length=200, blank=True, null=True)
    length = models.IntegerField()
    album = models.ForeignKey(Album, blank=True, null=True, on_delete=models.CASCADE, related_name='tracks')

    def __str__(self) -> str:
        return f'{self.author.username} - {self.name}'



class TrackToPlaylist(models.Model):
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.track.name} -> {self.playlist.name}'



class TrackToUser(models.Model):
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tracks')

    def __str__(self) -> str:
        return f'{self.track.id} -> {self.user.username}'
