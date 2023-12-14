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

@songs_routes.route("/songs/searchTitle", methods=["GET"])
def searchTitle():
    email = request.args.get("user")
    return songs.searchTitle(email)

@songs_routes.route("/songs/play", methods=["GET"])
def play():
    email = request.args.get("user")
    return songs.play(email)

@songs_routes.route("/songs/addGenre", methods=["PATCH"])
def addGenre():
    email = request.args.get("user")
    return songs.addGenre(email)

@songs_routes.route("/songs/updateTitle", methods=["PATCH"])
def updateTitle():
    email = request.args.get("user")
    return songs.updateTitle(email)

@songs_routes.route("/songs/updateArtist", methods=["PATCH"])
def updateArtist():
    email = request.args.get("user")
    return songs.updateArtist(email)

@songs_routes.route("/songs/totalUserSongs", methods=["GET"])
def totalUserSongs():
    email = request.args.get("user")
    return songs.totalUserSongs(email)

@songs_routes.route("/songs/totalUserSongsRedis", methods=["GET"])
def totalUserSongsRedis():
    email = request.args.get("user")
    return songs.totalUserSongsRedis(email)

@songs_routes.route("/songs/totalSongs", methods=["GET"])
def totalSongs():
    return songs.totalSongs()

@songs_routes.route("/songs/totalSongsRedis", methods=["GET"])
def totalSongsRedis():
    return songs.totalSongsRedis()

@songs_routes.route("/songs/getUserGenres", methods=["GET"])
def getUserGenres():
    return songs.getUserGenres()

@songs_routes.route("/songs/getUserGenresRedis", methods=["GET"])
def getUserGenresRedis():
    return songs.getUserGenresRedis()

@songs_routes.route("/songs/getAllSongsRedis", methods=["GET"])
def getAllSongsRedis():
    email = request.args.get("user")
    return songs.getAllSongsRedis(email)

# ----------------
@songs_routes.route("/songs/listFavorite", methods=["GET"])
def listFavorite():
    email = request.args.get("user")
    return songs.listFavorites(email)

@songs_routes.route("/songs/favorite", methods=["PATCH"])
def favorite():
    email = request.args.get("user")
    return songs.favorite(email)





@songs_routes.route("/songs/updateGender", methods=["PATCH"])
def updateGender():
    email = request.args.get("user")
    return songs.updateGender(email)

@songs_routes.route("/songs/deleteSong", methods=["DELETE"])
def deleteSong():
    email = request.args.get("user")
    return songs.deleteSong(email)
