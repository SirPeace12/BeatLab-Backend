from flask import request,jsonify, session
from azure.storage.blob import  BlobSasPermissions, generate_blob_sas
from datetime import datetime, timedelta
from config import container_client_song, container_client_images_song, blob_service_client, CONTAINER_NAME_SONG, CONTAINER_NAME_IMAGES_SONG
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
        expiry=datetime.utcnow() + timedelta(hours=720))  # Expiración del token de SAS )
    return f"https://{blob_service_client.account_name}.blob.core.windows.net/{CONTAINER_NAME_IMAGES_SONG}/{file.filename}?{sas_token}"

def generateSongURL(file):
    sas_token = generate_blob_sas(
        account_name = blob_service_client.account_name,
        container_name = CONTAINER_NAME_SONG,
        blob_name = file.filename,
        account_key = blob_service_client.credential.account_key,
        permission = BlobSasPermissions(read=True),  # Permiso para leer el archivo
        expiry=datetime.utcnow() + timedelta(hours=720))  # Expiración del token de SAS )
    return f"https://{blob_service_client.account_name}.blob.core.windows.net/{CONTAINER_NAME_SONG}/{file.filename}?{sas_token}"
    
def createSongDataBase(songData, user, songURL,imageSongURL):
    userEmail = user
    song =Song(title = songData["title"],
          artist = songData["artist"],
          gender = songData["gender"],
          songURL = songURL,
          imageSongURL = imageSongURL,
          user = userEmail,
          )
    song.save()

def upload(email):
    songData = {
        "title": request.form.get('title'),
        "artist": request.form.get('artist'),
        "gender": request.form.get('gender'),
        "fileSong":  request.files['fileSong'],
        "fileImage":  request.files['fileImage'],
    }
    songData["fileSong"].filename = newName(songData["fileSong"].filename)
    songData["fileImage"].filename = newName(songData["fileImage"].filename)

    uploadSongServer(songData["fileSong"])
    uploadSongImagesServer(songData["fileImage"])

    songURL = generateSongURL(songData["fileSong"])
    imageSongURL = generatePhotoSongURL(songData["fileImage"])

    createSongDataBase(songData,email ,songURL,imageSongURL)

    return jsonify({"Upload": "Successfull"})

def getAllSongs(email):
    userData = email
    songs = Song.objects(user=userData)
    songList = []
    for song in songs:
        songData = {
            'id' : str(song.id),
            'title' : song.title,
            'artist' : song.artist,
            'gender' : song.gender,
            'favorite' : song.favorite,
            'songURL' : song.songURL,
            'imageSongURL' : song.imageSongURL,
            'user' : song.user,
        }
        songList.append(songData)

    return jsonify({"SongsAll" : songList })

def listFavorites(email):
    user = email
    songs = Song.objects(favorite = True, user=user)
    songList = []

    for song in songs:
        songData = {
            'id' : str(song.id),
            'title' : song.title,
            'artist' : song.artist,
            'gender' : song.gender,
            'favorite' : song.favorite,
            'songURL' : song.songURL,
            'imageSongURL' : song.imageSongURL,
        }
        songList.append(songData)

    return jsonify({"SongsFavorites" :songList })
    
def favorite(email):
    songData = {
        'title' : request.json["title"],
    }

    user = email

    song = Song.objects(title =songData["title"], user=user).first()
    
    if (song.favorite):
        song.favorite = False
    else:
        song.favorite = True
    song.save()

    return jsonify({"SongFavorite" : "Successfull"})

def searchGender(email):
    songData = {
        'gender': request.json["gender"],
    }

    user = email
    songs = Song.objects(gender = songData["gender"], user=user)
    songList = []

    for song in songs:
        songData = {
            'id' : str(song.id),
            'title' : song.title,
            'artist' : song.artist,
            'gender' : song.gender,
            'favorite' : song.favorite,
            'songURL' : song.songURL,
            'imageSongURL' : song.imageSongURL,
        }
        songList.append(songData)

    return jsonify({"SearchGender" :songList })

def searchTitle(email):
    songData = {
        'title': request.json["title"],
    }

    user = email
    songs = Song.objects(title = songData["title"], user=user)
    songList = []

    for song in songs:
        songData = {
            'id' : str(song.id),
            'title' : song.title,
            'artist' : song.artist,
            'gender' : song.gender,
            'favorite' : song.favorite,
            'songURL' : song.songURL,
            'imageSongURL' : song.imageSongURL,
        }
        songList.append(songData)

    return jsonify({"SearchTitle" :songList })

def play(email):
    songData = {
        "title" : request.json["title"]
    }
    user = email

    song = Song.objects(title = songData["title"], user=user).first()

    songURL = song.songURL

    return jsonify({"PlaySong" : songURL})

def exist(data):
    return True if not data == None else False 

def updateArtist(email):
    songData = {
        "artist" : request.json["artist"],
        "title" : request.json["title"],
        "newArtist" : request.json["newArtist"]

    }

    song = Song.objects(artist = songData["artist"], user=email,  title=songData["title"]).first()
    if exist(song):
        song.artist = songData["newArtist"]
        song.save()
        return jsonify({"updateArtist" : "Update Artist Successful"})
    else:
        return jsonify({"updateArtist" : "Update Artist Failed"})

def updateTitle(email):
    songData = {
        "artist" : request.json["artist"],
        "title" : request.json["title"],
        "newTitle" : request.json["newTitle"]
    }

    song = Song.objects(artist = songData["artist"], user=email,  title=songData["title"]).first()
    if exist(song):
        song.title = songData["newTitle"]
        song.save()
        return jsonify({"updateTitle" : "Update Title Successful"})
    else:
        return jsonify({"updateTitle" : "Update Title Failed"})

def updateGender(email):
    songData = {
        "artist" : request.json["artist"],
        "title" : request.json["title"],
        "newGender" : request.json["newGender"]
    }

    song = Song.objects(artist = songData["artist"], user=email,  title=songData["title"]).first()
    if exist(song):
        song.gender = songData["newGender"]
        song.save()
        return jsonify({"updateGender" : "Update Gender Successful"})
    else:
        return jsonify({"updateGender" : "Update Gender Failed"})

def deleteSong(email):
    songData = {
        "title" : request.json["title"]
    }

    song = Song.objects(user = email, title = songData["title"]).first()

    song.delete()

    return jsonify({"DeleteSong": "Song deleted successfully"})
