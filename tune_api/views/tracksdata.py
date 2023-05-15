from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.http import FileResponse, HttpResponse
from tune_api.models import Track, TrackToUser
from tune_api.views.results import Error, Success
from tune_auth import tokendata
import json
import os
from server.settings import BASE_DIR



def AllTracksData(request):
    payload = tokendata.from_cookie_token_data(request)
    if payload is None:
        return Error.TokenVerificationError()
    
    try:
        author = User.objects.get(username=payload['username'])
    except:
        return Error.UserNotExist(user_payload=payload)
    

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
        return Success.DataSuccess(data, user_payload=payload)


    # Create Track
    if request.method == 'POST':
        storage = 'audio_files/'
        fs = FileSystemStorage(location=storage)

        try:
            file = request.FILES['Audio']
        except:
            return Error.WrongFileRepresentation(user_payload=payload)
        
        file_format = file.name.split('.')[-1]
        if file_format not in ['mp3']:
            return Error.WrongFileFormat(user_payload=payload)

        try:
            request_data = json.loads(request.POST['Data'])
            track_name = request_data['name']
            track_tags = request_data['tags']
            track_length = request_data['length']
            track_album = request_data['album']
        except:
            return Error.WrongBodyRepresentation(user_payload=payload)

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
        return Success.SimpleSuccess(user_payload=payload)
    
    return Error.WrongMethod(user_payload=payload)



def TrackData(request, track_id):
    payload = tokendata.from_cookie_token_data(request)
    if payload is None:
        return Error.TokenVerificationError()
    
    try:
        track = Track.objects.get(id=track_id)
    except:
        return Error.TrackNotExist(user_payload=payload)
    
    try:
        user = User.objects.get(username=payload['username'])
    except:
        return Error.UserNotExist(user_payload=payload)


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

        return Success.DataSuccess(data, user_payload=payload)
    

    # Update Track Data
    if request.method == 'PUT':
        if track.author.username != user.username:
            return Error.UserIsntAuthor(user_payload=payload)
        
        try:
            new_data = json.loads(request.body)
            track.name = new_data["name"]
            track.tags = new_data["tags"]
            track.length = new_data["length"]
            track.album = new_data["album"]
        except:
            return Error.WrongBodyRepresentation(user_payload=payload)
        
        track.save()
        return Success.SimpleSuccess(user_payload=payload)
    
    
    # Delete Track Data and Track Audio-File
    if request.method == 'DELETE':
        if track.author.username != user.username:
            return Error.UserIsntAuthor(user_payload=payload)
        
        track.delete()

        path = f'{BASE_DIR}\\audio_files\\{track_id}.mp3'
        if os.path.isfile(path):
            os.remove(path)
        
        return Success.SimpleSuccess(user_payload=payload)

    return Error.WrongMethod(user_payload=payload)
    


def TrackFile(request, track_id):
    payload = tokendata.from_cookie_token_data(request)
    if payload is None:
        return Error.TokenVerificationError()

    try:
        track = Track.objects.get(id=track_id)
    except:
        return Error.TrackNotExist(user_payload=payload)
    
    try:
        user = User.objects.get(username=payload['username'])
    except:
        return Error.UserNotExist(user_payload=payload)
    

    # Get track's audio file
    if request.method == 'GET':
        filename= f"audio_files/{track_id}.mp3"

        try:
            f = open(filename,"rb")
        except:
            return  Error.WrongFileRepresentation()

        response = HttpResponse()
        response['Content-Type'] ='audio/mp3'
        response['Content-Length'] =os.path.getsize(filename)

        response.write(f.read())
        return response
    
    return Error.WrongMethod()