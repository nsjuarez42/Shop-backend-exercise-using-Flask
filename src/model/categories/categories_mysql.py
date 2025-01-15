from model.categories.categories import categories

def category_to_json(category,columns):
    json = {}
    for i,c in enumerate(columns):
        json[c] = category[i]
    return json

class categories_mysql(categories):

    def __init__(self,conn,cursor):
        self.conn = conn
        self.cursor = cursor

    def get_all(self):
        self.cursor.execute("SELECT * FROM categories")
        categories = self.cursor.fetchall()
        return [category_to_json(c,self.get_column_names()) for c in categories]
    
    def get_by_id(self, id):
        self.cursor.execute("SELECT * FROM categories WHERE ID=%s",(id,))
        category = self.cursor.fetchone()
        return category_to_json(category,self.get_column_names()) if category else None
    
    def get_column_names(self):
        self.cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_schema='products' AND table_name='categories' ORDER BY ordinal_position")
        columns = self.cursor.fetchall()
        return [c[0] for c in columns]
