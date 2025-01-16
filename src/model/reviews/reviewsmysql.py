from model.reviews.reviews import reviews_ABC
from model.DB.mysqlhelpers import get_column_names,manage_connection,object_to_json

class reviews_mysql(reviews_ABC):

    def __init__(self,db):
        self.__db = db
        self.__columns = get_column_names("reviews")

    @property
    def columns(self):
        return self.__columns
    
    @columns.setter
    def columns(self,c):
        self.__columns = c
    
    @manage_connection
    def add(self, review,id_user,id_product):
        self.__db.cursor.execute("INSERT INTO reviews(ID,comment,date,rating,idproduct,iduser) VALUES(NULL,%s,%s,%s,%s)",(review['comment'],review['date'],review['rating'],id_product,id_user))
        self.__db.conn.commit()
        return self.__db.cursor.lastrowid
        
    @manage_connection
    def get_by_product(self, id_product):
        self.__db.cursor.execute("SELECT * FROM reviews WHERE idproduct=%s",(id_product,))
        reviews = self.__db.cursor.fetchall()
        return [object_to_json(r,self.columns) for r in reviews]
        
    @manage_connection
    def get_by_user(self, id_user):
        self.__db.cursor.execute("SELECT * FROM reviews WHERE iduser=%s",(id_user,))
        reviews = self.__db.cursor.fetchall()
        return [object_to_json(r,self.columns) for r in reviews]
        