from model.products.products import products_ABC


def product_to_json(product,columns):
    json = {}
    print(product)
    for i,c in enumerate(columns):
        json[c] = product[i]
    return json

class products(products_ABC):

    def __init__(self,conn,cursor):
        self.conn = conn
        self.cursor = cursor

    def get_all(self):
        self.cursor.execute("SELECT * FROM products")
        products = self.cursor.fetchall()
        return [product_to_json(p,self.get_column_names()) for p in products]
    
    def get_by_id(self,id):
        self.cursor.execute("SELECT * FROM products WHERE ID=%s",(id,))
        product = self.cursor.fetchone()
        return product_to_json(product,self.get_column_names())
    
    def get_by_title(self,title):
        self.cursor.execute("SELECT * FROM products WHERE title=%s",(title,))
        product = self.cursor.fetchone()
        return product_to_json(product,self.get_column_names()) if product else None
    
    def add(self,product):
        self.cursor.execute("INSERT INTO products VALUES(NULL,{})".format(",".join(["?" for i in product])),tuple(product.values()))
        self.conn.commit()
        return self.cursor.lastrowid
    
    def delete_by_id(self,id):
        self.cursor.execute("DELETE FROM products WHERE id=?",(id,))
        self.conn.commit()
    
    def update_by_id(self,product):
        questions = []
        for i,k in enumerate(product.keys()):
            if i != len(product)-1:
                questions.append(k+"=?,")
            else:
                questions.append(k+"=?")
        questions = " ".join(questions)

        self.cursor.execute("UPDATE products SET {} WHERE ID=?".format(questions),(*product.values(),id))
        self.conn.commit()
    
    def get_column_names(self):
        self.cursor.execute("SELECT column_name FROM information_schema.columns WHERE TABLE_SCHEMA='products' AND TABLE_NAME='products' ORDER BY ordinal_position")
        columns = self.cursor.fetchall()
        print(columns)
        return [c[0] for c in columns]


    def get_page(self,page):
        amount = 21
        self.cursor.execute("SELECT * FROM products ORDER BY ID LIMIT {} OFFSET {}".format(amount,(page-1)*amount))
        products = self.cursor.fetchall()

        return [product_to_json(p,self.get_column_names()) for p in products]