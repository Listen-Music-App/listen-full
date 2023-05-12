import json
from django.contrib.auth.models import User
from django.http import JsonResponse
from api.models import Playlist, PlaylistToUser, Profile, Track, TrackToUser
from api import tokendata
from api.views.results import Error, Success


def UserProfileData(request, username):
    payload = tokendata.from_cookie_token_data(request)
    if payload is None:
        return Error.TokenVerificationError()
        
    if request.method == 'GET':
        try:
            profile = Profile.objects.get(username=username)
        except:
            return Error.ProfileNotExist()

        data = {
            'username':profile.username,
            'name':profile.name,
            'surname':profile.surname,
            'description':profile.description
        }

        return Success.DataSuccess(data)

    return Error.WrongMethod()



def UserTracksData(request, username):
    payload = tokendata.from_cookie_token_data(request)
    if payload is None:
        return Error.TokenVerificationError()
    
    try:
        user = User.objects.get(username=username)
    except:
        return Error.UserNotExist()
    

    # Get user's tracks
    if request.method == 'GET':
        
        tracks = user.tracks.all()
        data = {
            'tracks':[]
        }
        for track_to_user in tracks:
            data['tracks'].append({
                "id":track_to_user.track.id,
                "author":track_to_user.track.author.username,
                "name":track_to_user.track.name,
                "length":track_to_user.track.length,
            })
        return Success.DataSuccess()
    

    # Append track to user
    if request.method == "POST":
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
            relation = TrackToUser()
            relation.track = track
            relation.user = user
            relation.save()
        except:
            return Error.AlreadyInList()
        
        return Success.SimpleSuccess()
    

    # Delete track from user
    if request.method == "DELETE":
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
            relation = TrackToUser.objects.get(track=track, user=user)
        except:
            return Error.RelationNotExist()
        
        relation.delete()
        return Success.SimpleSuccess()
    
    return Error.WrongMethod()



def UserPlaylistsData(request, username):
    payload = tokendata.from_cookie_token_data(request)
    if payload is None:
        return Error.TokenVerificationError()
    
    try:
        user = User.objects.get(username=username)
    except:
        return Error.UserNotExist()
    

    # Get user's playlists
    if request.method == 'GET':
        playlists = user.playlists.all()
        data = {
            'playlists':[]
        }
        for playlist_to_user in playlists:
            data['playlists'].append({
                "id":playlist_to_user.playlist.id,
                "author":playlist_to_user.playlist.author.username,
                "name":playlist_to_user.playlist.name,
            })
        return Success.DataSuccess(data)

    
    # Append playlist to user
    if request.method == 'POST':
        try:
            request_data = json.loads(request.body)
            playlist_id = request_data['playlist_id']
        except:
            return Error.WrongBodyRepresentation()

        try:
            playlist = Playlist.objects.get(id=playlist_id)
        except:
            return Error.PlaylistNotExist()
        
        try:
            relation = PlaylistToUser()
            relation.playlist = playlist
            relation.user = user
            relation.save()
        except:
            return Error.AlreadyInList()
        
        return Success.SimpleSuccess()
    

    # Delete Playlist from User
    if request.method == 'DELETE':
        try:
            request_data = json.loads(request.body)
            playlist_id = request_data['playlist_id']
        except:
            return Error.WrongBodyRepresentation()

        try:
            playlist = Playlist.objects.get(id=playlist_id)
        except:
            return Error.PlaylistNotExist()
        
        try:
            relation = PlaylistToUser.objects.get(playlist=playlist, user=user)
        except:
            return Error.RelationNotExist()
        
        relation.delete()
        return Success.SimpleSuccess()
    
    return Error.WrongMethod()