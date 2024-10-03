# from flask import Flask,render_template,redirect,url_for,request,jsonify
# from flask_pymongo import PyMongo
# from marketapp.market.schemas import ItemSchema,handle_validation_error
# from marshmallow import ValidationError


# app = Flask(__name__)



# app.config['SECRET_KEY']='03954c5efe6bffc2bdc8adf20b79c7d1303586cb'
# app.config['MONGO_URI']="mongodb+srv://ryanthomas2022:jgt0Ov0Utqu2aPAq@cluster0.wdjeluq.mongodb.net/market?retryWrites=true&w=majority&appName=Cluster0"



# client=PyMongo(app)


# db=client.db

# @app.route("/")
# @app.route("/home")
# def home():
#     return render_template("home.html")



# @app.route("/market")

# def market_page():

#     # data=request.json

#     item_schema=ItemSchema()
#     items = [
#     { 'name': 'Phone', 'barcode': '893212299897', 'price': 500},
#     { 'name': 'Laptop', 'barcode': '123985473165', 'price': 900},
#     {'name': 'Keyboard', 'barcode': '231985128446','price':4}
#     ]

#     try:
#         validated_data=item_schema.load(items,many=True)
#     except ValidationError as err:
#         return handle_validation_error(err)
#     market_collection=db.market
#     result=market_collection.insert_many(items).inserted_ids

#     return jsonify({"message":"Author created ","ids":str(result)}),201


#     # return render_template("market.html",items=items)


# if __name__=="__main__":
#     app.run(debug=True)

