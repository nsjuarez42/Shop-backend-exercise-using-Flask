from model.images.images import images

class images_mysql(images):

    def __init__(self,conn,cursor):
        self.conn = conn
        self.cursor = cursor
        self.columns = []

    @property
    def columns(self):
        if len(self.__columns) == 0:
            self.cursor.execute("SELECT column_name FROM information_schema.columns WHERE TABLE_SCHEMA='products' AND TABLE_NAME='images' ORDER BY ordinal_position")
            columns = self.cursor.fetchall()
            self.columns = [c[0] for c in columns]
        return self.__columns
    
    @columns.setter
    def columns(self,c):
        self.__columns = c


    
    def image_to_json(self,img):
        json = {}
        for i,c in enumerate(self.columns):
            json[c] = img[i]
        return json
    
    def get_by_product(self,product_id):
        self.cursor.execute("SELECT * FROM images WHERE idproduct=%s",(product_id,))
        images = self.cursor.fetchall()
        return [self.image_to_json(i) for i in images]
    
    def add(self,img):
        self.cursor.execute("INSERT INTO images(image,idproduct) VALUES(%s,%s)",(img['image'],img['idproduct']))
        return self.cursor.lastrowid
    

    

    
