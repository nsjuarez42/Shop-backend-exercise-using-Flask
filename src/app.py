from flask import Flask,jsonify,request
from model.DB_factory import DB_factory
from flask_cors import CORS


db = DB_factory.create_db("mysql")
#db = DB_factory.create_db("file")

if not db.has_data():
    #make request to json api products
    db.fill()

#TODO:
#login
#register

COLUMN_NAMES = db.get_column_names()

app = Flask(__name__)

CORS(app,resources={r"/products":{"origins":"*"}})


@app.before_request
def before_request_func():
    print('Antes de la peticion...')

@app.after_request
def after_request_func(response):
    print("after request")
    return response

@app.route("/products",methods=["GET"])
def get_products():
    return jsonify({"message":"Products list","products":db.get_products()})

@app.route("/products/<string:product_name>",methods=["GET"])
def get_product(product_name):
    product = db.get_product_by_name(product_name)
  
    if product is None:
        return jsonify({"message":"Product not found"}),404
    return jsonify({"message":"Product found","Product":product}),200


@app.route("/products",methods=['POST'])
def add_product():

    column_names = [c for c in COLUMN_NAMES if c != "ID"]
    data = request.json

    if set(column_names) != set(data.keys()):
        return jsonify({"error":"Data format not valid"}),400
    id = db.add_product(data) 

    inserted = db.get_product_by_id(id)

    return jsonify({"message":"Inserted successfully","product":inserted}),200

@app.route("/products/<int:id>",methods=["PUT"])
def edit_product(id):

    new_product = request.json
    if set([c for c in COLUMN_NAMES if c != "ID"]) != set(new_product.keys()):
        return jsonify({"error":"Data format not valid"}),400

    product = db.get_product_by_id(id) 

    if product is None:
        return jsonify({"error":"Product not found"}),404
    
    db.update_product_by_id(id,new_product)

    data = db.get_product_by_id(id) 

    return jsonify({"Message":"Updated successfully","product":data}),200

@app.route("/products/<int:id>",methods=["PATCH"])
def patch_product(id):

    data = request.json
    
    columns_to_change = [i for i in data.keys() if i in COLUMN_NAMES]

    if len(columns_to_change) == 0:
        return jsonify({"Error":"Data format not valid"}),400
    
    product = db.get_product_by_id(id) 

    if product is None:
        return jsonify({"Error":"product not found"}),400
    
    db.update_product_by_id(id,data)

    new_product = db.get_product_by_id(id)

    return jsonify({"message":"Product updated successfully","product":new_product})

@app.route("/products/<int:id>",methods=['DELETE'])
def delete_product(id):

    product = db.get_product_by_id(id)

    if product is None:
        return jsonify({"Error":"Product not found"}),404
    
    db.delete_product_by_id(id)

    return jsonify({"msg":"Deleted successfully","product":product}),200

if __name__ == "__main__":
    app.run(debug=True)

