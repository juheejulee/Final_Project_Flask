import jwt
from flask import Blueprint, request, jsonify
from FlaskApp.controllers import task_controller, user_controller
from FlaskApp import app_config as config
from FlaskApp.helpers.token_validation import validateToken

routes = Blueprint('routes', __name__)

# User Routes
@routes.route('/users', methods=['POST'])
def create_user():
    return user_controller.CreateUser(request.json)

@routes.route('/users', methods=['GET'])
def fetch_users():
    return user_controller.fetchUsers()

@routes.route('/login', methods=['POST'])
def login_user():
    return user_controller.loginUser(request.json)

# Task Routes
@routes.route('/tasks', methods=['POST'])
def create_task():
    user_info = validateToken()

    if type(user_info) is int:
        return jsonify({'message': 'Token is missing!'}), 401 if user_info == 401 else 400

    print(user_info)  # To check what data you are getting.

    # Check if 'name' and 'id' keys exist in the user_info
    if 'name' not in user_info or 'id' not in user_info:
        return jsonify({'message': 'Required user information is missing in the token!'}), 400

    user = {
        'uid': user_info['id'],
        'name': user_info['name']
    }

    # Call the CreateTask function with the request's JSON data and the authenticated user
    task_controller.CreateTask(request.get_json(), user)
    return jsonify({"message": "Task created successfully"}), 201


@routes.route('/tasks', methods=['GET'])
def fetch_tasks():
    return task_controller.fetchTasks()

@routes.route('/tasks/<taskUid>', methods=['PATCH'])
def update_task(taskUid):
    return task_controller.updateTask(taskUid, request.json)

@routes.route('/tasks/<taskUid>', methods=['DELETE'])
def delete_task(taskUid):
    return task_controller.deleteTask(taskUid)

@routes.route('/user/tasks', methods=['GET'])
def get_user_tasks():
    token = request.headers.get('Authorization')
    tasks = task_controller.fetchUserTasks(token)
    return jsonify(tasks)
