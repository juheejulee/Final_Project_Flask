from pymongo import MongoClient


class Database():
    def __init__(self, dataBaseName=None, connectionString=None):
        if ((dataBaseName == None) or (connectionString == None)):
            raise Exception("Mongo DB requires database name and string connection!")

        self.__dataBaseName = dataBaseName
        self.__connectionString = connectionString
        self.__dbConnection = None
        self.__dataBase = None

    @property
    def dataBase(self):
        return self.__dataBase

    def connect(self):
        try:
            self.__dbConnection = MongoClient(self.__connectionString)
            dbName = str(self.__dataBaseName)
            self.__dataBase = self.__dbConnection[dbName]
        except Exception as err:
            print("Mongo connection error", err)

database = Database('Group3', 'mongodb+srv://dimitryaujour:dimitry777@cluster0.0sanbxa.mongodb.net/?retryWrites=true&w=majority')
database.connect()


def create_document(self, collection_name, data):
    collection = self.dataBase[collection_name]
    document = collection.insert_one(data)
    return document.inserted_id

def insert_test_document():
    document = {"name": "Test User", "email": "testuser@example.com"}
    collection = database.dataBase['test']  # replace 'users' with your collection name
    insert_result = collection.insert_one(document)
    print(f'Inserted document with id {insert_result.inserted_id}')


insert_test_document()
