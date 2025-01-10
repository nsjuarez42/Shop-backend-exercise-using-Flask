from abc import ABC,abstractmethod

class DB(ABC):
    @abstractmethod
    def has_data(self):
        pass

    @abstractmethod
    def fill(self):
        pass

    @abstractmethod
    def get_products(self):
        pass

    @abstractmethod
    def get_product_by_id(self):
        pass

    @abstractmethod
    def get_product_by_name(self):
        pass
        
    @abstractmethod
    def add_product(self):
        pass
    
    @abstractmethod
    def update_product_by_id(self):
        pass

    @abstractmethod
    def delete_product_by_id(self):
        pass

    @abstractmethod
    def get_column_names(self):
        pass



