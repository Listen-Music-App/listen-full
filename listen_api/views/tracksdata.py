import glob
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from listen_api.auth import JWT_auth_required
from listen_api.models import Track, TrackToUser
from listen_api.views.results import Error, Success
import json
import os
import mutagen



@JWT_auth_required
def AllTracksData(request, payload=None):    
    author = payload['username']

    # Get all Tracks
    if request.method == 'GET':
        offset = request.GET.get('offset', 0)
        limit = request.GET.get('limit', 10)
        filter_map = {}

        search = request.GET.get('search', None)
        if search:
            filter_map['name__icontains'] = search

        genre = request.GET.get('genre', None)
        if genre:
            filter_map['genre_id'] = genre

        data = {'tracks':[]}

        tracks_query = Track.objects.filter(**filter_map)[offset:offset + limit]
        for track in tracks_query:
            data['tracks'].append({
                'id':track.id,
                'name':track.name,
                'author':track.author,
                'length':track.length,
                'album':track.album, 
                'genre':track.genre.name,
            })
        return Success.DataSuccess(data, user_payload=payload)


    # Create Track
    if request.method == 'POST':
        storage = 'audio/'
        fs = FileSystemStorage(location=storage)

        try:
            file = request.FILES['Audio']
        except:
            return Error.WrongFileRepresentation(user_payload=payload)
        
        file_format = file.name.split('.')[-1]
        if file_format not in ['mp3','m4a','wav']:
            return Error.WrongFileFormat(user_payload=payload)

        try:
            request_data = json.loads(request.POST['Data'])
            track_name = request_data['name']
            track_genre = request_data['genre']
            # track_album = request_data['album']
        except:
            return Error.WrongBodyRepresentation(user_payload=payload)

        track = Track()
        track.author = author
        track.name = track_name
        track.genre = track_genre

        track.length = mutagen.File(file).info.length
        track.save()

        relation = TrackToUser()
        relation.username = author
        relation.track = track
        relation.save()

        fs.save(f'{track.id}.{file_format}', file)

        return Success.SimpleSuccess(user_payload=payload)
    
    return Error.WrongMethod(user_payload=payload)



@JWT_auth_required
def TrackData(request, track_id, payload=None):

    try:
        track = Track.objects.get(id=track_id)
    except:
        return Error.TrackNotExist(user_payload=payload)

    # Get Track Data
    if request.method == 'GET':
        data = {
            'id':track.id,
            'author':track.author,
            'name':track.name,
            'length':track.length,
            'genre':track.genre,
            # 'album':track.album
        }

        return Success.DataSuccess(data, user_payload=payload)
    

    # Update Track Data
    if request.method == 'PUT':
        if track.author != payload['username']:
            return Error.UserIsntAuthor(user_payload=payload)
        
        try:
            new_data = json.loads(request.body)
            track.name = new_data["name"]
            track.genre = new_data["genre"]
        except:
            return Error.WrongBodyRepresentation(user_payload=payload)

        track.save()
        return Success.SimpleSuccess(user_payload=payload)
    
    
    # Delete Track Data and Track Audio-File
    if request.method == 'DELETE':
        if track.author != payload['username']:
            return Error.UserIsntAuthor(user_payload=payload)
        
        track.delete()

        filename = glob.glob(f'audio/{track_id}.*')
        if filename:
            filename = filename[0]
            os.remove(filename)
        
        return Success.SimpleSuccess(user_payload=payload)

    return Error.WrongMethod(user_payload=payload)
    


@JWT_auth_required
def TrackFile(request, track_id, payload=None):

    if not Track.objects.filter(id=track_id).exists():
        return Error.TrackNotExist(user_payload=payload)


    # Get track's audio file
    if request.method == 'GET':
        filename = glob.glob(f"audio/{track_id}.*")

        if filename:
            filename = filename[0]
            f = open(filename,"rb")
            format = filename.split('.')[-1]
        else:
            return  Error.WrongFileRepresentation()

        response = HttpResponse()
        response['Content-Type'] = f'audio/{format}'
        response['Content-Length'] = os.path.getsize(filename)

        response.write(f.read())
        return response
    
    return Error.WrongMethod()