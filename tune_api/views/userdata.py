import glob
import json
import os
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from tune_api.models import Playlist, PlaylistToUser, Track, TrackToUser
from tune_auth import tokendata
from tune_api.views.results import Error, Success


def UserData(request, username):
    payload = tokendata.from_cookie_token_data(request)
    if payload is None:
        return Error.TokenVerificationError()
        

    if request.method == 'GET':
        try:
            user = User.objects.get(username=username)
        except:
            return Error.UserNotExist(user_payload=payload)

        data = {
            'username':user.username,
            'name':user.first_name,
            'surname':user.last_name
        }

        return Success.DataSuccess(data, user_payload=payload)

    return Error.WrongMethod(user_payload=payload)



def UserImage(request, username):
    payload = tokendata.from_cookie_token_data(request)
    if payload is None:
        return Error.TokenVerificationError()

    if not User.objects.filter(username=username).exists():
        return Error.UserNotExist(user_payload=payload)

    storage = 'images/users/'

    # Get UserImage
    if request.method == 'GET':
        filename = glob.glob(f"{storage}{username}.*")

        if filename:
            filename = filename[0]
            f = open(filename, "rb")
            format = filename.split('.')[-1]
        else:
            f = open(f"images/users/userdefaultimage.jpg", "rb")
            format = 'jpg'

        response = HttpResponse()
        response['Content-Type'] = f'image/{format}'

        response.write(f.read())
        return response
    

    # Upload UserImage
    if request.method == 'POST':
        fs = FileSystemStorage(location=storage)

        try:
            file = request.FILES['Image']
        except:
            return Error.WrongFileRepresentation(user_payload=payload)
        
        file_format = file.name.split('.')[-1]
        if file_format not in ['jpeg', 'jpg', 'png', 'gif']:
            return Error.WrongFileFormat(user_payload=payload)
        
        previous_file = glob.glob(f'{storage}{username}.*')
        if previous_file:
            os.remove(previous_file[0])

        file_name = fs.save(f'{username}.{file_format}', file)
        file_url = fs.url(file_name)
        return Success.SimpleSuccess(user_payload=payload)


    return Error.WrongMethod()



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