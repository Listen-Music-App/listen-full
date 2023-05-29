# tune-auth
## AUTH microservice for Tune-Music-App.
### How to get AccessToken and RefreshToken?
* Use /auth/register/ to register your self on server.
* Use /auth/login/ to login and get Access and Refresh tokens.
### What this microservice do?
* This server can identify, authenticate and authorize users.
* This server can let another microservice know if a user with the given nickname exists.<br>
<sub>Read the documentation for more information.</sub>
### Where can i read documentation?
* Check out documentation on https://documenter.getpostman.com/view/27286123/2s93m1bQp7
### How can i run it?
* Clone this repo and customize */tune-auth/server/settings.py*. Add microservice_secret_codes in it.<br>
<sub>This is needed to authorize other microservices</sub>
```python
MICEROSERVICE_SECRET_CODES = {
  'microservicename':'yoursecretcode',
}
```
* Start server.
```ShellSession
/home/tune-auth> python manage.py runserver 127.0.0.1:5000
```
### Where can i try it as a client?
* We didn't deploy yet.
