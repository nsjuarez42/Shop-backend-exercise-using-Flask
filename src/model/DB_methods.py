from model.mysql_db import mysql_db
from model.file_db import file_db
#put all methods here deal with different types inside
#Fill db
#
class DB_methods():

    def __init__(self,db):
        self.db = db
        print(type(db) == mysql_db)

    def get_product_by_id(self,id):
        if type(self.db) == mysql_db:
            pass
        elif type(self.db) == file_db:
            pass

    def get_products(self):
        if type(self.db) == mysql_db:
            return self.db.select(["ID","name","quantity","price"],"products",many=True)
        elif type(self.db) == file_db:
            return self.db.select()
            pass

