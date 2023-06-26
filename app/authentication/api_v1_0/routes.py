from flask import Blueprint
import authentication.api_v1_0.views  as auth

auth_routes = Blueprint("auth", __name__)
@auth_routes.route("/login", methods=["POST"])
def login():
    return auth.login()

@auth_routes.route("/register", methods=["POST"])
def register():
    return auth.register()

@auth_routes.route("/configuration", methods=["POST"])
def sendRecuperationEmail():
    return auth.sendRecuperationEmail()

@auth_routes.route('/resetPassword/<token>', methods=['GET', 'POST'])
def resetPassword(token):
    return auth.resetPassword(token)