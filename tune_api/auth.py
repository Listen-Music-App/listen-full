import requests

AUTH_SERVER = 'http://127.0.0.1:5000/auth/'
API_SECRET_KEY = 'e^ewy|7X^feBi2^PlQT+ZDy<.g&@,1'

def authorize(request):
    try:
        token = request.COOKIES['tune-access']
    except:
        return None
    
    response = requests.get(f'{AUTH_SERVER}verify/', headers={'AccessToken':token})
    if response.status_code != 200:
        return None
    
    user_payload = response.json()['payload']
    return user_payload


def userexists(username):
    response = requests.get(f'{AUTH_SERVER}check/{username}', cookies={'SECRET_KEY':API_SECRET_KEY})
    if response.status_code != 200:
        return False
    return True

    