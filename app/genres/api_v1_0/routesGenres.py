from flask import Blueprint, request

import genres.api_v1_0.viewsGenres  as genres

genres_routes = Blueprint("genres", __name__)

@genres_routes.route("/songs/genre", methods=["POST"])
def createGenre():
    return genres.createGenre()

@genres_routes.route("/songs/searchGenres", methods=["GET"])
def searchGenres():
    email = request.args.get("user")
    return genres.searchGenres(email)

@genres_routes.route("/songs/searchGenresRedis", methods=["GET"])
def searchGenresRedis():
    return genres.searchGenresRedis()

@genres_routes.route("/songs/allGenres", methods=["GET"])
def allGenres():
    return genres.allGenres()

@genres_routes.route("/songs/allGenresRedis", methods=["GET"])
def allGenresRedis():
    return genres.allGenresRedis()

@genres_routes.route("/songs/getGenreSongs", methods=["GET"])
def getGenreSongs():
    return genres.getGenreSongs()

@genres_routes.route("/songs/getGenreSongsRedis", methods=["GET"])
def getGenreSongsRedis():
    return genres.getGenreSongsRedis()

@genres_routes.route("/songs/totalSongPerGenre", methods=["GET"])
def totalSongPerGenre():
    return genres.totalSongPerGenre()

@genres_routes.route("/songs/totalSongPerGenreRedis", methods=["GET"])
def totalSongPerGenreRedis():
    return genres.totalSongPerGenreRedis()