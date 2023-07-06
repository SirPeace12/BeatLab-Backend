from flask import Flask, request,jsonify, session
from azure.storage.blob import BlobServiceClient, BlobSasPermissions, generate_blob_sas
from datetime import datetime, timedelta
from config import container_client_song,container_client_images_song, blob_service_client, CONTAINER_NAME_SONG, CONTAINER_NAME_IMAGES_SONG
from songs.api_v1_0.songModels import Song
import uuid

def uploadSongServer(file):
    container_client_song.get_blob_client(file.filename).upload_blob(file)
    
def uploadSongImagesServer(file):
    container_client_images_song.get_blob_client(file.filename).upload_blob(file)

def newName(filename):
    return f"{str(uuid.uuid4())}_{filename}"

def generatePhotoSongURL(file):
    sas_token = generate_blob_sas(
        account_name = blob_service_client.account_name,
        container_name = CONTAINER_NAME_IMAGES_SONG,
        blob_name = file.filename,
        account_key = blob_service_client.credential.account_key,
        permission = BlobSasPermissions(read=True),  # Permiso para leer el archivo
        expiry=datetime.utcnow() + timedelta(hours=1))  # Expiración del token de SAS )
    return f"https://{blob_service_client.account_name}.blob.core.windows.net/{CONTAINER_NAME_IMAGES_SONG}/{file.filename}?{sas_token}"


def generateSongURL(file):
    sas_token = generate_blob_sas(
        account_name = blob_service_client.account_name,
        container_name = CONTAINER_NAME_SONG,
        blob_name = file.filename,
        account_key = blob_service_client.credential.account_key,
        permission = BlobSasPermissions(read=True),  # Permiso para leer el archivo
        expiry=datetime.utcnow() + timedelta(hours=1))  # Expiración del token de SAS )
    return f"https://{blob_service_client.account_name}.blob.core.windows.net/{CONTAINER_NAME_SONG}/{file.filename}?{sas_token}"
    
def createSongDataBase(songData,songURL,imageSongURL):
    userEmail = session.get('user')
    song =Song(title = songData["title"],
          artist = songData["artist"],
          gender = songData["gender"],
          songURL = songURL,
          imageSongURL = imageSongURL,
          user = userEmail,
          )
    song.save()

def upload():
    songData = {
        "title": request.form.get('title'),
        "artist": request.form.get('artist'),
        "gender": request.form.get('gender'),
        "fileSong":  request.files['fileSong'],
        "fileImage":  request.files['fileImage'],
    }
    print(songData["fileSong"].filename)
    songData["fileSong"].filename = newName(songData["fileSong"].filename)
    print(songData["fileSong"].filename)

    print("---------")

    print(songData["fileImage"].filename)

    songData["fileImage"].filename = newName(songData["fileImage"].filename)
    print(songData["fileImage"].filename)


    uploadSongServer(songData["fileSong"])
    uploadSongImagesServer(songData["fileImage"])

    songURL = generateSongURL(songData["fileSong"])
    imageSongURL = generatePhotoSongURL(songData["fileImage"])

    createSongDataBase(songData,songURL,imageSongURL)

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
            'imageSongURL' : song.imageSongURL,
        }
        songList.append(songData)

    return jsonify({"Songs All" : songList })

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
            'imageSongURL' : song.imageSongURL,
        }
        songList.append(songData)

    return jsonify({"Songs Favorites" :songList })
    
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

    return jsonify({"Song Favorite" : "Successfull"})

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
            'imageSongURL' : song.imageSongURL,
        }
        songList.append(songData)

    return jsonify({"Search gender" :songList })

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
            'imageSongURL' : song.imageSongURL,
        }
        songList.append(songData)

    return jsonify({"Search title" :songList })

def play():
    songData = {
        "title" : request.json["title"]
    }
    user = session.get('user')

    song = Song.objects(title = songData["title"], user=user).first()

    songURL = song.songURL

    return jsonify({"Play Song" : songURL})

# metodos para modificar atributos 

def modifyTitle():
    songData = {
        "title" : request.json["title"],
    }



