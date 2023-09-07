from flask import request
import jwt
from FlaskApp import app_config as config


def validateToken():
    token = None
    userInformation = None

    try:
        auth_header = request.headers.get('Authorization')
        if auth_header:
            token = auth_header.split(" ")[1]

        if not token:
            return 400

        try:
            userInformation = jwt.decode(token, key=config.TOKEN_SECRET, algorithms=["HS256"])
            print(userInformation)
        except Exception:
            return 401

        return userInformation
    except:
        return 400
