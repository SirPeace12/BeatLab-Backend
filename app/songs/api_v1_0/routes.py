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

@songs_routes.route("/songs/favorite", methods=["PATCH"])
def favorite():
    email = request.args.get("user")
    return songs.favorite(email)

@songs_routes.route("/songs/listFavorite", methods=["GET"])
def listFavorite():
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

@songs_routes.route("/songs/updateArtist", methods=["PATCH"])
def updateArtist():
    email = request.args.get("user")
    return songs.updateArtist(email)

@songs_routes.route("/songs/updateTitle", methods=["PATCH"])
def updateTitle():
    email = request.args.get("user")
    return songs.updateTitle(email)

@songs_routes.route("/songs/updateGender", methods=["PATCH"])
def updateGender():
    email = request.args.get("user")
    return songs.updateGender(email)

@songs_routes.route("/songs/deleteSong", methods=["DELETE"])
def deleteSong():
    email = request.args.get("user")
    return songs.deleteSong(email)
