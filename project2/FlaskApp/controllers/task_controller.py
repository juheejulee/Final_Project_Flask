from FlaskApp.database.__init__ import Database
from FlaskApp.models.task_model import Task
from FlaskApp import app_config as config
from . import user_controller


from datetime import datetime, timedelta
from flask import jsonify
from bson.objectid import ObjectId

from FlaskApp.database import database

def CreateTask(taskInformation, user):
    try:
        newTask = Task()
        newTask.description = taskInformation['description']
        newTask.done = taskInformation.get('done', False)  # default value is False if not provided
        newTask.assignedToUid = user['uid']
        newTask.createdByUid = user['uid']
        newTask.createdByName = user['name']
        newTask.assignedToName = user['name']

        print(newTask.__dict__)

        collection = database.dataBase[config.CONST_TASK_COLLECTION]

        createdTask = collection.insert_one(newTask.__dict__)

        return createdTask

    except Exception as err:
        raise ValueError("Error on creating Task!", err)

def fetchTasks(user):
    collection = database.dataBase[config.CONST_TASK_COLLECTION]
    tasks = []

    for item in collection.find({'assignedToUid': user['uid']}):
        currentTask = {}
        currentTask["taskUid"] = str(item["_id"])
        currentTask["description"] = item["description"]
        currentTask["done"] = item["done"]
        currentTask["createdByUid"] = item["createdByUid"]
        currentTask["assignedToUid"] = item["assignedToUid"]
        currentTask["createdByName"] = item["createdByName"]
        currentTask["assignedToName"] = item["assignedToName"]
        tasks.append(currentTask)

    return {"tasks": tasks}

def getTask(task_id):
    try:
        collection = database.dataBase[config.CONST_TASK_COLLECTION]
        task = collection.find_one({"_id": ObjectId(task_id)})
        if task:
            return task
        else:
            return "Task not found"
    except Exception as err:
        raise ValueError("Error on fetching task!", err)


def updateTask(task_id, task_info, user):
    collection = database.dataBase[config.CONST_TASK_COLLECTION]

    task = collection.find_one({"_id": ObjectId(task_id)})

    if task['assignedToUid'] != user['uid']:
        raise ValueError("Users can only change status when task is assigned to them.")

    update_result = collection.update_one(
        {"_id": ObjectId(task_id)},
        {"$set": task_info}
    )

    if update_result.modified_count == 0:
        return {"message": f"No tasks found with id {task_id}"}

    return {"message": f"Task with id {task_id} was updated."}


def deleteTask(task_id, user):
    collection = database.dataBase[config.CONST_TASK_COLLECTION]

    task = collection.find_one({"_id": ObjectId(task_id)})

    if task['createdByUid'] != user['uid']:
        raise ValueError("Users can only delete tasks they created.")

    delete_result = collection.delete_one({"_id": ObjectId(task_id)})

    if delete_result.deleted_count == 0:
        return {"message": f"No tasks found with id {task_id}"}

    return {"message": f"Task with id {task_id} was deleted."}
def getTasksAssignedToUser(token):
    # Decode the token
    user_id = user_controller.decode_auth_token(token)

    # If the token is invalid or expired
    if isinstance(user_id, str):
        return {"message": user_id}

    # Fetch tasks from the database assigned to the user
    collection = database.dataBase[config.CONST_TASK_COLLECTION]
    tasks = []

    for item in collection.find({"assignedTo": ObjectId(user_id)}):
        currentTask = {}
        currentTask["uid"] = str(item["_id"])
        currentTask["title"] = item["title"]
        currentTask["description"] = item["description"]
        tasks.append(currentTask)

    return {"tasks": tasks}
