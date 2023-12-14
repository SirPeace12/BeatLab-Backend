from flask import request,jsonify, session
from azure.storage.blob import  BlobSasPermissions, generate_blob_sas
from datetime import datetime, timedelta
from config import container_client_song, container_client_images_song, blob_service_client, CONTAINER_NAME_SONG, CONTAINER_NAME_IMAGES_SONG, redis_client

from songs.api_v1_0.songModels import Song, CreateGenre, CreateUser
# Users
from users.api_v1_0.userModel import Users, CreateSongUser, CreatePlayListUser
from users.api_v1_0.viewsUser import *

# Genres
from genres.api_v1_0.genreModels import Genre, CreateSong
from genres.api_v1_0.viewsGenres import *

# playList
from play_list.api_v1_0.playListModel import PlaylistSong, userPlayList, CreateSongPlayList
from play_list.api_v1_0.viewsPlayList import *



from bson import ObjectId
import json

import uuid

# ------------------- SONGS -------------

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
    return f"https://{blob_service_client.account_name}.blob.core.windows.net/{CONTAINER_NAME_SONG}/{file.filename}?sp=r&st=2023-12-14T04:32:08Z&se=2023-12-14T12:32:08Z&spr=https&sv=2022-11-02&sr=c&sig=Mfs2LyJOBL3D%2BTBxFQ3jVqIB%2Fu0Biz4OwmHpE87hjbc%3D"

def songDataRedis(email):
    songs = Users.objects(email = email).first().songs
    song_list = []

    for song in songs:
        song_data = {
            'id_song': str(song._id),
            'title': song.title,
            'artist': song.artist,
            'genres': [{'id_gender': str(genre._id), 'description': genre.description} for genre in song.genres],
            'songURL': song.songURL,
            'imageSongURL': song.imageSongURL,
        }
        song_list.append(song_data)
    redis_client.set(email, json.dumps(song_list))

def createSongDataBase(songData, user, songURL,imageSongURL):
    genre = Genre.objects(id=ObjectId(songData["genre"])).first()

    users = Users.objects(email=user).first()

    song =Song(title = songData["title"],
          artist = songData["artist"],
          genres = [CreateGenre(_id=genre.id, description = genre.description)],
          songURL = songURL,
          imageSongURL = imageSongURL,
          user = CreateUser(_id=users.id, nameUser = users.nameUser, lastNameUser = users.lastNameUser, email = users.email, phone = users.phone),
          )
    song.save()
    
    genreUpdate(songData, song)
    userUpdate(users, song)
    songDataRedis(user)
    redis_client.set('totalSong', len(Song.objects.all()))

def upload(email):
    songData = {
        "title": request.form.get('title'),
        "artist": request.form.get('artist'),
        "genre": request.form.get('genre'),
        "fileSong":  request.files['fileSong'],
        "fileImage":  request.files['fileImage'],
    }
    songData["fileSong"].filename = newName(songData["fileSong"].filename)
    songData["fileImage"].filename = newName(songData["fileImage"].filename)

    uploadSongServer(songData["fileSong"])
    # uploadSongImagesServer(songData["fileImage"])

    songURL = generateSongURL(songData["fileSong"])
    imageSongURL = generatePhotoSongURL(songData["fileImage"])

    createSongDataBase(songData,email ,songURL,imageSongURL)

    return jsonify({"Upload": "Successfull"})

def getAllSongs(email):
    songs = Users.objects(email=email).first().songs
    songList = []
    if songs:
        for song in songs:
            songData = {
                'id_song' : str(song._id),
                'title' : song.title,
                'artist' : song.artist,
                'genre' : [{"id_genre": str(genre._id), "description": genre.description} for genre in song.genres],
                'songURL' : song.songURL,
                'imageSongURL' : song.imageSongURL
            }
            songList.append(songData)
        return jsonify({"SongsAll" : songList })
    else:
        return jsonify({"message" : "User Not Found" })

    

def getAllSongsRedis(email):
    songs_bytes = redis_client.get(email)

    # Decodificar los bytes a una cadena
    songs_str = songs_bytes.decode('utf-8')

    # Cargar la cadena como objeto JSON
    songs = json.loads(songs_str)

    return jsonify({"SongsAll": songs})

