import os
import requests

from tune_api.views.results import Error

AUTH_SERVER = os.environ.get('AUTH_SERVER', 'http://localhost:3000/auth/')
API_SECRET_KEY = 'e^ewy|7X^feBi2^PlQT+ZDy<.g&@,1'

def authorize(request):
    '''Checks request "Authorization" header for access token and
    sends request to the AUTH microservice and return payload if response == 200'''
    try:
        token = request.headers['Authorization']
        if token.split(' ')[0] != 'Bearer':
            return None
        token = token.split(' ')[1]
    except:
        return None
    
    response = requests.get(f'{AUTH_SERVER}verify/', headers={'AccessToken':token})
    if response.status_code != 200:
        return None
    
    user_payload = response.json()['payload']
    return user_payload



def userexists(username):
    '''Sends request to the AUTH microservice
    and return bool value'''
    response = requests.get(f'{AUTH_SERVER}check/{username}/', headers={'Secret-Key':API_SECRET_KEY})
    if response.status_code != 200:
        return False
    return True



def JWT_auth_required(endpoint):
    '''JWT authorization decorator\n

    if you want your endpoint to be JWT authorized add "payload" kwarg to it:\n
    def endpoint(*args, **kwargs, payload=None):
        ...
    '''
    def wrapper(*args, **kwargs):
        kwargs['payload'] = authorize(args[0])
        if kwargs['payload'] is None:
            return Error.TokenVerificationError()
        return endpoint(*args, **kwargs)
    return wrapper



def user_exists_check(endpoint):
    '''User exists check decorator\n
    checking does user with {username} from url exists
    decorate your endpoint using this decorator.
    You also need add "username" argument to it.\n
    def your_endpoint(*args, username, **kwargs):
        ...
    '''
    def wrapper(*args, **kwargs):
        username = kwargs['username']
        if not userexists(username):
            return Error.UserNotExist()
        return endpoint(*args, **kwargs)
    return wrapper