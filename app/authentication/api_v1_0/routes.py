from flask import Blueprint, request
import authentication.api_v1_0.views  as auth

auth_routes = Blueprint("auth", __name__)



@auth_routes.after_request
def add_headers(response):
    response.headers['Content-Type'] = 'application/json'  # Configura el Content-Type como application/json
    return auth.add_cors_headers(response)

@auth_routes.route("/login", methods=["OPTIONS"])
def handle_options_request():
    return auth.handle_options_request()

@auth_routes.route("/login", methods=["POST"])
def login():
    return auth.login()

@auth_routes.route("/register", methods=["POST"])
def register():
    return auth.register()

@auth_routes.route("/logout", methods=["POST"])
def logout():
    return auth.logout()

@auth_routes.route("/sendRecuperationEmail", methods=["POST"])
def sendRecuperationEmail():
    return auth.sendRecuperationEmail()

@auth_routes.route("/resetPassword", methods=['POST'])
def resetPassword():
    token = request.args.get("token")
    return auth.resetPassword(token)

@auth_routes.route("/confirmToken", methods=["POST"])
def confirmToken():
    return auth.confirmToken()