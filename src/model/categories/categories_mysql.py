from model.categories.categories import categories
from model.DB.mysqlhelpers import object_to_json,manage_connection,get_column_names

class categories_mysql(categories):

    def __init__(self,db):
        self.__db = db
        self.__columns = get_column_names("categories") 

    @property
    def columns(self):
        return self.__columns
    
    @columns.setter
    def columns(self,c):
        self.__columns = c

    @manage_connection
    def get_all(self):
        self.__db.cursor.execute("SELECT * FROM categories")
        categories = self.__db.cursor.fetchall()
        return [object_to_json(c,self.columns) for c in categories]
    
    @manage_connection
    def get_by_id(self, id):
        self.cursor.execute("SELECT * FROM categories WHERE ID=%s",(id,))
        category = self.cursor.fetchone()
        return object_to_json(category,self.columns) if category else None
