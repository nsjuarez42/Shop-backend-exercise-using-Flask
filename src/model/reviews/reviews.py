from abc import ABC,abstractmethod

class reviews_ABC(ABC):

    @abstractmethod
    def __init__(self,conn,cursor):
        pass

    @abstractmethod
    def get_column_names(self):
        pass

    @abstractmethod
    def get_by_product(self,id):
        pass

    @abstractmethod
    def get_by_user(self,id):
        pass

    @abstractmethod
    def add(self,review):
        pass