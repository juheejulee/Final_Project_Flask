
from FlaskApp.database import Database, database


class Task:
    def __init__(self, createdByUid=None, createdByName=None, assignedToUid=None, assignedToName=None, description=None, done=False):
        self.createdByUid = createdByUid
        self.createdByName = createdByName
        self.assignedToUid = assignedToUid
        self.assignedToName = assignedToName
        self.description = description
        self.done = done

    def insert(self):
        return database.db.tasks.insert_one(self.__dict__)

