from model.DB import DB
import sqlite3
from products import products

DB_NAME = "products"


def product_to_json(product,columns):
    json = {}
    for i,c in enumerate(columns):
        json[c] = product[i]
    return json

class mysql_db(DB):

    def __new__(cls):
        if not hasattr(cls,'instance'):
            cls.instance = super(mysql_db,cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.conn = sqlite3.connect(DB_NAME,check_same_thread=False)
        self.cursor = self.conn.cursor()

    def has_data(self):
        tables = self.cursor.execute("SELECT name FROM sqlite_master WHERE TYPE='table'").fetchall()
        return len(tables) > 0
    
    def fill(self):
        products = "CREATE TABLE products(ID INTEGER AUTO_INCREMENT PRIMARY KEY,name VARCHAR(100) NOT NULL UNIQUE,price INTEGER UNSIGNED NOT NULL,quantity INTEGER UNSIGNED NOT NULL)"
        self.cursor.execute(products)
        for product in products:
            self.cursor.execute("INSERT INTO products VALUES(NULL,?,?,?)",(product["name"],product['price'],product['quantity']))
        self.conn.commit()
    
    def get_products(self):
        return [product_to_json(i,self.get_column_names()) for i in self.cursor.execute("SELECT * FROM products").fetchall()]
   
    def get_product_by_id(self,id):
        return self.cursor.execute("SELECT * FROM products WHERE ID=?",(id,)).fetchone()
  
    def get_product_by_name(self,name):
        return self.cursor.execute("SELECT * FROM products WHERE name=?",(name,)).fetchone()
    
    def add_product(self,product):
        self.cursor.execute("INSERT INTO products VALUES(NULL,?,?,?)",(product["name"],product["price"],product["quantity"]))
        self.conn.commit()
        return self.cursor.lastrowid
    
    def update_product_by_id(self,id,product):
        #put keys and dict in correct order
        print(product.keys())
        questions = []
        for i,k in enumerate(product.keys()):
            if i != len(product.keys())-1:
                questions.append(k+"=?,")
            else:
                questions.append(k+"=?")
        questions = " ".join(questions)
        
        self.cursor.execute("UPDATE products SET {} WHERE ID=?".format(questions),(*product.values(),id,))
        self.conn.commit()

    def delete_product_by_id(self,id):
        self.cursor.execute("DELETE FROM products WHERE ID=?",(id,))
        self.conn.commit()

    def get_column_names(self):
        return [c[1] for c in self.cursor.execute("PRAGMA table_info(products)").fetchall()]

