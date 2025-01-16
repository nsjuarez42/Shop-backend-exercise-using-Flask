from abc import ABC,abstractmethod


class users_ABC(ABC):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def add(self,user):
        pass

    @abstractmethod
    def get_by_username(self,username):
        pass

    @abstractmethod
    def get_by_mail(self,mail):
        pass

    @abstractmethod
    def get_by_id(self,id):
        pass