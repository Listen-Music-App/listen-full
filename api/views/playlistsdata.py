from django.contrib.auth.models import User
from django.http import JsonResponse
from api.models import Playlist, PlaylistToUser, Track, TrackToPlaylist
from api import tokendata
import json



def AllPlaylistsData(request):
    token_payload = tokendata.from_cookie_token_data(request)
    if token_payload is None:
        return JsonResponse({'result':'failed','error':'TokenVerificationFailed'}, safe=False)
    
    try:
        author = User.objects.get(username=token_payload['username'])
    except:
        return JsonResponse({'result':'failed','error':'UserNotExist'}, safe=False)
    
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
        return JsonResponse({'result':'success', 'data':data}, safe=False)

    # Create Playlist
    if request.method == 'POST':        
        try:
            request_data = json.loads(request.body)
            playlist_name = request_data['name']
            playlist_description = request_data['description']
        except:
            return JsonResponse({'result':'failed','error':'WrongBodyRepresentation'}, safe=False)

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
        return JsonResponse({'result':'success'}, safe=False)
    
    return JsonResponse({'result':'failed', 'error':'WrongMethod'}, safe=False)



def PlaylistData(request, playlist_id):
    token_payload = tokendata.from_cookie_token_data(request)
    if token_payload is None:
        return JsonResponse({'result':'failed','error':'TokenVerificationFailed'}, safe=False)
    
    try:
        user = User.objects.get(username=token_payload['username'])
    except:
        return JsonResponse({'result':'failed','error':'UserNotExist'}, safe=False)
    
    try:
        playlist = Playlist.objects.get(id=playlist_id)
    except:
        return JsonResponse({'result':'failed','error':'PlaylistNotExist'}, safe=False)

    # Get Playlist Data
    if request.method == 'GET':
        data = {
            "id":playlist.id,
            "author":playlist.author.username,
            "name":playlist.name,
            "description":playlist.description,
        }
        return JsonResponse({'result':'success', 'data':data}, safe=False)
    
    # Update Playlist Data
    if request.method == 'PUT':
        if playlist.author.username != user.username:
            return JsonResponse({'result':'failed','error':'UserIsntAuthor'}, safe=False)
        
        try:
            new_data = json.loads(request.body)
            playlist.name = new_data["name"]
            playlist.description = new_data["description"]
        except:
            return JsonResponse({'result':'failed','error':'WrongBodyRepresentation'}, safe=False) 
        
        playlist.save()
        return JsonResponse({'result':'success'}, safe=False)
    
    # Delete Playlist Data
    if request.method == 'DELETE':
        if playlist.author.username != user.username:
            return JsonResponse({'result':'failed','error':'UserIsntAuthor'}, safe=False)
        
        playlist.delete()
        return JsonResponse({'result':'success'}, safe=False)

    return JsonResponse({'result':'failed','error':'WrongMethod'}, safe=False)



def TrackToPlaylistData(request, playlist_id):
    token_payload = tokendata.from_cookie_token_data(request)
    if token_payload is None:
        return JsonResponse({'result':'failed','error':'TokenVerificationFailed'}, safe=False)
    
    try:
        user = User.objects.get(username=token_payload['username'])
    except:
        return JsonResponse({'result':'failed','error':'UserNotExist'}, safe=False)
    
    try:
        playlist = Playlist.objects.get(id=playlist_id)
    except:
        return JsonResponse({'result':'failed','error':'PlaylistNotExist'}, safe=False)


    # Append track to playlist
    if request.method == 'POST':
        if playlist.author.username != user.username:
            return JsonResponse({'result':'failed','error':'UserIsntAuthor'}, safe=False)
        
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
            relation = TrackToPlaylist()
            relation.track = track
            relation.playlist = playlist
            relation.save()
        except:
            return JsonResponse({'result':'failed','error':'TrackAlreadyInPlaylist'}, safe=False)
        return JsonResponse({'result':'success'}, safe=False)
    

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
        return JsonResponse({'result':'success', 'data':data}, safe=False)
    

    # Delete track from playlist
    if request.method == 'DELETE':
        if playlist.author.username != user.username:
            return JsonResponse({'result':'failed','error':'UserIsntAuthor'}, safe=False)
        
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
            relation = TrackToPlaylist.objects.get(track=track, playlist=playlist)
        except:
            return JsonResponse({'result':'failed','error':'TrackToPlaylistNotExist'}, safe=False)
        
        relation.delete()
        return JsonResponse({'result':'success'}, safe=False)
    
    return JsonResponse({'result':'failed','error':'WrongMethod'}, safe=False)