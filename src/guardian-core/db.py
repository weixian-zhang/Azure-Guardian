from abc import ABC, abstractmethod
from config import AppConfig
import pymongo

class DB(ABC):

    @abstractmethod
    def init(self, dbanme, dbconnstr):
        pass

    # @abstractmethod
    # def save_subscription(self, id, name):
    #     pass

    # @abstractmethod
    # def get_subscriptions(self):
    #     pass

    @abstractmethod
    def create_policy(self, resourceProvider, name, desc, username):
        # + id, time
        pass

    @abstractmethod
    def update_policy(self, id):
        # + id, time
        pass

    @abstractmethod
    def delete_policy(self, id):
        # + id, time
        pass

    @abstractmethod
    def delete_policy(self, *id):
        # + id, time
        pass

    @abstractmethod
    def list_all_policies(self):
        # + id, time
        pass


class Mongo(DB):

    MongoDbName = 'azguardian'
    Policy_Collection_Name = 'policy'

    def __init__(self, appconfig: AppConfig) -> None:
        super().__init__()

        self.appconfig = appconfig

        self.init()

        

    def initDb(self, dbanme, dbconnstr):

        """Connect to the API for MongoDB, create DB and collection, perform CRUD operations"""
        mongoClient = pymongo.MongoClient(self.appconfig.dbConnstring)

        try:
            mongoClient.server_info() # validate connection string
        except pymongo.errors.ServerSelectionTimeoutError:
            raise TimeoutError("Invalid API for MongoDB connection string or timed out when attempting to connect")

        self.mongodb = self.mongoClient[Mongo.mongodbName]

        #check if azguardian database doesn't exist
        if Mongo.mongodbName not in mongoClient.list_database_names():
            # Database with 400 RU throughput that can be shared across the DB's collections
            self.mongodb.command({'customAction': "CreateDatabase", 'offerThroughput': 400})
            print("Created db {} with shared throughput". format(Mongo.MongoDbName))


    def create_policy(self, resourceProvider, name, desc, username):
        # + id, time
        pass

    def update_policy(self, id):
        # + id, time
        pass

    def delete_policy(self, id):
        # + id, time
        pass

    def delete_policy(self, *id):
        # + id, time
        pass

    def list_all_policies(self):
        # + id, time
        pass