from abc import ABC,abstractmethod

class images(ABC):

    @abstractmethod
    def __init__(self,conn,cursor):
        pass

    @abstractmethod
    def get_by_product():
        pass

    @abstractmethod
    def add():
        pass

    @property
    @abstractmethod
    def columns():
        pass

    @abstractmethod
    def image_to_json():
        pass