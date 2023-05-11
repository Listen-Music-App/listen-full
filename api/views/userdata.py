import json
from django.contrib.auth.models import User
from django.http import JsonResponse
from api.models import Playlist, PlaylistToUser, Profile, Track, TrackToUser
from api import tokendata


def UserProfileData(request, username):
    payload = tokendata.from_cookie_token_data(request)
    if payload is None:
        return JsonResponse({'result':'failed','error':'TokenVerificationFailed'}, safe=False)
        
    if request.method == 'GET':
        try:
            profile = Profile.objects.get(username=username)
        except:
            return JsonResponse({'result':'failed', 'error':'ProfileDoesNotExist', 'user':payload}, safe=False)

        data = {
            'username':profile.username,
            'name':profile.name,
            'surname':profile.surname,
            'description':profile.description
        }

        return JsonResponse({'result':'success', 'user':payload, 'data':data}, safe=False)

    return JsonResponse({'result':'failed', 'error':'WrongMethod'}, safe=False)



def UserTracksData(request, username):
    payload = tokendata.from_cookie_token_data(request)
    if payload is None:
        return JsonResponse({'result':'failed','error':'TokenVerificationFailed'}, safe=False)
    
    try:
        user = User.objects.get(username=username)
    except:
        return JsonResponse({'result':'failed','error':'UserNotExist'}, safe=False)
    

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
        return JsonResponse({'result':'success', 'user':payload, 'data':data}, safe=False)
    

    # Append track to user
    if request.method == "POST":
        request_data = json.loads(request.body)
        try:
            request_data = json.loads(request.body)
            track_id = request_data['track_id']
        except:
            return JsonResponse({'result':'failed','error':'WrongBodyRepresentation'}, safe=False)
        
        try:
            track = Track.objects.get(id=track_id)
        except:
            return JsonResponse({'result':'failed','error':'TrackNotExist'}, safe=False)
        
        try:
            relation = TrackToUser()
            relation.track = track
            relation.user = user
            relation.save()
        except:
            return JsonResponse({'result':'failed','error':'TrackAlreadyInList'}, safe=False)
        
        return JsonResponse({'result':'success'}, safe=False)
    

    # Delete track from user
    if request.method == "DELETE":
        request_data = json.loads(request.body)
        try:
            request_data = json.loads(request.body)
            track_id = request_data['track_id']
        except:
            return JsonResponse({'result':'failed','error':'WrongBodyRepresentation'}, safe=False)

        try:
            track = Track.objects.get(id=track_id)
        except:
            return JsonResponse({'result':'failed','error':'TrackNotExist'}, safe=False)
        
        try:
            relation = TrackToUser.objects.get(track=track, user=user)
        except:
            return JsonResponse({'result':'failed','error':'TrackToUserNotExist'}, safe=False)
        
        relation.delete()
        return JsonResponse({'result':'success'}, safe=False)
    
    return JsonResponse({'result':'failed', 'error':'WrongMethod'}, safe=False)



def UserPlaylistsData(request, username):
    payload = tokendata.from_cookie_token_data(request)
    if payload is None:
        return JsonResponse({'result':'failed','error':'TokenVerificationFailed'}, safe=False)
    
    try:
        user = User.objects.get(username=username)
    except:
        return JsonResponse({'result':'failed','error':'UserNotExist'}, safe=False)
    

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
        return JsonResponse({'result':'success', 'user':payload, 'data':data}, safe=False)

    
    # Append playlist to user
    if request.method == 'POST':
        try:
            request_data = json.loads(request.body)
            playlist_id = request_data['playlist_id']
        except:
            return JsonResponse({'result':'failed','error':'WrongBodyRepresentation'}, safe=False)

        try:
            playlist = Playlist.objects.get(id=playlist_id)
        except:
            return JsonResponse({'result':'failed','error':'PlaylistNotExist'}, safe=False)
        
        try:
            relation = PlaylistToUser()
            relation.playlist = playlist
            relation.user = user
            relation.save()
        except:
            return JsonResponse({'result':'failed','error':'PlaylistAlreadyInList'}, safe=False)
        
        return JsonResponse({'result':'success'}, safe=False)
    

    # Delete Playlist from User
    if request.method == 'DELETE':
        try:
            request_data = json.loads(request.body)
            playlist_id = request_data['playlist_id']
        except:
            return JsonResponse({'result':'failed','error':'WrongBodyRepresentation'}, safe=False)

        try:
            playlist = Playlist.objects.get(id=playlist_id)
        except:
            return JsonResponse({'result':'failed','error':'PlaylistNotExist'}, safe=False)
        
        try:
            relation = PlaylistToUser.objects.get(playlist=playlist, user=user)
        except:
            return JsonResponse({'result':'failed','error':'PlaylistToUserNotExist'}, safe=False)
        
        relation.delete()
        return JsonResponse({'result':'success'}, safe=False)
    
    return JsonResponse({'result':'failed', 'error':'WrongMethod'}, safe=False)