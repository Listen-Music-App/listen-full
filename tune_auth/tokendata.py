import jwt
from rest_framework_jwt.utils import jwt_payload_handler
from server.settings import SECRET_KEY as secret



def token_generate(user:object, secret=secret):
    payload = jwt_payload_handler(user)
    token = jwt.encode(payload, secret, algorithm='HS256').decode('utf-8')
    return token


def from_cookie_token_data(request, secret=secret):
    try:
        token = request.COOKIES['JWT']
        data = jwt.decode(token, secret, algorithms='HS256')
    except:
        return None
    return data


def token_data(token:str, secret=secret):
    try:
        data = jwt.decode(token, secret, algorithms='HS256')
    except:
        return None
    return data
    
