from abc import ABC, abstractmethod
from config import AppConfig
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from datetime import date

class DB(ABC):

    # @abstractmethod
    # def init(self, dbanme, dbconnstr):
    #     pass

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

Base = declarative_base()

class Policy(Base):
    __tablename__ = 'policy'

    # def __init__(self, id, resource_provider, policy_name, description, username, rego, UpdatedTime) -> None:
    #     id = Column(String, primary_key=True)
    #     resource_provider = Column(String)
    #     policy_name = Column(String)
    #     description = Column(Integer)
    #     username = Column(Integer)
    #     rego = Column(String)
    #     UpdatedTime = Column(Date)

    id = Column(String, primary_key=True)
    resource_provider = Column(String)
    policy_name = Column(String)
    description = Column(String)
    username = Column(String)
    rego = Column(String)
    UpdatedTime = Column(Date)

class PostgreSql(DB):

    DbName = 'azguardian'

    def __init__(self, appconfig: AppConfig) -> None:
        super().__init__()

        dbUri = f'postgresql://dbadmin:EasyToRemember1231@postgresql-azguardian-dev.postgres.database.azure.com:5432/{PostgreSql.DbName}'

        engine = create_engine(dbUri)

        if not database_exists(engine.url):
            create_database(engine.url)

        Base.metadata.create_all(engine)

        Session = sessionmaker(bind=engine)

        self.PostgreSession = Session()

#host=postgresql-azguardian-dev.postgres.database.azure.com port=5432 dbname={your_database} user=dbadmin password={your_password} sslmode=require
        self.appconfig = appconfig

        

    # def initDb(self, dbanme, dbconnstr):
    #     pass
    #     """Connect to the API for MongoDB, create DB and collection, perform CRUD operations"""
    #     mongoClient = pymongo.MongoClient(self.appconfig.dbConnstring)

    #     try:
    #         mongoClient.server_info() # validate connection string
    #     except pymongo.errors.ServerSelectionTimeoutError:
    #         raise TimeoutError("Invalid API for MongoDB connection string or timed out when attempting to connect")

    #     self.mongodb = self.mongoClient[Mongo.mongodbName]

    #     #check if azguardian database doesn't exist
    #     if Mongo.mongodbName not in mongoClient.list_database_names():
    #         # Database with 400 RU throughput that can be shared across the DB's collections
    #         self.mongodb.command({'customAction': "CreateDatabase", 'offerThroughput': 400})
    #         print("Created db {} with shared throughput". format(Mongo.MongoDbName))


    def create_policy(self, id, resourceProvider, name, desc, username):

        policy = Policy(id = 'da', resource_provider='dasa', policy_name='dasa', description='dasa', username='dasa', rego='dasa', UpdatedTime=date.today())
        self.PostgreSession.add(policy)
        self.PostgreSession.commit()
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