#from model.DB.sqlite_db import sqlite
#from model.DB.file_db import file_db
from model.DB.mysql import Mysql

class DB_factory():
    @staticmethod
    def create_db(t):
        #if t == "sqlite":
        #    return sqlite()
        #if t == "file":
        #    return file_db()
        if t == "mysql":
            return Mysql()
        


    