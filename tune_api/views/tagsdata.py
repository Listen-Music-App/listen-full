from tune_api.models import Tag
from tune_api.views.results import Error, Success
from tune_api.auth import JWT_auth_required



@JWT_auth_required
def AllTagsData(request, payload=None):
    if request.method == 'GET':
        offset = request.GET.get('offset', None)
        limit = int(request.GET.get('limit', 10))

        if offset is not None:
            offset = int(offset)
            tags = Tag.objects.all()[offset:offset+limit]
        else:
            tags = Tag.objects.all()[:limit]
        
        data = {
            "tags":[]
        }
        for tag in tags:
            data["tags"].append({
                "id":tag.id,
                "text":tag.text,
            })
        
        return Success.DataSuccess(data, user_payload=payload)
    return Error.WrongMethod(user_payload=payload)
