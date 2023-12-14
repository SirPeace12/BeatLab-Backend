from azure.storage.blob import  BlobSasPermissions, generate_blob_sas
from datetime import datetime, timedelta
from config import container_client_song, container_client_images_song, blob_service_client, CONTAINER_NAME_SONG, CONTAINER_NAME_IMAGES_SONG, redis_client

from songs.api_v1_0.songModels import Song, CreateGenre, CreateUser
# Users
from users.api_v1_0.userModel import Users, CreateSongUser, CreatePlayListUser
from users.api_v1_0.viewsUser import *

# Genres
from genres.api_v1_0.genreModels import Genre, CreateSong

# playList
from play_list.api_v1_0.playListModel import PlaylistSong, userPlayList, CreateSongPlayList


from bson import ObjectId
import json

import uuid

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

# def allGenres ():


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

def allGenres():
    genres = Genre.objects.all()
    getGenres= []
    for genre in genres:
        data = {
            "id_genre":str(genre.id),
            "description":genre.description
        }
        getGenres.append(data)

    redis_client.set('allGenres', json.dumps(getGenres))

    return jsonify({"allGenres": getGenres})    

def allGenresRedis():
    genres = redis_client.get('allGenres')
    genres_str = genres.decode('utf-8')
    genres = json.loads(genres_str)
    return jsonify({"allGenresRedis": genres})   

def createGenre():
    genre = Genre(description = request.json['description'],
                  songs = [])
    genre.save()

    return jsonify({"Genre": "Successfull"})

def searchGenres(email):
    songData = {
        'id_genre':request.json["id_genre"],
    }

    data = Genre.objects(id = songData["id_genre"]).first()
    if data :
        songs = data.songs
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
        
        redis_client.set('SearchGender', json.dumps(songList))
        return jsonify({"SearchGender" :songList })
    
    return jsonify({"SearchGender" : "Genre Not Found" })

def searchGenresRedis():
    sg = redis_client.get('SearchGender')
    songs_str = sg.decode('utf-8')
    songs = json.loads(songs_str)
    return jsonify({"SearchGender": songs})  

def addSongGenre(genre, song):
    genre = Genre.objects(id = genre.id).first()
    genre.songs.append(CreateSong(_id=song.id, 
                                        title = song.title, 
                                        artist = song.artist, 
                                        songURL = song.songURL,
                                        imageSongURL = song.imageSongURL,
                                        user = song.user,))
    genre.save()

def newTitleGenre(title, song):
    genres = Genre.objects.all()
    for genre in genres:
        for sg in genre.songs:
            if sg._id == song.id:
                sg.title = title
    genre.save()

def newArtistGenre(artist, song):
    genres = Genre.objects.all()
    for genre in genres:
        for sg in genre.songs:
            if sg._id == song.id:
                sg.artist = artist
    genre.save()

def getGenreSongs():
    songData = {
        'id_genre' : request.json["id_genre"],
    }
    genre = Genre.objects(id = songData['id_genre']).first()
    if(genre):
        key = f'TotalSongsPerGenre:{genre.description}'

        redis_client.set(key, json.dumps(len(genre.songs)))

        return jsonify({"Total Sogs Per Genre" : len(genre.songs) })
    else:
        return jsonify({"message" : "Genre Not Found"})


def getGenreSongsRedis():
    songData = {
        'description' : request.json["description"],
    }
    description =songData['description']
    key = f'TotalUserSongs:{description}'
    totalSongs = redis_client.get(key)
    if totalSongs:
        songs_str = totalSongs.decode('utf-8')
        return jsonify({"Total Sogs Per Genre" : int(songs_str) })
    else:
        return jsonify({"messge" : "Description Not Found" })



def totalSongPerGenre():
    genres = Genre.objects.all()
    genre_counts = {}

    for genre in genres:
        genre_counts[genre.description] = len(genre.songs)

    redis_client.set('GenreCounts', json.dumps(genre_counts))

    return jsonify({"GenreCounts": genre_counts})

def totalSongPerGenreRedis():
    countSongs = redis_client.get('GenreCounts')
    totalSongs = countSongs.decode('utf-8')
    total = json.loads(totalSongs)
    return jsonify({"Total Sogs Per Genre" : total })

