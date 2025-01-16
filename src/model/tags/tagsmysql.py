from model.tags.tags import tags
from model.DB.mysqlhelpers import manage_connection,object_to_json,get_column_names

class tags_mysql(tags):

    def __init__(self,db):
        self.__db = db
        self.__columns = get_column_names("tags")

    @property
    def columns(self):
        return self.__columns
    
    @columns.setter
    def columns(self,c):
        self.__columns = c

    @manage_connection
    def get_all(self):
        self.__db.cursor.execute("SELECT * FROM tags")
        tags = self.__db.cursor.fetchall()
        return [object_to_json(tag,self.columns) for tag in tags]
    
    @manage_connection    
    def get_by_product(self,id):
        #all tags in a product
        self.__db.cursor.execute("SELECT t.* FROM tags as t INNER JOIN tagproduct as tp ON t.ID = tp.idtag INNER JOIN products as p ON p.ID = tp.idproduct WHERE p.ID =%s",(id,))
        tags = self.__db.cursor.fetchall()
        return [object_to_json(t,self.columns) for t in tags] 

