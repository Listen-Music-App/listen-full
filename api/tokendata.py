import jwt


def from_cookie_data(request, secret:str):
    try:
        token = request.COOKIES['JWT']
        data = jwt.decode(token, secret, algorithms='HS256')
    except:
        return None

    return data
    