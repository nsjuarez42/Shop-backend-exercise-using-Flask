from __main__ import app
from flask import jsonify,request
from flask_jwt_extended import jwt_required,get_jwt_identity,create_access_token
from model.DB.current import db
import bcrypt


USERS_COLUMN_NAMES = db.users.columns

@app.route("/register",methods=["POST"])
def register():

    data = request.json

    if set(data.keys()) != set([c for c in USERS_COLUMN_NAMES if c !="ID"]):
        return jsonify({"error":"Data format not valid"}),400
    
    user_by_username = db.users.get_by_username(data["username"])
    user_by_mail = db.users.get_by_mail(data["mail"])
     
    if user_by_username:
        return jsonify({"error":"user already exists"}),400
    
    if user_by_mail:
        return jsonify({"error":"mail already registered"}),400
    
    hashed = bcrypt.hashpw(data['password'].encode(),bcrypt.gensalt())
    data['password'] = hashed.decode()
    id = db.users.add(data)

    return jsonify({"msg":"User registered successfully","user":db.get_user_by_id(id)}),200

@app.route("/login",methods=["POST"])
def login():

    print(request)
    data = request.json
    print(data)


    #login by username for now
    if set(data.keys()) != set(["username","password"]):
        return jsonify({"error":"Data format not valid"}),400
    
    user = db.users.get_by_username(data['username'])

    print(user)
    if not user:
        return jsonify({"error":"User does not exist"}),400
    
    if bcrypt.checkpw(data['password'].encode(),user['password'].encode()):
        return jsonify({"msg":"Logged in successfully","token":create_access_token(identity=user['ID'])})
    else:
        return jsonify({"error":"incorrect credentials"}),401
    
@app.route("/user",methods=["GET"])
@jwt_required()
def get_user():
    print(get_jwt_identity())
    user = get_jwt_identity()
    print(user)
    return jsonify(logged_in_as=user)


#@app.route("/users",methods=["GET"])
#def get_users():
#    print(db.get_users())
#    return jsonify({"message":"all users","users":db.get_users()})
