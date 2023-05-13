from django.contrib.auth.models import User
from django.http import JsonResponse
from api.models import Playlist, PlaylistToUser, Track, TrackToPlaylist
from api.views.results import Error, Success
from api import tokendata
import json



def AllPlaylistsData(request):
    payload = tokendata.from_cookie_token_data(request)
    if payload is None:
        return Error.TokenVerificationError()
    
    try:
        author = User.objects.get(username=payload['username'])
    except:
        return Error.UserNotExist(user_payload=payload)
    

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
        return Success.DataSuccess(data, user_payload=payload)


    # Create Playlist
    if request.method == 'POST':        
        try:
            request_data = json.loads(request.body)
            playlist_name = request_data['name']
            playlist_description = request_data['description']
        except:
            return Error.WrongBodyRepresentation(user_payload=payload)

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
        return Success.SimpleSuccess(user_payload=payload)
    
    return Error.WrongMethod(user_payload=payload)



def PlaylistData(request, playlist_id):
    payload = tokendata.from_cookie_token_data(request)
    if payload is None:
        return Error.TokenVerificationError()
    
    try:
        user = User.objects.get(username=payload['username'])
    except:
        return Error.UserNotExist(user_payload=payload)
    
    try:
        playlist = Playlist.objects.get(id=playlist_id)
    except:
        return Error.PlaylistNotExist(user_payload=payload)


    # Get Playlist Data
    if request.method == 'GET':
        data = {
            "id":playlist.id,
            "author":playlist.author.username,
            "name":playlist.name,
            "description":playlist.description,
        }
        return Success.DataSuccess(data, user_payload=payload)
    

    # Update Playlist Data
    if request.method == 'PUT':
        if playlist.author.username != user.username:
            return Error.UserIsntAuthor(user_payload=payload)
        
        try:
            new_data = json.loads(request.body)
            playlist.name = new_data["name"]
            playlist.description = new_data["description"]
        except:
            return Error.WrongBodyRepresentation(user_payload=payload)
        
        playlist.save()
        return Success.SimpleSuccess(user_payload=payload)
    
    # Delete Playlist Data
    if request.method == 'DELETE':
        if playlist.author.username != user.username:
            return Error.UserIsntAuthor(user_payload=payload)
        
        playlist.delete()
        return Success.SimpleSuccess(user_payload=payload)

    return Error.WrongMethod(user_payload=payload)



def TrackToPlaylistData(request, playlist_id):
    payload = tokendata.from_cookie_token_data(request)
    if payload is None:
        return Error.TokenVerificationError()
    
    try:
        user = User.objects.get(username=payload['username'])
    except:
        return Error.UserNotExist(user_payload=payload)
    
    try:
        playlist = Playlist.objects.get(id=playlist_id)
    except:
        return Error.PlaylistNotExist(user_payload=payload)


    # Append track to playlist
    if request.method == 'POST':
        if playlist.author.username != user.username:
            return Error.UserIsntAuthor(user_payload=payload)
        
        request_data = json.loads(request.body)
        try:
            request_data = json.loads(request.body)
            track_id = request_data['track_id']
        except:
            return Error.WrongBodyRepresentation(user_payload=payload)
        
        try:
            track = Track.objects.get(id=track_id)
        except:
            return Error.TrackNotExist(user_payload=payload)
        
        try:
            relation = TrackToPlaylist()
            relation.track = track
            relation.playlist = playlist
            relation.save()
        except:
            return Error.AlreadyInList(user_payload=payload)
        

        return Success.SimpleSuccess(user_payload=payload)
    

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
        return Success.DataSuccess(data, user_payload=payload)
    

    # Delete track from playlist
    if request.method == 'DELETE':
        if playlist.author.username != user.username:
            return Error.UserIsntAuthor(user_payload=payload)
        
        request_data = json.loads(request.body)
        try:
            request_data = json.loads(request.body)
            track_id = request_data['track_id']
        except:
            return Error.WrongBodyRepresentation(user_payload=payload)
        
        try:
            track = Track.objects.get(id=track_id)
        except:
            return Error.TrackNotExist(user_payload=payload)
        
        try:
            relation = TrackToPlaylist.objects.get(track=track, playlist=playlist)
        except:
            return Error.RelationNotExist(user_payload=payload)
        
        relation.delete()
        return Success.SimpleSuccess(user_payload=payload)
    
    return Error.WrongMethod(user_payload=payload)