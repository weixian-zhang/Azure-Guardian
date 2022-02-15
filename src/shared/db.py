from abc import ABC, abstractmethod
from config import AppConfig
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from datetime import date
from typing import List
import log
import uuid

class DB(ABC):

    @abstractmethod
    def create_or_update_policy(self, resourceProvider, packageName, desc, username):
        # + id, time
        pass

    # @abstractmethod
    # def update_policy(self, id):
    #     # + id, time
    #     pass

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
    package_name = Column(String)
    rego = Column(String)
    description = Column(String)
    username = Column(String)
    UpdatedTime = Column(Date)

class PostgreSql(DB):

    DbName = 'azguardian'

    def __init__(self, appconfig: AppConfig) -> None:
        super().__init__()

<<<<<<< HEAD
        dbUri = f'postgresql://-:-@postgresql-azguardian-dev.postgres.database.azure.com:5432/{PostgreSql.DbName}'
=======
        dbUri = f'postgresql://{appconfig.dbUserName}:{appconfig.dbUserPass}@{appconfig.dbHost}:5432/{PostgreSql.DbName}'
>>>>>>> f3947200f26258bfa605beac1af2cc713f0699cb

        engine = create_engine(dbUri)

        if not database_exists(engine.url):
            create_database(engine.url)

        Base.metadata.create_all(engine)

        Session = sessionmaker(bind=engine)

        self.PostgreSession: Session
        self.PostgreSession = Session()

        self.appconfig = appconfig

    def create_or_update_policy(self, resourceProvider, packageName, desc, username, rego):

        exist, policy = self.is_policy_exists(packageName)
        if exist:
            ok = self.update_policy(resourceProvider=resourceProvider, packageName=packageName, \
                rego=rego,desc=desc,username=username)
            return ok
        
        policy = Policy(id = self.uid(), resource_provider= resourceProvider, package_name= packageName, \
            description= desc, username= username, rego= rego, UpdatedTime=date.today())

        self.PostgreSession.add(policy)
        self.PostgreSession.commit()

        return True

    def is_policy_exists(self, packageName):
        policy = self.PostgreSession.query(Policy).filter(Policy.package_name == packageName).first()
        if policy != None:
            return True, policy
        return False, None

    #packageName is unique
    def update_policy(self, resourceProvider = '', packageName= '', desc= '', username= '', rego= ''):

        try:

            policy = self.PostgreSession.query(Policy).filter(Policy.package_name == packageName).first()
            policy.resource_provider = resourceProvider
            policy.packageName = packageName
            policy.desc = desc
            policy.rego = rego
            policy.username = username

            self.PostgreSession.commit()

            return True
        except (Exception) as e:
            log.error(e)
            return False


    def delete_policy(self, id):
        policy = self.PostgreSession.query(Policy).filter(Policy.id == id).first()
        self.PostgreSession.delete(policy)
        self.PostgreSession.commit()

    def list_all_policies(self) -> List[Policy]:
        policies = self.PostgreSession.query(Policy).all()
        return policies

    def uid(self):
        return str(uuid.uuid4())[:8]
