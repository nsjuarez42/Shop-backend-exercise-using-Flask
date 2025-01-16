from model.DB.DB import DBABC
from model.users.usersmysql import users
from model.products.productsmysql import products
from model.reviews.reviewsmysql import reviews_mysql
from model.categories.categories_mysql import categories_mysql
from model.tags.tagsmysql import tags_mysql
from model.images.images_mysql import images_mysql
from model.DB.mysqlconnection import Connection


class mysql(DBABC):

    def __init__(self):
        db = Connection()
    
        self.__products = products(db)
        self.__users = users(db)
        self.__reviews = reviews_mysql(db)
        self.__categories = categories_mysql(db)
        self.__tags = tags_mysql(db)
        self.__images = images_mysql(db)

    @property
    def cursor(self):
        return self.__cursor
    
    @cursor.setter
    def cursor(self,new):
        self.__cursor = new

    @property
    def conn(self):
        return self.__conn
    
    @conn.setter
    def conn(self,c):
        self.__conn = c

    @property
    def products(self):
        return self.__products
    
    @property
    def users(self):
        return self.__users
    
    @property 
    def images(self):
        return self.__images
    
    @property
    def categories(self):
        return self.__categories
    
    @property
    def tags(self):
        return self.__tags
    
    @property
    def reviews(self):
        return self.__reviews
    
    





    

