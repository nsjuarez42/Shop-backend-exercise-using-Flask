from model.DB import DB
import sqlite3
#from sample_data import products,users

DB_NAME = "products"

def product_to_json(product,columns):
    print(product)
    json = {}
    for i,c in enumerate(columns):
        json[c] = product[i]
    return json

class sqlite(DB):

    def __new__(cls):
        if not hasattr(cls,'instance'):
            cls.instance = super(sqlite,cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.conn = sqlite3.connect(DB_NAME,check_same_thread=False)
        self.cursor = self.conn.cursor()

    def has_data(self):
        tables = self.cursor.execute("SELECT name FROM sqlite_master WHERE TYPE='table'").fetchall()
        return len(tables) > 0
    
   # def fill(self):
   #     create_products = "CREATE TABLE products(ID INTEGER PRIMARY KEY,name VARCHAR(100) NOT NULL UNIQUE,price INTEGER UNSIGNED NOT NULL,quantity INTEGER UNSIGNED NOT NULL)"
   #     create_users = "CREATE TABLE users(ID INTEGER PRIMARY KEY,name VARCHAR(120) NOT NULL,password varchar(40) NOT NULL,username VARCHAR(80) NOT NULL UNIQUE,mail VARCHAR (100) NOT NULL UNIQUE)"
   #     self.cursor.execute(create_products)
   #     self.cursor.execute(create_users)
   #     for product in products:
   #         self.cursor.execute("INSERT INTO products(name,price,quantity) VALUES(?,?,?)",(product["name"],product['price'],product['quantity']))
   #     for user in users:
   #         self.cursor.execute("INSERT INTO users(name,password,username,mail) VALUES(?,?,?,?)",(user['name'],user['password'],user['username'],user['mail']))
   #     self.conn.commit()
    
    def get_products(self):
        return [product_to_json(i,self.get_product_column_names()) for i in self.cursor.execute("SELECT * FROM products").fetchall()]
   
    def get_product_by_id(self,id):
        product = self.cursor.execute("SELECT * FROM products WHERE ID=?",(id,)).fetchone()
        return product_to_json(product,self.get_product_column_names()) if product else None
  
    def get_product_by_name(self,name):
        product =self.cursor.execute("SELECT * FROM products WHERE name=?",(name,)).fetchone()
        return product_to_json(product,self.get_product_column_names()) if product else None
    
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

    def get_product_column_names(self):
        return [c[1] for c in self.cursor.execute("PRAGMA table_info(products)").fetchall()]
    
    def get_users_column_names(self):
        return [c[1] for c in self.cursor.execute("PRAGMA table_info(users)").fetchall()]
    
    def add_user(self, user):
        self.cursor.execute("INSERT INTO users VALUES (NULL,?,?,?,?)",(user["name"],user["password"],user["username"],user['mail']))
        self.conn.commit()
        return self.cursor.lastrowid
    
    def get_user_by_username(self, username):
        user = self.cursor.execute("SELECT * FROM users WHERE username=?",(username,)).fetchone()
        return product_to_json(user,self.get_users_column_names()) if user else None 
    
    def get_user_by_mail(self, mail):
        user = self.cursor.execute("SELECT * FROM users WHERE mail=?",(mail,)).fetchone()
        return product_to_json(user,self.get_users_column_names()) if user else None

    def get_user_by_id(self, id):
        user =self.cursor.execute("SELECT * FROM users WHERE id=?",(id,)).fetchone()
        return product_to_json(user,self.get_users_column_names()) if user else None
    
    def get_users(self):
        return [product_to_json(u,self.get_users_column_names()) for u in self.cursor.execute("SELECT * FROM users").fetchall()]
    
