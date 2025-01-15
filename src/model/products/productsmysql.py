from model.products.products import products_ABC
from math import trunc

def product_to_json(product,columns):
    json = {}
    print(product)
    for i,c in enumerate(columns):
        json[c] = product[i]
    return json

products_per_page = 21

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
        return product_to_json(product,self.get_column_names()) if product else None
    
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
        return [c[0] for c in columns]


    def get_page(self,page):
        self.cursor.execute("SELECT * FROM products ORDER BY ID LIMIT {} OFFSET {}".format(products_per_page,(page-1)*products_per_page))
        products = self.cursor.fetchall()

        return [product_to_json(p,self.get_column_names()) for p in products]
    
    def get_pages(self):
        self.cursor.execute("SELECT COUNT(*) / {} FROM products".format(products_per_page))
        columns = self.cursor.fetchone()[0]
        return int(columns) +1 if int(columns) < columns else int(columns)
    
    def filter_products(self, filters):
        self.cursor.execute("""SELECT p.*,t.name FROM products as p
        INNER JOIN categories as c ON c.ID = p.idcategory
        INNER JOIN tagproduct as tp ON tp.idproduct = p.ID
        INNER JOIN tags as t ON tp.idtag = t.ID
        WHERE c.name=%s;""",(filters['category'],))
        filtered_by_category = self.cursor.fetchall()
        products = [product_to_json(p,self.get_column_names()+['tag']) for p in filtered_by_category]
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