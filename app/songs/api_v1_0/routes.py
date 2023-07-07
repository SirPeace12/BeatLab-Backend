from flask import Blueprint, request

import songs.api_v1_0.views  as songs

songs_routes = Blueprint("songs", __name__)

@songs_routes.route("/songs", methods=["GET"])
def showAll():
    email = request.args.get("user")
    return songs.getAllSongs(email)

@songs_routes.route("/songs/upload", methods=["POST"])
def upload():
    email = request.args.get("user")
    return songs.upload(email)

@songs_routes.route("/songs/favorite", methods=["POST"])
def favorite():
    email = request.args.get("user")
    return songs.favorite(email)

@songs_routes.route("/songs/listfavorite", methods=["GET"])
def listfavorite():
    email = request.args.get("user")
    return songs.listFavorites(email)

@songs_routes.route("/songs/searchGender", methods=["GET"])
def searchGender():
    email = request.args.get("user")
    return songs.searchGender(email)

@songs_routes.route("/songs/searchTitle", methods=["GET"])
def searchTitle():
    email = request.args.get("user")
    return songs.searchTitle(email)

@songs_routes.route("/songs/play", methods=["GET"])
def play():
    email = request.args.get("user")
    return songs.play(email)

