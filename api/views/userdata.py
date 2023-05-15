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
            return Error.ProfileNotExist(user_payload=payload)

        data = {
            'username':profile.username,
            'name':profile.name,
            'surname':profile.surname,
            'description':profile.description
        }

        return Success.DataSuccess(data, user_payload=payload)

    return Error.WrongMethod(user_payload=payload)



def UserTracksData(request, username):
    payload = tokendata.from_cookie_token_data(request)
    if payload is None:
        return Error.TokenVerificationError()
    
    try:
        user = User.objects.get(username=username)
    except:
        return Error.UserNotExist(user_payload=payload)
    

    # Get user's tracks
    if request.method == 'GET':
        offset = request.GET.get('offset', None)
        limit = int(request.GET.get('limit', 10))

        if offset is not None:
            offset = int(offset)
            tracks = user.tracks.all()[offset:offset+limit]
        else:
            tracks = user.tracks.all()[:limit]
        
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
        return Success.DataSuccess(data, user_payload=payload)
    

    # Append track to user
    if request.method == "POST":
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
            relation = TrackToUser()
            relation.track = track
            relation.user = user
            relation.save()
        except:
            return Error.AlreadyInList(user_payload=payload)
        
        return Success.SimpleSuccess(user_payload=payload)
    

    # Delete track from user
    if request.method == "DELETE":
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
            relation = TrackToUser.objects.get(track=track, user=user)
        except:
            return Error.RelationNotExist(user_payload=payload)
        
        relation.delete()
        return Success.SimpleSuccess(user_payload=payload)
    
    return Error.WrongMethod(user_payload=payload)



def UserPlaylistsData(request, username):
    payload = tokendata.from_cookie_token_data(request)
    if payload is None:
        return Error.TokenVerificationError()
    
    try:
        user = User.objects.get(username=username)
    except:
        return Error.UserNotExist(user_payload=payload)
    

    # Get user's playlists
    if request.method == 'GET':
        offset = request.GET.get('offset', None)
        limit = int(request.GET.get('limit', 10))

        if offset is not None:
            offset = int(offset)
            playlists = user.playlists.all()[offset:offset+limit]
        else:
            playlists = user.playlists.all()[:limit]
        
        data = {
            'playlists':[]
        }
        for playlist_to_user in playlists:
            data['playlists'].append({
                "id":playlist_to_user.playlist.id,
                "author":playlist_to_user.playlist.author.username,
                "name":playlist_to_user.playlist.name,
            })
        return Success.DataSuccess(data, user_payload=payload)

    
    # Append playlist to user
    if request.method == 'POST':
        try:
            request_data = json.loads(request.body)
            playlist_id = request_data['playlist_id']
        except:
            return Error.WrongBodyRepresentation(user_payload=payload)

        try:
            playlist = Playlist.objects.get(id=playlist_id)
        except:
            return Error.PlaylistNotExist(user_payload=payload)
        
        try:
            relation = PlaylistToUser()
            relation.playlist = playlist
            relation.user = user
            relation.save()
        except:
            return Error.AlreadyInList(user_payload=payload)
        
        return Success.SimpleSuccess(user_payload=payload)
    

    # Delete Playlist from User
    if request.method == 'DELETE':
        try:
            request_data = json.loads(request.body)
            playlist_id = request_data['playlist_id']
        except:
            return Error.WrongBodyRepresentation(user_payload=payload)

        try:
            playlist = Playlist.objects.get(id=playlist_id)
        except:
            return Error.PlaylistNotExist(user_payload=payload)
        
        try:
            relation = PlaylistToUser.objects.get(playlist=playlist, user=user)
        except:
            return Error.RelationNotExist(user_payload=payload)
        
        relation.delete()
        return Success.SimpleSuccess(user_payload=payload)
    
    return Error.WrongMethod(user_payload=payload)