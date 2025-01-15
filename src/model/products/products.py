from abc import ABC,abstractmethod

class products_ABC(ABC):

    @abstractmethod
    def __init__(self,conn,cursor):
        pass

    @abstractmethod
    def filter_products(self,filters):
        pass


    @abstractmethod
    def get_pages(self):
        pass

    @abstractmethod
    def get_page(self,page):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def get_by_id(self):
        pass

    @abstractmethod
    def get_by_title(self):
        pass

    @abstractmethod   
    def add(self):
        pass

    @abstractmethod
    def update_by_id(self):
        pass

    @abstractmethod
    def delete_by_id(self):
        pass

    @abstractmethod
    def get_column_names(self):
        pass