from flask import Blueprint

import songs.api_v1_0.views  as songs

songs_routes = Blueprint("songs", __name__)

@songs_routes.route("/songs/<string:email>", methods=["GET"])
def showAll(email):
    return songs.getAllSongs(email)

@songs_routes.route("/songs/upload", methods=["POST"])
def upload():
    return songs.upload()

@songs_routes.route("/songs/favorite", methods=["POST"])
def favorite():
    return songs.favorite()

@songs_routes.route("/songs/listfavorite", methods=["GET"])
def listfavorite():
    return songs.listFavorites()

@songs_routes.route("/songs/searchGender", methods=["POST"])
def searchGender():
    return songs.searchGender()

@songs_routes.route("/songs/searchTitle", methods=["POST"])
def searchTitle():
    return songs.searchTitle()

@songs_routes.route("/songs/play", methods=["GET"])
def play():
    return songs.play()

