from model.users.users import users_ABC
from model.DB.mysqlhelpers import manage_connection,get_column_names,object_to_json

class users(users_ABC):

    def __init__(self, db):
        self.__db = db
        self.__columns = get_column_names("users")

    @property
    def columns(self):
        return self.__columns
    
    @columns.setter
    def columns(self,c):
        self.__columns = c

    @manage_connection
    def get_by_id(self, id):
        self.__db.cursor.execute("SELECT * FROM users WHERE id=?",(id,))
        user = self.__db.cursor.fetchone()
        return object_to_json(user,self.columns) if user else None
    
    @manage_connection
    def get_by_mail(self, mail):
        self.__db.cursor.execute("SELECT * FROM users WHERE mail=?",(mail,))
        user = self.__db.cursor.fetchone()
        return object_to_json(user,self.columns) if user else None
    
    @manage_connection
    def get_by_username(self, username):
        self.__db.cursor.execute("SELECT * FROM users WHERE username=?",(username,)).fetchone()
        user = self.__db.cursor.fetchone()
        return object_to_json(user,self.columns) if user else None 

    @manage_connection
    def add(self, user):
        self.__db.cursor.execute("INSERT INTO users VALUES (NULL,?,?,?,?)",(user["name"],user["password"],user["username"],user['mail']))
        self.__db.conn.commit()
        return self.__db.cursor.lastrowid

