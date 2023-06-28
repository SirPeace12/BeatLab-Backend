from flask import Blueprint
import authentication.api_v1_0.views  as auth



auth_routes = Blueprint("auth", __name__)

@auth_routes.after_request
def add_headers(response):
    response.headers['Content-Type'] = 'application/json'  # Configura el Content-Type como application/json
    return response

@auth_routes.route("/login", methods=["POST"])
def login():
    return auth.login()

@auth_routes.route("/register", methods=["POST"])
def register():
    return auth.register()


