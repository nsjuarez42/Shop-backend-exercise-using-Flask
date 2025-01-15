from model.DB.DB import DBABC
from model.users.usersmysql import users
from model.products.productsmysql import products
from model.reviews.reviewsmysql import reviews_mysql
from model.categories.categories_mysql import categories_mysql

import mysql.connector

class Mysql(DBABC):

    def __new__(cls):
        if not hasattr(cls,"instance"):
            cls.instance = super(Mysql,cls).__new__(cls)
        return cls.instance

    def __init__(self):
        conn = mysql.connector.connect(user="root",database="products",password="root",host="127.0.0.1")
        cursor = conn.cursor()
      
        self.__products = products(conn,cursor)
        self.__users = users(conn,cursor)
        self.__reviews = reviews_mysql(conn,cursor)
        self.__categories = categories_mysql(conn,cursor)

    @property
    def products(self):
        return self.__products
    
    @property
    def users(self):
        return self.__users
    
    @property 
    def images(self):
        return None
    
    @property
    def categories(self):
        return self.__categories
    
    @property
    def tags(self):
        return None
    
    @property
    def reviews(self):
        return self.__reviews
    
    





    

