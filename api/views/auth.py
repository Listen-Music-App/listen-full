from django.contrib.auth.models import User
from django.http import JsonResponse
from api.models import Profile
from api.views.results import Error, Success
from api import tokendata
import json



# Create your views here.
def UserRegister(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        if User.objects.filter(username=data['username']):
            return Error.UsernameUsed()

        if User.objects.filter(email=data['email']):
            return Error.EmailUsed()
             
        user = User()
        user.username = data['username']
        user.email = data['email']
        user.set_password(data['password'])
        user.save()

        profile = Profile()
        profile.user = user
        profile.username = data['username']
        profile.save()
        
        return Success.SimpleSuccess()

    return Error.WrongMethod()



def UserLogin(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data['username']
        password = data['password']
        
        try:
            user = User.objects.get(username=username)
        except:
            return Error.WrongUsername()
        
        if not user.check_password(password):
            return Error.WrongPassword()
        
        print(f'YOUR USER IS: {user}')

        token = tokendata.token_generate(user)
        print(f'YOUR TOKEN IS: {token}')
        response = JsonResponse({'result':'success'}, safe=False)
        response.set_cookie(key='JWT', value=token, max_age=3600, httponly=True)
        return response

    return Error.WrongMethod()



def UserToken(request):
    payload = tokendata.from_cookie_token_data(request)
    if payload is None:
        return Error.TokenVerificationError()
    
    if request.method == 'GET':    
        return Success.SimpleSuccess()

    return Error.WrongMethod()

        