from django.contrib.auth.models import User
from django.http import JsonResponse
from api.models import Profile
from api import tokendata


def UserProfileData(request, username):
    if request.method == 'GET':
        payload = tokendata.from_cookie_token_data(request)
        if payload is None:
            return JsonResponse({'result':'failed','error':'TokenVerificationFailed'}, safe=False)

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
    if request.method == 'GET':

        payload = tokendata.from_cookie_token_data(request)
        if payload is None:
            return JsonResponse({'result':'failed','error':'TokenVerificationFailed'}, safe=False)
        
        try:
            user = User.objects.get(username=username)
        except:
            return JsonResponse({'result':'failed','error':'UserNotExist'}, safe=False)
        
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
    
    return JsonResponse({'result':'failed', 'error':'WrongMethod'}, safe=False)


def UserPlaylistsData(request, username):
    if request.method == 'GET':

        payload = tokendata.from_cookie_token_data(request)
        if payload is None:
            return JsonResponse({'result':'failed','error':'TokenVerificationFailed'}, safe=False)
        
        try:
            user = User.objects.get(username=username)
        except:
            return JsonResponse({'result':'failed','error':'UserNotExist'}, safe=False)
        
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
    
    return JsonResponse({'result':'failed', 'error':'WrongMethod'}, safe=False)