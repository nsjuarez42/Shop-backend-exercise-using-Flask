from model.users.users import users_ABC

def user_to_json(user,columns):
    json = {}
    for i,c in enumerate(columns):
        json[c] = user[i]
    return json

class users(users_ABC):

    def __init__(self, conn, cursor):
        self.conn = conn
        self.cursor = cursor

    def get_by_id(self, id):
        self.cursor.execute("SELECT * FROM users WHERE id=?",(id,))
        user = self.cursor.fetchone()
        return user_to_json(user,self.get_column_names()) if user else None
    
    def get_by_mail(self, mail):
        self.cursor.execute("SELECT * FROM users WHERE mail=?",(mail,))
        user = self.cursor.fetchone()
        return user_to_json(user,self.get_column_names()) if user else None
    
    def get_by_username(self, username):
        self.cursor.execute("SELECT * FROM users WHERE username=?",(username,)).fetchone()
        user = self.cursor.fetchone()
        return user_to_json(user,self.get_column_names()) if user else None 

    def get_column_names(self):
        self.cursor.execute("SELECT column_name FROM information_schema.columns WHERE TABLE_SCHEMA='products' AND TABLE_NAME='users'")
        columns =self.cursor.fetchall()
        print(columns)
        return [c[0] for c in columns]
    
    def add(self, user):
        self.cursor.execute("INSERT INTO users VALUES (NULL,?,?,?,?)",(user["name"],user["password"],user["username"],user['mail']))
        self.conn.commit()
        return self.cursor.lastrowid

