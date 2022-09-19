from flask import Flask, request, make_response
from flask_sqlalchemy import SQLAlchemy
from datetime import date
import src.server.barcode_lookup as bl

app = Flask(__name__)

# Google Cloud SQL (change this accordingly)
USERNAME = 'barcode'
PASSWORD = 'admin123'
PUBLIC_IP_ADDRESS = '34.88.132.90'
DBNAME = 'products'
PROJECT_ID = 'barcode-362508'
INSTANCE_NAME = 'barcode'
CONNECTION_NAME = 'barcode-362508:europe-north1:barcode'

# configuration
app.config["SECRET_KEY"] = "yoursecretkey"
app.config[
    "SQLALCHEMY_DATABASE_URI"] = f"mysql+mysqldb://root:{PASSWORD}@{PUBLIC_IP_ADDRESS}/{DBNAME}?unix_socket=/cloudsql/{PROJECT_ID}:{INSTANCE_NAME}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)


class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(50), nullable=False)
    barcode_id = db.Column(db.String(50), nullable=False)
    purchase_date = db.Column(db.DateTime(), nullable=False)
    data_source = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)


@app.route('/removeproduct', methods=['DELETE'])
def delete_product():
    product_to_delete = request.json['barcode_id']
    Products.query.filter(Products.barcode_id == product_to_delete).delete()
    db.session.commit()

    response = {
        'status': 'success',
        'message': 'Successfully removed.'
    }

    return make_response(response, 200)


@app.route('/addproduct', methods=['POST'])
def add_product():
    product_to_add = bl.find_product(request.json['barcode_id'])
    print(product_to_add)
    product = Products(
        title=product_to_add['title'],
        price=product_to_add['price'] ,
        barcode_id=product_to_add['barcode_id'],
        purchase_date=date.today(),
        data_source=product_to_add['data_source']
    )
    db.session.add(product)
    db.session.commit()

    response = {
        'status': 'success',
        'message': 'Successfully added.'
    }

    return make_response(response, 200)


@app.route('/products')
def get_products():

    dev = True
    response = list()

    if dev:
        response.append({
            'title': 'title',
            'price': 'price',
            'barcode_id': 'barcode_id',
            'purchase_date': date.today(),
            'data_source': 'data_source'
        })
    else:
        products = Products.query.all()
        for product in products:
            response.append({
                'title': product.title,
                'price': product.price,
                'barcode_id': product.barcode_id,
                'purchase_date': product.purchase_date,
                'data_source': product.data_source
            })

    return make_response({
        'status': 'success',
        'message': response
    }, 200)
