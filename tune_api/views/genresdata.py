from tune_api.models import Genre
from tune_api.views.results import Error, Success
from tune_api.auth import JWT_auth_required



@JWT_auth_required
def AllGenresData(request, payload=None):

    if request.method == 'GET':
        offset = int(request.GET.get('offset', 0))
        limit = int(request.GET.get('limit', 10))
        search = request.GET.get('search', None)

        filter_map = {}

        if search:
            filter_map['name__icontains'] = search

        genres = Genre.objects.filter(**filter_map).all()[offset:offset+limit]
        
        data = {
            "genres":[]
        }

        for genre in genres:
            data["genres"].append({
                "id":genre.id,
                "name":genre.name,
            })
        
        return Success.DataSuccess(data, payload)

    return Error.WrongMethod(payload)