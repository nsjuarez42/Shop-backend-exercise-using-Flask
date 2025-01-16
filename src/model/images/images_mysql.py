from model.images.images import images
from model.DB.mysqlhelpers import manage_connection,object_to_json,get_column_names

class images_mysql(images):

    def __init__(self,db):
        self.__db = db
        self.__columns = get_column_names("images")

    @property
    def columns(self):
        return self.__columns
    
    @columns.setter
    def columns(self,c):
        self.__columns = c

    @manage_connection    
    def get_by_product(self,product_id):
        self.__db.cursor.execute("SELECT * FROM images WHERE idproduct=%s",(product_id,))
        images = self.__db.cursor.fetchall()
        return [object_to_json(i,self.columns) for i in images]
    
    @manage_connection
    def add(self,img):
        self.__db.cursor.execute("INSERT INTO images(image,idproduct) VALUES(%s,%s)",(img['image'],img['idproduct']))
        self.__db.conn.commit()
        return self.__db.cursor.lastrowid
    

    

    
