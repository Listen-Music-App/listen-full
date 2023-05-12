from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.http import JsonResponse
from api.models import Track, TrackToUser
from api.views.results import Error, Success
from api import tokendata
import json
import os
from server.settings import BASE_DIR



def AllTracksData(request):
    token_payload = tokendata.from_cookie_token_data(request)
    if token_payload is None:
        return Error.TokenVerificationError()
    
    try:
        author = User.objects.get(username=token_payload['username'])
    except:
        return Error.UserNotExist()
    

    # Get all Tracks
    if request.method == 'GET':
        data = {'tracks':[]}
        tracks_query = Track.objects.all()
        for track in tracks_query:
            data['tracks'].append({
                'id':track.id,
                'name':track.name,
                'author':track.author.username,
                'tags':track.tags,
                'length':track.length,
                'album':track.album
            })
        return Success.DataSuccess(data)


    # Create Track
    if request.method == 'POST':
        storage = 'audio_files/'
        fs = FileSystemStorage(location=storage)

        try:
            file = request.FILES['Audio']
        except:
            return Error.WrongFileRepresentation()
        
        file_format = file.name.split('.')[-1]
        if file_format not in ['mp3']:
            return Error.WrongFileFormat()

        try:
            request_data = json.loads(request.POST['Data'])
            track_name = request_data['name']
            track_tags = request_data['tags']
            track_length = request_data['length']
            track_album = request_data['album']
        except:
            return Error.WrongBodyRepresentation()

        track = Track()
        track.author = author
        track.name = track_name
        track.save()

        file_name = fs.save(f'{track.id}.{file_format}', file)
        file_url = fs.url(file_name)
        
        relation = TrackToUser()
        relation.user = author
        relation.track = track
        relation.save()
        return Success.SimpleSuccess()
    
    return Error.WrongMethod()



def TrackData(request, track_id):
    token_payload = tokendata.from_cookie_token_data(request)
    if token_payload is None:
        return Error.TokenVerificationError()
    
    try:
        track = Track.objects.get(id=track_id)
    except:
        return Error.TrackNotExist()
    
    try:
        user = User.objects.get(username=token_payload['username'])
    except:
        return Error.UserNotExist()


    # Get Track Data
    if request.method == 'GET':
        data = {
            'id':track.id,
            'author':track.author.username,
            'name':track.name,
            'tags':track.tags,
            'length':track.length,
            'album':track.album
        }

        return Success.DataSuccess(data)
    

    # Update Track Data
    if request.method == 'PUT':
        if track.author.username != user.username:
            return Error.UserIsntAuthor()
        
        try:
            new_data = json.loads(request.body)
            track.name = new_data["name"]
            track.tags = new_data["tags"]
            track.length = new_data["length"]
            track.album = new_data["album"]
        except:
            return Error.WrongBodyRepresentation()
        
        track.save()
        return Success.SimpleSuccess()
    
    
    # Delete Track Data and Track Audio-File
    if request.method == 'DELETE':
        if track.author.username != user.username:
            return Error.UserIsntAuthor()
        
        track.delete()

        path = f'{BASE_DIR}\\audio_files\\{track_id}.mp3'
        if os.path.isfile(path):
            os.remove(path)
        
        return Success.SimpleSuccess()

    return Error.WrongMethod()
    