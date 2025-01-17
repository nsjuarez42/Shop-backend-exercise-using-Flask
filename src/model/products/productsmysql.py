from model.products.products import products_ABC
from model.DB.mysqlconnection import Connection
from model.DB.mysqlhelpers import manage_connection,get_column_names,object_to_json

products_per_page = 21

class products(products_ABC):

   
    def __init__(self,db):
        print(type(db))
        print(db)
        self.__columns = get_column_names("products")
        self.__db = db

    @property
    def columns(self):
        return self.__columns
    
    @columns.setter
    def columns(self,c):
        self.__columns = c

    @manage_connection
    def get_all(self):
        self.__db.cursor.execute("SELECT * FROM products")
        products = self.__db.cursor.fetchall()
        return [object_to_json(p,self.columns) for p in products]
    
    @manage_connection
    def get_by_id(self,id):
        self.__db.cursor.execute("SELECT * FROM products WHERE ID=%s",(id,))
        product = self.__db.cursor.fetchone()
        return object_to_json(product,self.columns) if product else None
    
    @manage_connection
    def get_by_title(self,title):
        self.__db.cursor.execute("SELECT * FROM products WHERE title=%s",(title,))
        product = self.__db.cursor.fetchone()
        return object_to_json(product,self.columns) if product else None
    
    @manage_connection
    def add(self,product):
        self.__db.cursor.execute("INSERT INTO products VALUES(NULL,{})".format(",".join(["?" for i in product])),tuple(product.values()))
        self.__db.conn.commit()
        return self.__db.cursor.lastrowid
    
    @manage_connection
    def delete_by_id(self,id):
        self.__db.cursor.execute("DELETE FROM products WHERE id=?",(id,))
        self.__db.conn.commit()

    @manage_connection
    def update_by_id(self,product):
        questions = []
        for i,k in enumerate(product.keys()):
            if i != len(product)-1:
                questions.append(k+"=?,")
            else:
                questions.append(k+"=?")
        questions = " ".join(questions)

        self.__db.cursor.execute("UPDATE products SET {} WHERE ID=?".format(questions),(*product.values(),id))
        self.__db.conn.commit()

    @manage_connection
    def get_page(self,page):
        self.__db.cursor.execute("SELECT * FROM products ORDER BY ID LIMIT {} OFFSET {}".format(products_per_page,(page-1)*products_per_page))
        products = self.__db.cursor.fetchall()
        return [object_to_json(p,self.columns) for p in products]
    
    @manage_connection
    def get_pages(self):
        self.__db.cursor.execute("SELECT COUNT(*) / {} FROM products".format(products_per_page))
        columns = self.__db.cursor.fetchone()[0]
        return int(columns) +1 if int(columns) < columns else int(columns)
    
    @manage_connection
    def filter_products(self, filters):
        self.__db.cursor.execute("""SELECT p.*,t.name FROM products as p
        INNER JOIN categories as c ON c.ID = p.idcategory
        INNER JOIN tagproduct as tp ON tp.idproduct = p.ID
        INNER JOIN tags as t ON tp.idtag = t.ID
        WHERE c.name=%s;""",(filters['category'],))
        filtered_by_category = self.__db.cursor.fetchall()
        products = [object_to_json(p,self.columns+['tag']) for p in filtered_by_category]
        #each product should have tags key which contains all tags from that same product
        unique_products = []
        for product in products:
            if product["ID"] not in [p["ID"] for p in unique_products if p["ID"] == product["ID"]]:
                print("{} not in unique products".format(product["ID"]))
                unique_products.append(product)
            else:
                print("{} is in unique products".format(product["ID"]))
                print(unique_products)
                p_i= [i for i,x in enumerate(unique_products) if x["ID"] == product["ID"]][0]
                
                if "tags" not in unique_products[p_i].keys():
                    unique_products[p_i]['tags'] = [unique_products[p_i]['tag'],product['tag']]
                    del unique_products[p_i]['tag']
                else:
                    unique_products[p_i]['tags'].append(product['tag'])
        #if tags sent are in tags of object
        data = []
        for p in unique_products:
            for tag in filters['tags']:
                if tag not in p['tags']:
                    break
            else:
                data.append(p)
  
        return data