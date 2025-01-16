from model.DB.mysqlconnection import Connection
#decorator to be used in every function of mysql

def manage_connection(f):
    db = Connection()
    def wrapper(*args,**kwargs):
        result = f(*args,**kwargs)
        db.cursor.close()
        db.cursor = db.conn.cursor()
        return result
    return wrapper

def object_to_json(obj,columns):
    json = {}
    for i,c in enumerate(columns):
        json[c] = obj[i]
    return json

@manage_connection
def get_column_names(table_name):
    db = Connection()
    db.cursor.execute("SELECT column_name FROM information_schema.columns WHERE TABLE_SCHEMA='products' AND TABLE_NAME='{}' ORDER BY ordinal_position".format(table_name))
    columns = db.cursor.fetchall()
    return [c[0] for c in columns]

