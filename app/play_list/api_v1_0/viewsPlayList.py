from flask import request,jsonify, session
from azure.storage.blob import  BlobSasPermissions, generate_blob_sas
from datetime import datetime, timedelta
from config import container_client_song, container_client_images_song, blob_service_client, CONTAINER_NAME_SONG, CONTAINER_NAME_IMAGES_SONG, redis_client
from songs.api_v1_0.songModels import Song, CreateGenre, CreateUser
from users.api_v1_0.userModel import Users, CreateSongUser, CreatePlayListUser
from users.api_v1_0.viewsUser import *

from genres.api_v1_0.genreModels import Genre, CreateSong
from bson import ObjectId
import json

def createPlayList(email):
    user = Users.objects(email=email).first()

    play_list_data = {
        "playlistName": request.json['playlistName'],
        "description": request.json['description']
    }
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

def addGenrePlayList(user, genre, song):
    playLists = PlaylistSong.objects.all()
    for playList in playLists:
        if (playList.user.email == user.email):
            for sg in playList.songs:
                if sg._id == song.id:
                    sg.genres.append(CreateGenre(_id=genre.id, description = genre.description))
        playList.save()

def updateDescription(email):
    data ={
        "description" : request.json["description"],
        "id_play_list" : request.json["id_play_list"]
    }
    playlist = PlaylistSong.objects(id = ObjectId(data['id_play_list'])).first()

    playlist.description = data['description']
    playlist.save()

    updateDescriptionUser(email, playlist.id, data['description'])

    return jsonify({"message": "updateDescriptionSuccessfull"})

def updateName(email):
    data ={
        "playlistName" : request.json["playlistName"],
        "id_play_list" : request.json["id_play_list"]
    }
    playlist = PlaylistSong.objects(id = ObjectId(data['id_play_list'])).first()

    playlist.playlistName = data['playlistName']
    playlist.save()
    updatePlaylistNameUser(email, playlist.id, data['playlistName'])

    return jsonify({"message": "updateNameSuccessfull"})


def newTitlePlayList(user, title, song):
    playLists = PlaylistSong.objects.all()
    for playList in playLists:
        if (playList.user.email == user.email):
            for sg in playList.songs:
                if sg._id == song.id:
                    sg.title = title
        playList.save()

def newArtistPlayList(user, artist, song):
    playLists = PlaylistSong.objects.all()
    for playList in playLists:
        if (playList.user.email == user.email):
            for sg in playList.songs:
                if sg._id == song.id:
                    sg.artist = artist
        playList.save()


    
    