import glob
import os
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from tune_api.auth import JWT_auth_required
from tune_api.models import Playlist, PlaylistToUser, Track, TrackToPlaylist
from tune_api.views.results import Error, Success
import json



@JWT_auth_required
def AllPlaylistsData(request, payload=None):
       
    author = payload['username']
    
    # Get all Playlists
    if request.method == 'GET':
        offset = int(request.GET.get('offset', 0))
        limit = int(request.GET.get('limit', 10))

        data = {'playlists':[]}
        playlists_query = Playlist.objects.all()[offset:offset+limit]
        
        for playlist in playlists_query:
            data['playlists'].append({
                'id':playlist.id,
                'author':playlist.author,
                'name':playlist.name,
                'description':playlist.description
            })
        return Success.DataSuccess(data, user_payload=payload)


    # Create Playlist
    if request.method == "POST":        
        try:
            request_data = json.loads(request.body)
            playlist_name = request_data['name']
            playlist_description = request_data['description']
        except:
            return Error.WrongBodyRepresentation(user_payload=payload)

        playlist = Playlist()
        playlist.author = author
        playlist.name = playlist_name
        if playlist_description is not None:
            playlist.description = playlist_description
        playlist.save()

        relation = PlaylistToUser()
        relation.username = author
        relation.playlist = playlist
        relation.save()
        return Success.SimpleSuccess(user_payload=payload)
    
    return Error.WrongMethod(user_payload=payload)



@JWT_auth_required
def PlaylistData(request, playlist_id, payload=None):
    
    try:
        playlist = Playlist.objects.get(id=playlist_id)
    except:
        return Error.PlaylistNotExist(user_payload=payload)


    # Get Playlist Data
    if request.method == 'GET':
        data = {
            "id":playlist.id,
            "author":playlist.author,
            "name":playlist.name,
            "description":playlist.description,
        }
        return Success.DataSuccess(data, user_payload=payload)
    

    # Update Playlist Data
    if request.method == 'PUT':
        if playlist.author != payload['username']:
            return Error.UserIsntAuthor(user_payload=payload)
        
        try:
            new_data = json.loads(request.body)
            playlist.name = new_data["name"]
            playlist.description = new_data["description"]
        except:
            return Error.WrongBodyRepresentation(user_payload=payload)
        
        playlist.save()
        return Success.SimpleSuccess(user_payload=payload)
    
    # Delete Playlist Data
    if request.method == 'DELETE':
        if playlist.author != payload['username']:
            return Error.UserIsntAuthor(user_payload=payload)
        
        playlist.delete()
        return Success.SimpleSuccess(user_payload=payload)

    return Error.WrongMethod(user_payload=payload)



@JWT_auth_required
def PlaylistImage(request, playlist_id, payload=None):
    
    try:
        playlist = Playlist.objects.get(id=playlist_id)
    except:
        return Error.PlaylistNotExist(user_payload=payload)
    
    storage = 'images/playlists/'


    # Get PlaylistImage
    if request.method == 'GET':
        filename = glob.glob(f"{storage}{playlist.id}.*")

        if filename:
            filename = filename[0]
            f = open(filename, "rb")
            format = filename.split('.')[-1]
        else:
            f = open(f"images/playlists/playlistdefaultimage.png", "rb")
            format = 'png'

        response = HttpResponse()
        response['Content-Type'] = f'image/{format}'

        response.write(f.read())
        return response
    

    # Upload PlaylistImage
    if request.method == 'POST':
        fs = FileSystemStorage(location=storage)

        if playlist.author != payload['username']:
            return Error.UserIsntAuthor(user_payload=payload)
        
        try:
            file = request.FILES['Image']
        except:
            return Error.WrongFileRepresentation(user_payload=payload)
        
        file_format = file.name.split('.')[-1]
        if file_format not in ['jpeg', 'jpg', 'png']:
            return Error.WrongFileFormat(user_payload=payload)
        
        previous_file = glob.glob(f'{storage}{playlist.id}.*')
        if previous_file:
            os.remove(previous_file[0])

        file_name = fs.save(f'{playlist.id}.{file_format}', file)
        file_url = fs.url(file_name)
        return Success.SimpleSuccess(user_payload=payload)
    
    return Error.WrongMethod()



@JWT_auth_required
def TrackToPlaylistData(request, playlist_id, payload=None):
    
    try:
        playlist = Playlist.objects.get(id=playlist_id)
    except:
        return Error.PlaylistNotExist(user_payload=payload)


    # Append track to playlist
    if request.method == 'POST':
        if playlist.author != payload['username']:
            return Error.UserIsntAuthor(user_payload=payload)
        
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
            relation = TrackToPlaylist()
            relation.track = track
            relation.playlist = playlist
            relation.save()
        except:
            return Error.AlreadyInList(user_payload=payload)
        

        return Success.SimpleSuccess(user_payload=payload)
    

    # Get tracks of playlist
    if request.method == 'GET':
        data = {'tracks':[]}
        for relation in playlist.tracks.all():
            track = relation.track
            data['tracks'].append({
                'id':track.id,
                'name':track.name,
                'author':track.author,
                'length':track.length,
                'album':track.album
            })
        return Success.DataSuccess(data, user_payload=payload)
    

    # Delete track from playlist
    if request.method == 'DELETE':
        if playlist.author != payload['username']:
            return Error.UserIsntAuthor(user_payload=payload)
        
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
            relation = TrackToPlaylist.objects.get(track=track, playlist=playlist)
        except:
            return Error.RelationNotExist(user_payload=payload)
        
        relation.delete()
        return Success.SimpleSuccess(user_payload=payload)
    
    return Error.WrongMethod(user_payload=payload)