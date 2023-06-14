import os
import requests

API_SERVER = 'http://' + os.environ.get('api', 'api') + ':5000/api/'
AUTH_SECRET_KEY = os.environ.get('AUTH_SECRET_KEY', 'some-secret-key')


def create_new_profile(username):
    url = f'{API_SERVER}user/create/'
    print(url)
    response = requests.post(f'{API_SERVER}user/create/', headers={'Secret-Key':AUTH_SECRET_KEY}, json={"username":username})
    if response.status_code == 200:
        return True
    
    print(f'statusCode={response.status_code}')
    return False