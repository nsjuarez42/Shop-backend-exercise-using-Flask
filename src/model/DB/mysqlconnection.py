import mysql.connector

class Connection():
    def __new__(cls):
        if not hasattr(cls,"instance"):
            cls.instance = super(Connection,cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.__conn = mysql.connector.connect(user="root",database="products",password="root",host="127.0.0.1")
        self.__cursor = self.__conn.cursor()

    @property
    def cursor(self):
        return self.__cursor

    @cursor.setter
    def cursor(self,c):
        self.__cursor = c

    @property
    def conn(self):
        return self.__conn
