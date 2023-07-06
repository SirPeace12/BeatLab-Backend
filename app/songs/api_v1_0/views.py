from flask import Flask, request,jsonify, session
from azure.storage.blob import BlobServiceClient, BlobSasPermissions, generate_blob_sas
from datetime import datetime, timedelta
from config import container_client, blob_service_client,CONTAINER_NAME
from songs.api_v1_0.songModels import Song
import uuid

def uploadServer(file):
    container_client.get_blob_client(file.filename).upload_blob(file)

def newName(filename):
    return f"{str(uuid.uuid4())}_{filename}"

def generateSongURL(file):
    sas_token = generate_blob_sas(
        account_name = blob_service_client.account_name,
        container_name = CONTAINER_NAME,
        blob_name = file.filename,
        account_key = blob_service_client.credential.account_key,
        permission = BlobSasPermissions(read=True),  # Permiso para leer el archivo
        expiry=datetime.utcnow() + timedelta(hours=1))  # Expiración del token de SAS )
    return f"https://{blob_service_client.account_name}.blob.core.windows.net/{CONTAINER_NAME}/{file.filename}?{sas_token}"
    
def createSongDataBase(songData,songURL):
    userEmail = session.get('user')
    song =Song(title = songData["title"],
          artist = songData["artist"],
          gender = songData["gender"],
          songURL = songURL,
          user = userEmail,
          )
    song.save()

def upload():
    songData = {
        "title": request.form.get('title'),
        "artist": request.form.get('artist'),
        "gender": request.form.get('gender'),
        "file":  request.files['file'],
    }
    songData["file"].filename = newName(songData["file"].filename)
    
    uploadServer(songData["file"])
    
    songURL = generateSongURL(songData["file"])
    createSongDataBase(songData,songURL)

    return jsonify({"Upload": "Successfull"})

def getAllSongs():
    songs = Song.objects(user=session.get('user'))
    songList = []
    for song in songs:
        songData = {
            'title' : song.title,
            'artist' : song.artist,
            'gender' : song.gender,
            'favorite' : song.favorite,
            'songURL' : song.songURL,
        }
        songList.append(songData)

    return jsonify({"SongsAll" : songList })

def listFavorites():
    user = session.get('user')
    songs = Song.objects(favorite = True, user=user)
    songList = []

    for song in songs:
        songData = {
            'title' : song.title,
            'artist' : song.artist,
            'gender' : song.gender,
            'favorite' : song.favorite,
            'songURL' : song.songURL,
        }
        songList.append(songData)

    return jsonify({"SongsFavorites" :songList })
    
def favorite():
    songData = {
        'title' : request.json["title"],
    }

    user = session.get('user')

    song = Song.objects(title =songData["title"], user=user).first()
    
    if (song.favorite):
        song.favorite = False
    else:
        song.favorite = True
    song.save()

    return jsonify({"SongFavorite" : "Successfull"})

def searchGender():
    songData = {
        'gender': request.json["gender"],
    }

    user = session.get('user')
    songs = Song.objects(gender = songData["gender"], user=user)
    songList = []

    for song in songs:
        songData = {
            'title' : song.title,
            'artist' : song.artist,
            'gender' : song.gender,
            'favorite' : song.favorite,
            'songURL' : song.songURL,
        }
        songList.append(songData)

    return jsonify({"SearchGender" :songList })

def searchTitle():
    songData = {
        'title': request.json["title"],
    }

    user = session.get('user')
    songs = Song.objects(title = songData["title"], user=user)
    songList = []

    for song in songs:
        songData = {
            'title' : song.title,
            'artist' : song.artist,
            'gender' : song.gender,
            'favorite' : song.favorite,
            'songURL' : song.songURL,
        }
        songList.append(songData)

    return jsonify({"SearchTitle" :songList })

def play():
    songData = {
        "title" : request.json["title"]
    }
    user = session.get('user')

    song = Song.objects(title = songData["title"], user=user).first()

    songURL = song.songURL

    return jsonify({"PlaySong" : songURL})