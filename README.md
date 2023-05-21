# tune-api
## API microservice for Tune-Music-App [JWT authorization required].
### How to get AccessToken and RefreshToken?
* Use tune-auth microservice for this.
### What this microservice do?
* This is a **CRUD** application for UsersData, TracksData and PlaylistsData inside of Tune-Music-App.<br>
<sub>Read the documentation for more information.</sub>
### Where can i read documentation?
* Check out documentation on https://documenter.getpostman.com/view/27286123/2s93m1bQam
### How can i run it?
* Run a PostgreSQL server and create database in it.
* Clone this repo and customize DB setting in */tune-api/server/settings.py*
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'tunedb',
        'USER': 'user',
        'PASSWORD': 'password',
        'HOST': '127.0.0.1',
        'PORT': 8000,
    }
}
```
* Clone tune-auth repo and customize */tune-auth/server/settings.py*. Add microservice_secret_codes in it.
```python
MICEROSERVICE_SECRET_CODES = {
  'Tune-API':'yoursecretcode',
}
```
* Customize server adress in *tune-api/tune_api/auth.py*
```python
AUTH_SERVER = 'http://yourhost:5000/auth/'
SECRET_KEY = 'yoursecretkey'
```
* Start both servers at the specified addresses.
```ShellSession
/home/tune-api> python manage.py runserver 127.0.0.1:8000
```
```ShellSession
/home/tune-auth> python manage.py runserver 127.0.0.1:5000
```
### Where can i try it as i client?
* We didn't deploy yet.