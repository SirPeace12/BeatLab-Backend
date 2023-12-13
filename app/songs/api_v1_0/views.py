from flask import request,jsonify, session
from azure.storage.blob import  BlobSasPermissions, generate_blob_sas
from datetime import datetime, timedelta
from config import container_client_song, container_client_images_song, blob_service_client, CONTAINER_NAME_SONG, CONTAINER_NAME_IMAGES_SONG, redis_client
from songs.api_v1_0.songModels import Song, CreateGenre, CreateUser
from authentication.api_v1_0.userModel import Users, CreateSongUser, CreatePlayListUser
from songs.api_v1_0.genreModels import Genre, CreateSong
from songs.api_v1_0.playListModel import PlaylistSong, userPlayList, CreateSongPlayList
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
    return f"https://{blob_service_client.account_name}.blob.core.windows.net/{CONTAINER_NAME_SONG}/{file.filename}?{sas_token}"

def songDataRedis():
    songs = Song.objects.all()
    song_list = []

    for song in songs:
        song_data = {
            'id': str(song.id),
            'title': song.title,
            'artist': song.artist,
            'genres': [{'_id': str(genre._id), 'description': genre.description} for genre in song.genres],
            'songURL': song.songURL,
            'imageSongURL': song.imageSongURL,
            'user': {
                '_id': str(song.user._id),
                'nameUser': song.user.nameUser,
                'lastNameUser': song.user.lastNameUser,
                'email': song.user.email,
                'phone': song.user.phone
            }
        }
        song_list.append(song_data)
    redis_client.set('allUserSongs', json.dumps(song_list))

def genreDataRedis():
    genres = Genre.objects.all()
    genres_list = []

    for genre in genres:
        genre_data = {
            'id_genre': str(genre.id),
            'description': genre.description,
            'songs': [{'_id' : str(song._id), 
                       'title' : song.title, 
                       'artist' : song.artist, 
                       'songURL' : song.songURL, 
                       'imageSongURL' : song.imageSongURL,
                       'user' : {'_id' : str(song.user._id), 'nameUser' : song.user.nameUser, 'lastNameUser' : song.user.lastNameUser, 'email' : song.user.email, 'phone' : song.user.phone}}

                       for song in genre.songs]
            }
        genres_list.append(genre_data)
    redis_client.set('allGenres', json.dumps(genres_list))

def userDataRedis(user):
    user_data = {
        'nameUser' : user.nameUser,
        'lastNameUser' : user.lastNameUser,
        'email' : user.email,
        'phone' : user.phone,
        'playlist_songs' : [{'_id_playlist' : str(playlist._id), 
                       'playlistName' : playlist.playlistName, 
                       'description' : playlist.description, 
                       'songs' : [{'_id_song' : str(song._id),
                                   'title' : song.title,
                                   'artist' : song.artist,
                                   'genres' : [{
                                       '_id_genre' : str(genre._id),
                                       'description' : genre.description
                                   } for genre in song.genres],
                                   'songURL' : song.songURL,
                                   'imageSongURL' : song.imageSongURL,
                                   } for song in playlist.songs] 
                       }
                       for playlist in user.playlist_songs],
        'userPhotoURL' : user.userPhotoURL,
        'songs' : [{'_id_song' : str(song._id),
                                   'title' : song.title,
                                   'artist' : song.artist,
                                   'genres' : [{
                                       '_id_genre' : str(genre._id),
                                       'description' : genre.description
                                   } for genre in song.genres],
                                   'songURL' : song.songURL,
                                   'imageSongURL' : song.imageSongURL,
                                   } for song in user.songs] 
    }
    redis_client.set('user', json.dumps(user_data))

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

    songDataRedis()
    genreUpdate(songData, song)
    userUpdate(users, song)

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

    # uploadSongServer(songData["fileSong"])
    # uploadSongImagesServer(songData["fileImage"])

    songURL = generateSongURL(songData["fileSong"])
    imageSongURL = generatePhotoSongURL(songData["fileImage"])

    createSongDataBase(songData,email ,songURL,imageSongURL)

    return jsonify({"Upload": "Successfull"})

def getAllSongs(email):
    songs = Users.objects(email=email).first().songs
    songList = []
    for song in songs:
        songData = {
            'id_song' : str(song._id),
            'title' : song.title,
            'artist' : song.artist,
            'genre' : [{"id_genre": str(genre._id), "description": genre.description} for genre in song.genres],
            # 'favorite' : song.favorite,
            'songURL' : song.songURL,
            'imageSongURL' : song.imageSongURL
        }
        songList.append(songData)
    return jsonify({"SongsAll" : songList })

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

    song = next((s for s in user.songs if s.title == songData['title']), None)

    if song:
        song_url = song.songURL
        return jsonify({"PlaySong": song_url})
    else:
        return jsonify({"error": "Song not found"})



