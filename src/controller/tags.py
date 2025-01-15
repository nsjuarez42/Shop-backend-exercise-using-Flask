from __main__ import app
from flask import jsonify
from model.DB.current import db


@app.route("/tags")
def get_tags():
    return jsonify({"msg":"All tags","tags":db.tags.get_all()})

@app.route("/tags/<int:id>")
def get_tags_for_product(id):

    product = db.products.get_by_id(id)

    if not product:
        return jsonify({"error":"product not found"}),404
    
    return jsonify({'msg':"tags for product {}".format(id),'tags':db.tags.get_by_product(id)})
    #check if product exists

