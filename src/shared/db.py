from abc import ABC, abstractmethod
from config import AppConfig
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from datetime import date
from typing import List
import uuid

class DB(ABC):

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

        dbUri = f'postgresql://{appconfig.dbUserName}:{appconfig.dbUserPass}@{appconfig.dbHost}:5432/{PostgreSql.DbName}'

        engine = create_engine(dbUri)

        if not database_exists(engine.url):
            create_database(engine.url)

        Base.metadata.create_all(engine)

        Session = sessionmaker(bind=engine)

        self.PostgreSession: Session
        self.PostgreSession = Session()

        self.appconfig = appconfig

    def create_policy(self, resourceProvider, name, desc, username, rego):

        policy = Policy(id = self.uid(), resource_provider= resourceProvider, policy_name= name, description= desc, username= username, rego= rego, UpdatedTime=date.today())
        self.PostgreSession.add(policy)
        self.PostgreSession.commit()

    def update_policy(self, id, resourceProvider = '', name= '', desc= '', username= '', rego= ''):

        policy = self.PostgreSession.query(Policy).filter(Policy.id == id).first()
        policy.resource_provider = resourceProvider
        policy.name = name
        policy.desc = desc
        policy.rego = rego
        policy.username = username

        self.PostgreSession.commit()

    def delete_policy(self, id):
        policy = self.PostgreSession.query(Policy).filter(Policy.id == id).first()
        self.PostgreSession.delete(policy)
        self.PostgreSession.commit()

    def list_all_policies(self) -> List[Policy]:
        policies = self.PostgreSession.query(Policy).all()
        return policies

    def uid(self):
        return str(uuid.uuid4())[:8]