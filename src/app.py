from flask import Flask
from flask_cors import CORS
from dotenv import dotenv_values
from flask_jwt_extended import JWTManager

config = dotenv_values(".env")
app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = config["SECRET"]

jwt = JWTManager(app)
CORS(app)#resources={r"/":{"origins":"*"}})

import controller.images
import controller.products
import controller.users
import controller.tags
import controller.reviews
import controller.categories

#db = DB_factory.create_db("file")

#TODO:
#login
#register

if __name__ == "__main__":
    app.run(debug=True)

