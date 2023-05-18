from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from tune_auth import tokendata
from tune_auth.tokenconfig import JWT_AUTH
import json



# Create your views here.
def UserRegister(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        if User.objects.filter(username=data['username']):
            return HttpResponse(409, status=409)

        if User.objects.filter(email=data['email']):
            return HttpResponse(409, status=409)
             
        user = User()
        user.username = data['username']
        user.email = data['email']
        user.set_password(data['password'])
        user.save()
        
        return HttpResponse(200, status=200)

    return HttpResponse(405, status=405)



def UserLogin(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data['username']
        password = data['password']
        
        try:
            user = User.objects.get(username=username)
        except:
            return HttpResponse(401, status=401)
        
        if not user.check_password(password):
            return HttpResponse(401, status=401)

        access_token, access_expiration = tokendata.access_token_generate(user)
        access_payload = tokendata.token_data(access_token, JWT_AUTH['ACCESS_SECRET'])

        refresh_token, refresh_expiration = tokendata.refresh_token_generate(user)
        
        response = JsonResponse({'result':'success', 'user_payload':access_payload}, safe=False, status=200)
        response.set_cookie(key='tune-access', value=access_token, expires=access_expiration, httponly=True, path='/api/')
        response.set_cookie(key='tune-refresh', value=refresh_token, expires=refresh_expiration, httponly=True, path='/auth/update')
        return response

    return HttpResponse(405, status=405)



def AccessTokenVerification(request):
    if request.method == 'GET':
        try:
            token = request.headers['AccessToken']
        except:
            return HttpResponse(status=400)
        
        payload = tokendata.token_data(token, JWT_AUTH['ACCESS_SECRET'])

        if not payload:
            return HttpResponse(status=400)

        if not User.objects.filter(id=payload['user_id'],username=payload['username'], email=payload['email']).exists():
            return HttpResponse(status=400)
        
        return JsonResponse({'payload':payload}, status=200, safe=False)

    return HttpResponse(405, status=405)



def AccessTokenUpdate(request):
    if request.method == 'GET':
        try:
            refresh_token = request.COOKIES['tune-refresh']
        except:
            return HttpResponse(status=400)
        
        
        payload = tokendata.token_data(refresh_token, JWT_AUTH['REFRESH_SECRET'])

        if not payload:
            return HttpResponse(status=400)
        
        try:
            user = User.objects.get(id=payload['user_id'], username=payload['username'], email=payload['email'])
        except:
            return HttpResponse(status=400)
        
        new_access_token, access_expirations = tokendata.access_token_generate(user)
        access_payload = tokendata.token_data(new_access_token, JWT_AUTH['ACCESS_SECRET'])

        response = JsonResponse({'result':'success', 'token_payload':access_payload}, safe=False)
        response.set_cookie(key='tune-access', value=new_access_token, expires=access_expirations, httponly=True)
        return response
    
    return HttpResponse(405, status=405)


def IsExistsCheck(request, username):
    if request.method == 'GET':
        if User.objects.filter(username=username).exists():
            return HttpResponse(200, status=200)
        return HttpResponse(404, status=404)

        