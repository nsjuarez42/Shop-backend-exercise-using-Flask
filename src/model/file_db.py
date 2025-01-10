from model.DB import DB
import os

import json

class file_db(DB):

    def get_column_names(self):
        return super().get_column_names()

    def select(self):
        print("Currently on {}".format(os.getcwd()))
        with open("./src/products.py","rb") as f:
            file = f.read().decode()
            file = file.replace("products = ","").replace(" ","")
            products = []
            for line in file.split("\r\n")[1:-1]:
                print(line[:-1])
                products.append(json.loads(line[:-1]))
            print(products)
        pass

    def insert(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass
