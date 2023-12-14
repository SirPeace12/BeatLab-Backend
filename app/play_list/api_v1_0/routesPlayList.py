from flask import Blueprint, request

import play_list.api_v1_0.viewsPlayList  as playList

playList_routes = Blueprint("playList", __name__)

@playList_routes.route("/songs/playlist", methods=["POST"])
def createPlayList():
    email = request.args.get("user")
    return playList.createPlayList(email)

@playList_routes.route("/songs/addSong", methods=["POST"])
def addSong():
    email = request.args.get("user")
    return playList.addSong(email)

@playList_routes.route("/songs/updateDescription", methods=["PATCH"])
def updateDescription():
    email = request.args.get("user")
    return playList.updateDescription(email)

@playList_routes.route("/songs/updateName", methods=["PATCH"])
def updateName():
    email = request.args.get("user")
    return playList.updateName(email)