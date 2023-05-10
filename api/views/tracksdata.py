from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.http import JsonResponse
from api.models import Track, TrackToUser, TrackToPlaylist
from api import tokendata
import json



def AllTracksData(request):
    token_payload = tokendata.from_cookie_token_data(request)
    if token_payload is None:
        return JsonResponse({'result':'failed','error':'TokenVerificationFailed'}, safe=False)
    
    try:
        author = User.objects.get(username=token_payload['username'])
    except:
        return JsonResponse({'result':'failed','error':'UserNotExist'}, safe=False)
    
    # Get all Tracks
    if request.method == 'GET':
        data = {'tracks':[]}
        tracks_query = Track.objects.all()
        for track in tracks_query:
            data['tracks'].append({
                'id':track.id,
                'author':track.author.username,
                'tags':track.tags,
                'length':track.length,
                'album':track.album
            })
        return JsonResponse({'result':'success', 'data':data}, safe=False)

    # Create Track
    if request.method == 'POST':
        storage = 'audio_files/'
        fs = FileSystemStorage(location=storage)

        try:
            file = request.FILES['Audio']
            file_format = file.name.split('.')[-1]
            if file_format not in ['mp3']:
                return JsonResponse({'result':'failed','error':'WrongFileFormat'}, safe=False)
        except:
            return JsonResponse({'result':'failed','error':'WrongFileRepresentation'}, safe=False)
        
        try:
            request_data = json.loads(request.POST['Data'])
            track_name = request_data['name']
            track_tags = request_data['tags']
            track_length = request_data['length']
            track_album = request_data['album']
        except:
            return JsonResponse({'result':'failed','error':'WrongBodyRepresentation'}, safe=False)

        track = Track()
        track.author = author
        track.name = track_name
        track.save()

        print(track.id)

        file_name = fs.save(f'{track.id}.{file_format}', file)
        file_url = fs.url(file_name)
        
        relation = TrackToUser()
        relation.user = author
        relation.track = track
        relation.save()
        return JsonResponse({'result':'success'}, safe=False)
    
    return JsonResponse({'result':'failed', 'error':'WrongMethod'}, safe=False)
