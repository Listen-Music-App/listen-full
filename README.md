# AUTH microservice for Listen-Music-App.
## How to get AccessToken and RefreshToken?
* Use /auth/register/ to register your self on server.
* Use /auth/login/ to login and get Access and Refresh tokens.
## What this microservice do?
* This server can identify, authenticate and authorize users.
* This server can let another microservice know if a user with the given nickname exists.<br>
<sub>Read the documentation for more information.</sub>

## Where can i read an API documentation?
* Check out documentation on https://documenter.getpostman.com/view/27286123/2s93m1bQp7 [old version]

## How can i run it?
* Clone this repo and customize *dockerfile*. Change API_SECRET_CODE (if you want). You may also change host and port, but this is not recomended if you want to just test it on your own PC.<br>

```dockerfile
ENV HOST=0.0.0.0 PORT=3000 API_SECRETE_CODE=some-secret-code

EXPOSE 3000
```

* Build a docker image.

```shell
docker build -t listen-auth:latest . 
```

* Run docker container
```shell
docker run -p 127.0.0.1:3000:3000/tcp -d --name listen-auth listen-auth:latest
```

## Where can i try it as a client?
* We didn't deploy yet.
* We have no frontend D:

### IF YOU WANT TO CREATE A FRONT-END FOR IT, TEXT ME ON *lengthylyova@gmail.com*
