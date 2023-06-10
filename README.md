# Listen-Music-App
## What is this?
* This is a music service for distributing your own and listening to other people's music, creating your own and adding other people's playlists.

## Do u have website?
* We didn't deploy yet.

## How can i try it? [no frontend yet]
* You need docker on your pc.
* Clone this repo
```shell
git clone https://github.com/Listen-Music-App/listen-full.git
```
* Run docker engine.
* Open the cloned directory and change the host in the *host.env* file. Instead of **0.0.0.0**, insert your **ipv4**.
```shell
HOST="192.168.1.2"
```
* Run docker compose. Make sure you are in the right directory.
```shell
D:\some\path\listen_full> docker compose -up --build
```
* Interact with the service using our api **[JWT authorization required]**.
<img src="https://i.imgur.com/3IBTIWw.png">