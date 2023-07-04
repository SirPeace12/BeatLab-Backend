from flask import Blueprint

import songs.api_v1_0.views  as songs

songs_routes = Blueprint("songs", __name__)

# @songs_routes.route("/songs", methods=["POST"])
# def showAll():
#     return songs.showAll()

@songs_routes.route("/songs/play", methods=["GET"])
def play():
    return songs.play()

@songs_routes.route("/songs/upload", methods=["GET"])
def upload():
    return songs.upload()