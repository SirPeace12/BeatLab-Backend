from flask import request,jsonify, session
from azure.storage.blob import  BlobSasPermissions, generate_blob_sas
from datetime import datetime, timedelta
from config import container_client_song, container_client_images_song, blob_service_client, CONTAINER_NAME_SONG, CONTAINER_NAME_IMAGES_SONG, redis_client
from songs.api_v1_0.songModels import Song, CreateGenre, CreateUser
from users.api_v1_0.userModel import Users, CreateSongUser, CreatePlayListUser
from users.api_v1_0.viewsUser import *

from genres.api_v1_0.genreModels import Genre, CreateSong
from play_list.api_v1_0.playListModel import PlaylistSong, userPlayList, CreateSongPlayList
from bson import ObjectId
import json

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

def userUpdate(user, song):
    user.songs = user.songs + [CreateSongUser(_id=song.id, 
                                        title = song.title, 
                                        artist = song.artist, 
                                        genres = song.genres ,
                                        songURL = song.songURL,
                                        imageSongURL = song.imageSongURL)]
    user.save()
    userDataRedis(user)
    key = f'TotalUserSongs:{user.email}'
    redis_client.set(key, len(user.songs))


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

def addGenreSongUser(user, genre, song):
    for sg in user.songs:
        if sg._id == song.id:
            sg.genres = sg.genres + [CreateGenre(_id=genre.id, description = genre.description)]
    user.save()
    addPlayList(user, genre, song)

def addPlayList(user, genre, song):
    playLists = user.playlist_songs
    for playList in playLists:
            for sg in playList.songs:
                if sg._id == song.id:
                    sg.genres.append(CreateGenre(_id=genre.id, description = genre.description))
    user.save()

def updateDescriptionUser(email, playlist, description):
    user = Users.objects(email=email).first()
    for pl in user.playlist_songs:
        if pl._id == playlist:
            pl.description = description
    user.save()

def updatePlaylistNameUser(email, playlist, playlistName):
    user = Users.objects(email=email).first()
    for pl in user.playlist_songs:
        if pl._id == playlist:
            pl.playlistName = playlistName
    user.save()

def addPTitlelayList(user, title, song):
    playLists = user.playlist_songs
    for playList in playLists:
            for sg in playList.songs:
                if sg._id == song.id:
                    sg.title = title
    user.save()

def newTitleSongUser(user, title, song):
    for sg in user.songs:
        if sg._id == song.id:
            sg.title = title
    user.save()
    addPTitlelayList(user, title, song)

def addArtistlayList(user, artist, song):
    playLists = user.playlist_songs
    for playList in playLists:
            for sg in playList.songs:
                if sg._id == song.id:
                    sg.artist = artist
    user.save()

def newArtistSongUser(user, artist, song):
    for sg in user.songs:
        if sg._id == song.id:
            sg.artist = artist
    user.save()
    addArtistlayList(user, artist, song)

def getUserGenres():
    all_users_genres = []
    for user in Users.objects:
        user_genres = {"user": user.email, "genres": set()}

        for song in user.songs:
            for genre in song.genres:
                genre_tuple = ("genero", genre.description)
                user_genres["genres"].add(genre_tuple)
        user_genres["genres"] = list(user_genres["genres"])
        all_users_genres.append(user_genres)

    redis_client.set('getUserGenres',json.dumps(all_users_genres) )

    return jsonify({"AllUsersGenres": all_users_genres})

def getUserGenresRedis():
    all_users_genres = redis_client.get('getUserGenres')
    all_users_genres_str = all_users_genres.decode('utf-8')
    salida = json.loads(all_users_genres_str)
    return jsonify({"allGenresRedis": salida})   