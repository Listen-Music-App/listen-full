from django.http import JsonResponse
from django.contrib.auth.models import User
from api import tokendata
from server.settings import SECRET_KEY as secret
from rest_framework_jwt.utils import jwt_payload_handler
import json
import jwt

from requests import Response

# Create your views here.
def UserRegister(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        if User.objects.filter(username=data['username']):
            return JsonResponse({'result':'failed', 'error':'UsernameUsed'}, safe=False)

        if User.objects.filter(email=data['email']):
            return JsonResponse({'result':'failed', 'error':'EmailUsed'}, safe=False)
        
        User.objects.create_user(username=data['username'], email=data['email'], password=data['password'])
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

        payload = jwt_payload_handler(user)
        token = jwt.encode(payload, secret, algorithm='HS256').decode('utf-8')
        print(f'YOUR TOKEN IS: {token}')
        response = JsonResponse({'result':'success'}, safe=False)
        response.set_cookie(key='JWT', value=token, max_age=3600, httponly=True)
        return response

    return JsonResponse({'result':'failed', 'error':'WrongMethod'}, safe=False)


def TokenFromCookieData(request):
    if request.method == 'GET':    
        payload = tokendata.from_cookie_data(request, secret)
        if payload is None:
            return JsonResponse({'result':'failed','error':'TokenVerificationFailed'}, safe=False)
        return JsonResponse(payload, safe=False)

    return JsonResponse({'result':'failed', 'error':'WrongMethod'}, safe=False)




    

    


        
        