from model.DB.DB_factory import DB_factory

#change this string to change db
current_db = "mysql"
db = DB_factory.create_db("mysql")