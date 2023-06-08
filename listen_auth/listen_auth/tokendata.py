from datetime import datetime, timezone, timedelta
import jwt
from rest_framework_jwt.utils import jwt_payload_handler

from listen_auth.tokenconfig import JWT_AUTH



def access_token_generate(user:object):
    secret = JWT_AUTH['ACCESS_SECRET']
    payload = jwt_payload_handler(user)

    tz = timezone(timedelta(hours=3), 'Moscow UTC+3')
    payload['exp'] = datetime.now(tz) + JWT_AUTH['JWT_EXPIRATION_DELTA']
    expiration = payload['exp'].strftime("%d %b %Y %H:%M:%S")

    token = jwt.encode(payload, secret, algorithm='HS256').decode('utf-8')
    return token, expiration


def refresh_token_generate(user:object):
    secret = JWT_AUTH['REFRESH_SECRET']
    payload = jwt_payload_handler(user)

    tz = timezone(timedelta(hours=3), 'Moscow UTC+3')
    payload['exp'] = datetime.now(tz) + JWT_AUTH['JWT_REFRESH_EXPIRATION_DELTA']
    expiration = payload['exp'].strftime("%d %b %Y %H:%M:%S")

    token = jwt.encode(payload, secret, algorithm='HS256').decode('utf-8')
    return token, expiration


def token_data(token:str, secret):
    try:
        data = jwt.decode(token, secret, algorithms='HS256')
    except:
        return None
    return data
    
