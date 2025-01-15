from model.tags.tags import tags

def tag_to_json(tag,columns):
    json = {}
    for i,c in enumerate(columns):
        json[c] = tag[i]
    return json

class tags_mysql(tags):

    def __init__(self,conn,cursor):
        self.conn = conn 
        self.cursor = cursor

    def get_all(self):
        self.cursor.execute("SELECT * FROM tags")
        tags = self.cursor.fetchall()
        return [tag_to_json(tag,self.get_column_names()) for tag in tags]
        
    def get_by_product(self,id):
        #all tags in a product
        self.cursor.execute("SELECT t.* FROM tags as t INNER JOIN tagproduct as tp ON t.ID = tp.idtag INNER JOIN products as p ON p.ID = tp.idproduct WHERE p.ID =%s",(id,))
        tags = self.cursor.fetchall()
        return [tag_to_json(t,self.get_column_names()) for t in tags] 

    def get_column_names(self):
        self.cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_schema='products' AND table_name='tags'")
        columns = self.cursor.fetchall()
        return [c[0] for c in columns] 
