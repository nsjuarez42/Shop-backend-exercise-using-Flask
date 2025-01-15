from abc import ABC,abstractmethod

class DBABC(ABC):

    @property
    @abstractmethod
    def categories(self):
        pass

    @property
    @abstractmethod
    def images(self):
        pass

    @property
    @abstractmethod
    def tags(self):
        pass

    @property
    @abstractmethod
    def reviews(self):
        pass

    @property
    @abstractmethod
    def users(self):
        pass

    @property
    @abstractmethod
    def products(self):
        pass
 








