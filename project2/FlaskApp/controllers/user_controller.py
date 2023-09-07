from FlaskApp.database.__init__ import Database
from FlaskApp.models import user_model
import bcrypt
from FlaskApp import app_config as config
from flask import jsonify

from datetime import datetime, timedelta
import jwt
from flask import jsonify
from bson.objectid import ObjectId
from flask import current_app as app
from FlaskApp.database import database
from FlaskApp.models.user_model import User


def generateHashPassword(password):
    salt = bcrypt.gensalt()
    hashPassword = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashPassword


def CreateUser(userInformation):
    try:
        newUser = User()
        newUser.name = userInformation['name'].lower()
        newUser.email = userInformation['email'].lower()
        newUser.password = generateHashPassword(userInformation['password'])

        print(newUser.__dict__)

        collection = database.dataBase[config.CONST_USER_COLLECTION]

        if collection.find_one({'email': newUser.email}):
            return {"message": "Duplicated User"}

        collection.insert_one(newUser.__dict__)

        return {"message": "User created successfully"}

    except Exception as err:
        return {"message": "Error on creating User!", "error": str(err)}


def loginUser(userInformation):
    email = userInformation['email'].lower()
    password = userInformation['password'].encode("utf-8")

    collection = database.dataBase[config.CONST_USER_COLLECTION]

    currentUser = collection.find_one({'email': email})

    if not currentUser:
        return {"message": "Invalid Email"}

    if not bcrypt.checkpw(password, currentUser["password"]):
        return {"message": "Invalid Password"}

    loggedUser = {}
    loggedUser['uid'] = str(currentUser['_id'])
    loggedUser['email'] = currentUser['email']
    loggedUser['name'] = currentUser['name']

    expiration = datetime.utcnow() + timedelta(seconds=config.JWT_EXPIRATION)

    jwtData = {
        'email': currentUser['email'],
        'id': str(currentUser['_id']),
        'name': currentUser['name'],
        'exp': expiration
    }

    jwtToReturn = jwt.encode(payload=jwtData, key=config.TOKEN_SECRET)

    return {'token': jwtToReturn, 'expiration': config.JWT_EXPIRATION, 'loggedUser': loggedUser}


def fetchUsers():
    collection = database.dataBase[config.CONST_USER_COLLECTION]
    users = []

    for item in collection.find():
        currentUser = {}
        currentUser["uid"] = str(item["_id"])
        currentUser["email"] = item["email"]
        currentUser["name"] = item["name"]
        users.append(currentUser)

    return {"users": users}
def getUser(user_id):
    try:
        collection = database.dataBase[config.CONST_USER_COLLECTION]
        user = collection.find_one({"_id": ObjectId(user_id)})
        if user:
            return user
        else:
            return "User not found"
    except Exception as err:
        raise ValueError("Error on fetching user!", err)


def updateUser(user_id, user_info):
    collection = database.dataBase[config.CONST_USER_COLLECTION]

    update_result = collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": user_info}
    )

    if update_result.modified_count == 0:
        return {"message": f"No users found with id {user_id}"}

    return {"message": f"User with id {user_id} was updated."}


def deleteUser(user_id):
    collection = database.dataBase[config.CONST_USER_COLLECTION]

    delete_result = collection.delete_one({"_id": ObjectId(user_id)})

    if delete_result.deleted_count == 0:
        return {"message": f"No users found with id {user_id}"}

    return {"message": f"User with id {user_id} was deleted."}

def decode_auth_token(auth_token):
    try:
        payload = jwt.decode(auth_token, config.TOKEN_SECRET)
        return payload['id']
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'