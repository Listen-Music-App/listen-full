from django.db import models



class Album(models.Model):
    author = models.CharField(max_length=150, null=False)
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self) -> str:
        return f'{self.author} - {self.name}'



class Playlist(models.Model):
    author = models.CharField(max_length=150, null=False)
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self) -> str:
        return f'{self.author} - {self.name}'



class Track(models.Model):
    author = models.CharField(max_length=150, null=False)
    name = models.CharField(max_length=60)
    tags = models.CharField(max_length=200, blank=True, null=True)
    length = models.IntegerField(null=True)
    album = models.ForeignKey(Album, blank=True, null=True, on_delete=models.CASCADE, related_name='tracks')

    def __str__(self) -> str:
        return f'{self.author} - {self.name}'



class TrackToPlaylist(models.Model):
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name='tracks')

    def __str__(self) -> str:
        return f'{self.playlist.name} -> {self.track.name}'
    
    class Meta:
        unique_together = ("track", "playlist")



class TrackToUser(models.Model):
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    username = models.CharField(max_length=150, null=False)

    def __str__(self) -> str:
        return f'{self.username} -> {self.track.name} [ID:{self.track.id}]'
    
    class Meta:
        unique_together = ("track", "username")
    


class PlaylistToUser(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    username = models.CharField(max_length=150, null=False)

    def __str__(self) -> str:
        return f'{self.username} -> {self.playlist.name} [ID:{self.playlist.id}]'

    class Meta:
        unique_together = ("playlist", "username")



class Tag(models.Model):
    text = models.TextField(null=False, unique=True)

    def __str__(self) -> str:
        return f'#{self.text}'



class TagToTrack(models.Model):
    tag = models.ForeignKey(Tag, null=False, on_delete=models.DO_NOTHING)
    track = models.ForeignKey(Track, null=False, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'track_id: {self.track.id}, hashtag_id: {self.tag.id}'
    
    class Meta:
        unique_together = ("tag", "track")