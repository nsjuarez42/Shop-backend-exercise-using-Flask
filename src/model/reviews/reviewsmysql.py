from model.reviews.reviews import reviews_ABC

def review_to_json(review,columns):
    json = {}
    for i,c in enumerate(columns):
        json[c] = review[i]
    return json

class reviews_mysql(reviews_ABC):

    def __init__(self, conn, cursor):
        self.conn = conn
        self.cursor = cursor

    def get_column_names(self):
        self.cursor.execute("SELECT column_name FROM information_schema.columns WHERE TABLE_SCHEMA='products' AND TABLE_NAME='reviews' ORDER BY ordinal_position")
        columns = self.cursor.fetchall()
        return [c[0] for c in columns]
    
    def add(self, review,id_user,id_product):
        self.cursor.execute("INSERT INTO reviews(ID,comment,date,rating,idproduct,iduser) VALUES(NULL,%s,%s,%s,%s)",(review['comment'],review['date'],review['rating'],id_product,id_user))
        self.conn.commit()
        return self.cursor.lastrowid

    def get_by_product(self, id_product):
        self.cursor.execute("SELECT * FROM reviews WHERE idproduct=%s",(id_product,))
        reviews = self.cursor.fetchall()
        return [review_to_json(r,self.get_column_names()) for r in reviews]
    
    def get_by_user(self, id_user):
        self.cursor.execute("SELECT * FROM reviews WHERE iduser=%s",(id_user,))
        reviews = self.cursor.fetchall()
        return [review_to_json(r,self.get_column_names()) for r in reviews]
        