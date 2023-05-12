from django.contrib.auth.models import User
from django.http import JsonResponse
from api.models import Playlist, PlaylistToUser, Track, TrackToPlaylist
from api.views.results import Error, Success
from api import tokendata
import json



def AllPlaylistsData(request):
    token_payload = tokendata.from_cookie_token_data(request)
    if token_payload is None:
        return Error.TokenVerificationError()
    
    try:
        author = User.objects.get(username=token_payload['username'])
    except:
        return Error.UserNotExist()
    

    # Get all Playlists
    if request.method == 'GET':
        data = {'playlists':[]}
        playlists_query = Playlist.objects.all()
        for playlist in playlists_query:
            data['playlists'].append({
                'id':playlist.id,
                'author':playlist.author.username,
                'name':playlist.name,
                'description':playlist.description
            })
        return Success.DataSuccess(data)


    # Create Playlist
    if request.method == 'POST':        
        try:
            request_data = json.loads(request.body)
            playlist_name = request_data['name']
            playlist_description = request_data['description']
        except:
            return Error.WrongBodyRepresentation()

        playlist = Playlist()
        playlist.author = author
        playlist.name = playlist_name
        if playlist_description is not None:
            playlist.description = playlist_description
        playlist.save()

        relation = PlaylistToUser()
        relation.user = author
        relation.playlist = playlist
        relation.save()
        return Success.SimpleSuccess()
    
    return Error.WrongMethod()



def PlaylistData(request, playlist_id):
    token_payload = tokendata.from_cookie_token_data(request)
    if token_payload is None:
        return Error.TokenVerificationError()
    
    try:
        user = User.objects.get(username=token_payload['username'])
    except:
        return Error.UserNotExist()
    
    try:
        playlist = Playlist.objects.get(id=playlist_id)
    except:
        return Error.PlaylistNotExist()


    # Get Playlist Data
    if request.method == 'GET':
        data = {
            "id":playlist.id,
            "author":playlist.author.username,
            "name":playlist.name,
            "description":playlist.description,
        }
        return Success.DataSuccess(data)
    

    # Update Playlist Data
    if request.method == 'PUT':
        if playlist.author.username != user.username:
            return Error.UserIsntAuthor()
        
        try:
            new_data = json.loads(request.body)
            playlist.name = new_data["name"]
            playlist.description = new_data["description"]
        except:
            return Error.WrongBodyRepresentation()
        
        playlist.save()
        return Success.SimpleSuccess()
    
    # Delete Playlist Data
    if request.method == 'DELETE':
        if playlist.author.username != user.username:
            return Error.UserIsntAuthor()
        
        playlist.delete()
        return Success.SimpleSuccess()

    return Error.WrongMethod()



def TrackToPlaylistData(request, playlist_id):
    token_payload = tokendata.from_cookie_token_data(request)
    if token_payload is None:
        return Error.TokenVerificationError
    
    try:
        user = User.objects.get(username=token_payload['username'])
    except:
        return Error.UserNotExist()
    
    try:
        playlist = Playlist.objects.get(id=playlist_id)
    except:
        return Error.PlaylistNotExist()


    # Append track to playlist
    if request.method == 'POST':
        if playlist.author.username != user.username:
            return Error.UserIsntAuthor()
        
        request_data = json.loads(request.body)
        try:
            request_data = json.loads(request.body)
            track_id = request_data['track_id']
        except:
            return Error.WrongBodyRepresentation()
        
        try:
            track = Track.objects.get(id=track_id)
        except:
            return Error.TrackNotExist()
        
        try:
            relation = TrackToPlaylist()
            relation.track = track
            relation.playlist = playlist
            relation.save()
        except:
            return Error.AlreadyInList()
        

        return Success.SimpleSuccess()
    

    # Get tracks of playlist
    if request.method == 'GET':
        data = {'tracks':[]}
        for relation in playlist.tracks.all():
            track = relation.track
            data['tracks'].append({
                'id':track.id,
                'name':track.name,
                'author':track.author.username,
                'tags':track.tags,
                'length':track.length,
                'album':track.album
            })
        return Success.DataSuccess(data)
    

    # Delete track from playlist
    if request.method == 'DELETE':
        if playlist.author.username != user.username:
            return Error.UserIsntAuthor()
        
        request_data = json.loads(request.body)
        try:
            request_data = json.loads(request.body)
            track_id = request_data['track_id']
        except:
            return Error.WrongBodyRepresentation()
        
        try:
            track = Track.objects.get(id=track_id)
        except:
            return Error.TrackNotExist()
        
        try:
            relation = TrackToPlaylist.objects.get(track=track, playlist=playlist)
        except:
            return Error.RelationNotExist()
        
        relation.delete()
        return Success.SimpleSuccess()
    
    return Error.WrongMethod()