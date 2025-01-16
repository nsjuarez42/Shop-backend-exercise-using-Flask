from abc import ABC,abstractmethod

class tags(ABC):

    @abstractmethod
    def __init__(self,conn,cursor):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def get_by_product(self):
        pass

