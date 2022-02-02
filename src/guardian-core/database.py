from abc import ABC, abstractmethod


class DB(ABC):

    @abstractmethod
    def init(self):
        pass

    @abstractmethod
    def save_subscription(self, id,name):
        pass

    @abstractmethod
    def get_subscriptions(self):
        pass


# class Mongo(DB):

