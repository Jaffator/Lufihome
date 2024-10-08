from flask import Blueprint, render_template, jsonify, request
from modules import query, AlarmFunctions, GarageGate
from werkzeug.security import generate_password_hash, check_password_hash
from web import SocketIO_events
import time
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from flask_jwt_extended import set_access_cookies
from flask_jwt_extended import unset_jwt_cookies
from datetime import datetime
from datetime import timedelta
from datetime import timezone

auth = Blueprint('auth', __name__)


def authenticate(user, passw):
    result = bool
    userdata = query.get_User(user)
    if len(userdata) == 0:  # if is not in database, length of list is 0
        result = False
    else:  # user found in databe -> check the password
        hashpass = userdata[0]['Pass']
        result = check_password_hash(hashpass, passw)
    return result


@auth.route('/auth/login', methods=['GET', 'POST'])
def login():
    data = request.json
    password = data['password']
    username = data['username']
    auth_result = authenticate(username, password)
    if auth_result == False:
        response = jsonify({"msg": "login not successful"})
        return response, 401
    role = query.get_User(username)[0]['AccountType']
    response = jsonify({'username': username, 'role': role})
    access_token = create_access_token(identity=username)
    set_access_cookies(response, access_token)
    print('user logged in!')
    return response, 201


@auth.route("/auth/logout", methods=["POST"])
def logout():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response


@auth.route("/auth/checktoken", methods=["GET", "POST"])
@jwt_required()
def checktoken():
    response = jsonify({"msg": "jwt ok"})
    return response
