from flask import Blueprint, request
import authentication.api_v1_0.views  as auth

auth_routes = Blueprint("auth", __name__)

@auth_routes.route("/login", methods=["POST"])
def login():
    return auth.login()

@auth_routes.route("/register", methods=["POST"])
def register():
    return auth.register()

@auth_routes.route("/sendRecuperationEmail", methods=["POST"])
def sendRecuperationEmail():
    return auth.sendRecuperationEmail()

@auth_routes.route("/confirmToken", methods=["POST"])
def confirmToken():
    return auth.confirmToken()

@auth_routes.route("/resetPassword", methods=['POST'])
def resetPassword():
    token = request.args.get("token")
    return auth.resetPassword(token)

@auth_routes.route("/uploadPhoto", methods=['PUT'])
def uploadPhoto():
    email = request.args.get("user")
    return auth.uploadPhoto(email)

@auth_routes.route("/updateName", methods=['PUT'])
def updateName():
    email = request.args.get("user")
    return auth.updateName(email)