# TODO AJUSTAR
def deleteSong(email):
    songData = {
        "title" : request.json["title"]
    }

    song = Song.objects(user = email, title = songData["title"]).first()

    song.delete()

    return jsonify({"DeleteSong": "Song deleted successfully"})

# TODO AJUSTAR

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

# TODO AJUSTAR

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

# def UpdateSongPlayList(user,  id_play_list, song):
#     user.playlist_songs = user.playlist_songs + [CreatePlayListUser(_id=play_list.id, 
#                                         playlistName = play_list.playlistName, 
#                                         description = play_list.description,
#                                         songs = play_list.songs)]
#     user.save()


#  ------------------- PLAY LIST----------
def createPlayList(email):
    user = Users.objects(email=email).first()

    play_list_data = {
        "playlistName": request.json['playlistName'],
        "description": request.json['description']
    }
    print(play_list_data)
    play_list = PlaylistSong(playlistName=play_list_data['playlistName'], 
                             description=play_list_data['description'], 
                             songs =[], 
                             user = userPlayList(_id = user.id, 
                                                 nameUser = user.nameUser, 
                                                 lastNameUser = user.lastNameUser, 
                                                 email = user.email, 
                                                 phone = user.phone))
    
    play_list.save()
    userUpdatePlayList(user, play_list)

    return jsonify({"message": "PlayListSuccefull"})

def addSong(email):
    songData = {
        "id_song" : request.json["id_song"],
        "id_play_list" : request.json["id_play_list"],
    }

    song = Song.objects(id = ObjectId(songData["id_song"])).first()
    user = Users.objects(email=email).first()
    playList = PlaylistSong.objects(id = ObjectId(songData["id_play_list"])).first()
    playList.songs = playList.songs + [CreateSongPlayList(_id=song.id, 
                                        title = song.title, 
                                        artist = song.artist, 
                                        genres = song.genres ,
                                        songURL = song.songURL,
                                        imageSongURL = song.imageSongURL)]
    playList.save()
    userUpdateSongPlayList(user, songData["id_play_list"], song)
   

    return jsonify({"message": "AddSongSuccessfull"})


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

# --------------- USER -----------
def userUpdate(user, song):
    user.songs = user.songs + [CreateSongUser(_id=song.id, 
                                        title = song.title, 
                                        artist = song.artist, 
                                        genres = song.genres ,
                                        songURL = song.songURL,
                                        imageSongURL = song.imageSongURL)]
    user.save()
    userDataRedis(user)


def userUpdatePlayList(user, play_list):
    user.playlist_songs = user.playlist_songs + [CreatePlayListUser(_id=play_list.id, 
                                        playlistName = play_list.playlistName, 
                                        description = play_list.description,
                                        songs = play_list.songs)]
    user.save()

def userUpdateSongPlayList(user,  id_play_list, song):
    for playList in user.playlist_songs:
        if playList._id == ObjectId(id_play_list):
            playList.songs = playList.songs + [CreateSongUser(_id=song.id, 
                                        title = song.title, 
                                        artist = song.artist, 
                                        genres = song.genres ,
                                        songURL = song.songURL,
                                        imageSongURL = song.imageSongURL)]
    user.save()


# -------------------------- GENRES ---------

def genreUpdate(songData, song):
    genre = Genre.objects(id=ObjectId(songData["genre"])).first()

    genre.songs = genre.songs + [CreateSong(_id=song.id, 
                                        title = song.title, 
                                        artist = song.artist, 
                                        songURL = song.songURL,
                                        imageSongURL = song.imageSongURL,
                                        user = song.user,)]
    genre.save()
    genreDataRedis()

def createGenre():
    genre = Genre(description = request.json['description'],
                  songs = [])
    genre.save()
    return jsonify({"Genre": "Successfull"})

def searchGenres(email):
    songData = {
        'id_genre':request.json["id_genre"],
        'gender': request.json["gender"],
    }

    songs = Genre.objects(id = songData["id_genre"]).first().songs
    songList = []

    for song in songs:
        if song.user.email == email:
            songData = {
            'id_song' : str(song._id),
            'title' : song.title,
            'artist' : song.artist,
            'songURL' : song.songURL,
            'imageSongURL' : song.imageSongURL
        }
            songList.append(songData)

    return jsonify({"SearchGender" :songList })

# TODO AJUSTAR
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

def exist(data):
    return True if not data == None else False 


