from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from api import tokendata
from api.models import Profile, TrackToUser
from rest_framework_jwt.utils import jwt_payload_handler
import json



# Create your views here.
def UserRegister(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        if User.objects.filter(username=data['username']):
            return JsonResponse({'result':'failed', 'error':'UsernameUsed'}, safe=False)

        if User.objects.filter(email=data['email']):
            return JsonResponse({'result':'failed', 'error':'EmailUsed'}, safe=False)
             
        user = User()
        user.username = data['username']
        user.email = data['email']
        user.set_password(data['password'])
        user.save()

        profile = Profile()
        profile.user = user
        profile.username = data['username']
        profile.save()
        
        return JsonResponse({'result':'success'}, safe=False)

    return JsonResponse({'result':'failed', 'error':'WrongMethod'}, safe=False)



def UserLogin(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data['username']
        password = data['password']
        
        try:
            user = User.objects.get(username=username)
        except:
            return JsonResponse({'result':'failed','error':'WrongUsername'}, safe=False)
        
        if not user.check_password(password):
            return JsonResponse({'result':'failed','error':'WrongPassword'}, safe=False)
        
        print(f'YOUR USER IS: {user}')

        token = tokendata.token_generate(user)
        print(f'YOUR TOKEN IS: {token}')
        response = JsonResponse({'result':'success'}, safe=False)
        response.set_cookie(key='JWT', value=token, max_age=3600, httponly=True)
        return response

    return JsonResponse({'result':'failed', 'error':'WrongMethod'}, safe=False)



def TokenUser(request):
    if request.method == 'GET':    
        payload = tokendata.from_cookie_token_data(request)
        if payload is None:
            return JsonResponse({'result':'failed','error':'TokenVerificationFailed'}, safe=False)
        return JsonResponse({'result':'success', 'user':payload}, safe=False)

    return JsonResponse({'result':'failed', 'error':'WrongMethod'}, safe=False)



def ProfileData(request, username):
    if request.method == 'GET':
        payload = tokendata.from_cookie_token_data(request)
        if payload is None:
            return JsonResponse({'result':'failed','error':'TokenVerificationFailed'}, safe=False)

        try:
            profile = Profile.objects.get(username=username)
        except:
            return JsonResponse({'result':'failed', 'error':'ProfileDoesNotExist', 'user':payload}, safe=False)

        data = {
            'user':profile.username,
            'name':profile.name,
            'surname':profile.surname,
            'description':profile.description
        }

        return JsonResponse({'result':'success', 'user':payload, 'data':data}, safe=False)


# def TracksData(request, username):
#     if request.method == 'GET':
#         user = User.objects.get(username=username)
#         print(user)
#         print(user.tracks.values())
#         return HttpResponse(200)




    

    


        
        