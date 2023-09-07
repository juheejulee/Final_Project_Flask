
from flask import Blueprint, jsonify, request
from models.user_model import User
from database.__init__ import database
import json
import controllers.user_controller as user_controller
from helpers.token_validation import validateToken

user = Blueprint("user", __name__)

@user.route("/v0/users/signup", methods=["POST"])
def create():

    data = json.loads(request.data)

    if 'email' not in data:
        return jsonify({'error': "Email is required!"}), 400
    if 'password' not in data:
        return jsonify({'error': "Password is required!"}), 400
    if 'name' not in data:
        return jsonify({'error': "Name is required!"}), 400

    createdUser = user_controller.CreateUser(data)

    if createdUser == "Duplicated User":
        return jsonify({'error': "Email Already Exists"}), 400

    if not createdUser.inserted_id:
        return jsonify({'error': "Something went wrong!"}), 400


    return jsonify({'id': str(createdUser.inserted_id)})


@user.route("/v0/users/login", methods=["POST"])
def login():
    data = json.loads(request.data)

    if 'email' not in data:
        return jsonify({'error': "Email is required!"}), 400
    if 'password' not in data:
        return jsonify({'error': "Password is required!"}), 400
    
    loginAttempt = user_controller.loginUser(data)

    if loginAttempt=="Invalid email":
        return jsonify({'error': "Invalid Email or Password"}), 400
    if loginAttempt=="Invalid Password":
        return jsonify({'error': "Invalid Email or Password"}), 400

    return jsonify({'token': loginAttempt.json['token'], 'expiration': loginAttempt.json['expiration'], 'loggedUser': loginAttempt.json['loggedUser']})



@user.route("/v0/users/all", methods=["GET"])
def fetch():

    token = validateToken()
    
    try:
        if token == 400:
            return jsonify({'error': "Token is missing"}), 400
        if token == 401:
            return jsonify({'error': "Invalid Auth"}), 400

        print("Before Fetch Users")

        return user_controller.fetchUsers()
    except:
        return jsonify({'error': "Error on fetching users"}), 400
