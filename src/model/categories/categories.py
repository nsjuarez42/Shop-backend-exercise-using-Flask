from abc import abstractmethod,ABC

class categories(ABC):

    @abstractmethod
    def __init__(self,conn,cursor):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def get_by_id(self,id):
        pass

    @abstractmethod 
    def get_column_names(self):
        pass