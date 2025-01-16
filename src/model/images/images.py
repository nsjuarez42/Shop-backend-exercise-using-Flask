from abc import ABC,abstractmethod

class images(ABC):

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