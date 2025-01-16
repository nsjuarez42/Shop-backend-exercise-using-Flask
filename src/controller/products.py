from __main__ import app
from model.DB.current import db
from flask import jsonify,request

PRODUCT_COLUMN_NAMES = db.products.columns

@app.route("/products",methods=["GET"])
def get_products():
    return jsonify({"message":"Products list","products":db.products.get_all()})

@app.route("/products/filter",methods=["POST"])
def filtered_products():
    data = request.json

    if 'tags' not in data.keys() and 'category' not in data.keys():
        return jsonify({"error":"data format not valid"}),400

    return jsonify({"msg":"filtered products by {} and {}".format(", ".join(data['tags']),data['category']),"products":db.products.filter_products(data)})


@app.route("/products/<int:id>",methods=["GET"])
def get_product(id):

    product = db.products.get_by_id(id)

    if product is None:
        return jsonify({"message":"Product not found"}),404
    return jsonify({"message":"Product found","product":product}),200



@app.route("/products",methods=['POST'])
def add_product():

    column_names = [c for c in PRODUCT_COLUMN_NAMES if c != "ID"]
    data = request.json

    if set(column_names) != set(data.keys()):
        return jsonify({"error":"Data format not valid"}),400
    id = db.products.add(data) 

    inserted = db.products.get_by_id(id)

    return jsonify({"message":"Inserted successfully","product":inserted}),200

@app.route("/products/<int:id>",methods=["PUT"])
def edit_product(id):

    new_product = request.json

    if set([c for c in PRODUCT_COLUMN_NAMES if c != "ID"]) != set(new_product.keys()):
        return jsonify({"error":"Data format not valid"}),400

    product = db.products.get_by_id(id) 

    if product is None:
        return jsonify({"error":"Product not found"}),404
    
    db.products.update_by_id(id,new_product)

    data = db.products.get_by_id(id) 

    return jsonify({"Message":"Updated successfully","product":data}),200

@app.route("/products/<int:id>",methods=["PATCH"])
def patch_product(id):

    data = request.json
    
    columns_to_change = [i for i in data.keys() if i in PRODUCT_COLUMN_NAMES]

    if len(columns_to_change) == 0:
        return jsonify({"Error":"Data format not valid"}),400
    
    product = db.products.get_by_id(id) 

    if product is None:
        return jsonify({"Error":"product not found"}),400
    
    db.products.update_by_id(id,data)

    new_product = db.products.get_by_id(id)

    return jsonify({"message":"Product updated successfully","product":new_product})

@app.route("/products/<int:id>",methods=['DELETE'])
def delete_product(id):

    product = db.products.get_by_id(id)

    if product is None:
        return jsonify({"Error":"Product not found"}),404
    
    db.products.delete_by_id(id)

    return jsonify({"msg":"Deleted successfully","product":product}),200

@app.route("/products/page/<int:page>")
def get_products_page(page):
    return jsonify({"msg":"Products for page {}".format(page),"products":db.products.get_page(page),'pagesAmount':db.products.get_pages()})