from __main__ import app
from flask import jsonify
from model.DB.current import db 

@app.route("/images/<int:idproduct>")
def get_imgs_by_product(idproduct):

    product = db.products.get_by_id(idproduct)

    if not product:
        return jsonify({"error":"product not found"}),404
    
    return jsonify({"msg":"images for product {}".format(idproduct),"images":db.images.get_by_product(idproduct)})

