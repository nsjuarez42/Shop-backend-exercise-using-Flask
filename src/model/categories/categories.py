from abc import abstractmethod,ABC

class categories(ABC):

    @property
    @abstractmethod
    def columns(self):
        pass

    @columns.setter
    @abstractmethod
    def columns(self,c):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def get_by_id(self,id):
        pass