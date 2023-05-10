import json
from api.models import Playlist, Track, TrackToPlaylist
from django.contrib.auth.models import User
from django.http import JsonResponse
from api import tokendata


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
        
        relation = TrackToPlaylist.objects.get(track=track, playlist=playlist)
        relation.delete()
        return JsonResponse({'result':'success'}, safe=False)
    
    return JsonResponse({'result':'failed','error':'WrongMethod'}, safe=False)
        
        
        
        
