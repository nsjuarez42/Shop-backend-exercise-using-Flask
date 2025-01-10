from model.mysql_db import mysql_db
from model.file_db import file_db


class DB_factory():
    @staticmethod
    def create_db(t):
        if t == "mysql":
            return mysql_db()
        elif t == "file":
            return file_db()
        


    