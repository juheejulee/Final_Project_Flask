
from pymongo import MongoClient
from .db import Database
import app_config as config

database = Database(connectionString=config.CONST_MONGO_URL, dataBaseName=config.CONST_DATABASE)
database.connect()

#database = MongoClient("mongodb+srv://renancavalcanti:acqHkikAXzcQCXuS@cluster0.0n2n4ys.mongodb.net/?retryWrites=true&w=majority")




