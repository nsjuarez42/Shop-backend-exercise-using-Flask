from __main__ import app
from flask import jsonify,request
from model.DB.current import db

@app.route("/categories")
def get_categories():
    return jsonify({"msg":"all categories",'categories':db.categories.get_all()})