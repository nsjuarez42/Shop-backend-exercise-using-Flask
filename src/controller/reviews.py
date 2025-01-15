from __main__ import app
from model.DB.current import db
from flask import jsonify,request
from flask_jwt_extended import jwt_required,get_jwt_identity

REVIEW_COLUMN_NAMES = db.reviews.get_column_names()

@app.route("/reviews/<int:idproduct>")
def get_by_product(idproduct):
    reviews = db.reviews.get_by_product(idproduct)
    return jsonify({"msg":"reviews for product {}".format(idproduct),"reviews":reviews})

@app.route("/reviews/user")
@jwt_required()
def get_by_user(iduser):
    user = get_jwt_identity()
    pass

@app.route("/reviews",methods=["POST"])
@jwt_required()
def add_review():
    data = request.json()
    user = get_jwt_identity()
    pass