def searchTitle(email):
    songData = {
        'title': request.json["title"],
    }

    songs = Song.objects(title = songData["title"])
    songList = []

    for song in songs:
        if song.user.email == email:
            songData = {
                'id' : str(song.id),
                'title' : song.title,
                'artist' : song.artist,
                'genres' : [{"id_genre": str(genre._id), "description": genre.description} for genre in song.genres],
                'songURL' : song.songURL,
                'imageSongURL' : song.imageSongURL,
            }
            songList.append(songData)

    return jsonify({"SearchTitle" :songList })

def play(email):
    songData = {
        "title" : request.json["title"]
    }
    user = Users.objects(email=email).first()
    if user :

        song = next((s for s in user.songs if s.title == songData['title']), None)

        if song:
            song_url = song.songURL
            return jsonify({"PlaySong": song_url})
        else:
            return jsonify({"message": "Song not found"})
    else:
            return jsonify({"message": "User not found"})


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

# -------------------------- GENRES ---------

def addGenreSong(genre, song):
    song = Song.objects(id=song.id).first()
    song.genres = song.genres + [CreateGenre(_id=genre.id, description = genre.description)]

    song.save()


def newGenre(user, genre, song):
    addGenreSongUser(user, genre, song)
    addGenreSong(genre, song)
    addSongGenre(genre, song)
    addGenrePlayList(user, genre, song)
    songDataRedis(user.email)


def addGenre(email):
    songData = {
        "id_song" : request.json["id_song"],
        "id_genre" : request.json["id_genre"]
    }

    song = Song.objects(id = ObjectId(songData['id_song'])).first()
    genre = Genre.objects(id = ObjectId(songData['id_genre'])).first()
    user = Users.objects(email = email).first()

    # if exist(song):
    newGenre(user, genre, song)
    return jsonify({"updateGender" : "Update Gender Successful"})
    # else:
    #     return jsonify({"updateGender" : "Update Gender Failed"})

def newTitleSong(title, song):
    song = Song.objects(id=song.id).first()
    song.title = title
    song.save()

def newTitle(user, title, song):
    newTitleSongUser(user, title, song)
    newTitleSong(title, song)
    newTitleGenre(title, song)
    newTitlePlayList(user, title, song)
    songDataRedis(user.email)


def updateTitle(email):
    songData = {
        "id_song" : request.json["id_song"],
        "title" : request.json["title"]
    }

    song = Song.objects(id = ObjectId(songData['id_song'])).first()
    user = Users.objects(email = email).first()

    newTitle(user, songData['title'], song)
    return jsonify({"updateGender" : "Update Gender Successful"})

def newArtistSong(artist, song):
    song = Song.objects(id=song.id).first()
    song.artist = artist
    song.save()

def newArtist(user, artist, song):
    newArtistSongUser(user, artist, song)
    newArtistSong(artist, song)
    newArtistGenre(artist, song)
    newArtistPlayList(user, artist, song)
    songDataRedis(user.email)


def updateArtist(email):
    songData = {
        "id_song" : request.json["id_song"],
        "artist" : request.json["artist"]
    }

    song = Song.objects(id = ObjectId(songData['id_song'])).first()
    user = Users.objects(email = email).first()

    newArtist(user, songData['artist'], song)
    return jsonify({"updateGender" : "Update Gender Successful"})
    
def totalUserSongs(email):
    user = Users.objects(email=email).first()
    if user :
        totalSongs= len(user.songs)
        key = f'TotalUserSongs:{email}'
        
        redis_client.set(key, totalSongs)

        return jsonify({"TotalUserSongs": totalSongs})
    else:
        return jsonify({"message": "User Not Found"})

def totalUserSongsRedis(email):
    key = f'TotalUserSongs:{email}'
    totalSongs =  redis_client.get(key)
    songs_str = totalSongs.decode('utf-8')
    return jsonify({"TotalUserSongs": int(songs_str)})

def totalSongs():
    songs = Song.objects.all()
    totalSong = len(songs)
    redis_client.set('totalSong', totalSong)
    return jsonify({"TotalSongs": totalSong})

def totalSongsRedis():
    totalSongs =  redis_client.get('totalSong')
    songs_str = totalSongs.decode('utf-8')
    return jsonify({"TotalSongs": int(songs_str)})

def exist(data):
    return True if not data == None else False 


