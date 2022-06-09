from flask import Flask,request,jsonify,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import create_engine, insert
from configdb import *
from models import *
from ClassAllData import ClassAllData
from ClassCreateOrder import ClassCreateOrder
from ClassListOrder import ClassListOrder

# INICO DE LA PLICACION
app = Flask(__name__)
v = 1 #version
api = f'/api_beitech/v{v}' # API URL VERSION

# VARIABLES DE CONFIGURACION
app.config['SQLALCHEMY_DATABASE_URI'] = FULL_URL_DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate()
migrate.init_app(app, db)

# METODO GET all_customers
@app.route(f"{api}/all_customers")
def all_customers():
    return jsonify(all_data('customer',Customer.query.all()))

# METODO GET all_product
@app.route(f"{api}/all_product")
def all_product():
    return jsonify(all_data('product',Product.query.all()))

# METODO GET all_customer_product
@app.route(f"{api}/all_customer_product")
def all_customer_product():
    cp = CustomerProduct.query.all()
    d = []
    b = {}
    for c in cp:
        customer = Customer.query.get(c.customer_id)
        product = Product.query.get(c.product_id)
        b = {
            'product_id':product.name,
            'customer':customer.name, 
        }
        d.append(b)

    return jsonify(d)

# METODO POST create_order
@app.route(f"{api}/create_order", methods=['POST'])
def create_order():
    order = get_request_json()
    new_order = ClassCreateOrder(order, FULL_URL_DB)
    new_order.load_process
    return  new_order.getResponse

# METODO POST list_order
@app.route(f"{api}/list_order", methods=['POST'])
def list_order():
    data = get_request_json()
    lo = ClassListOrder(data, FULL_URL_DB)
    return jsonify(lo.getResponse)


# METODO all_data
def all_data(type, query):
    cl = ClassAllData(type)
    cl.setData = query
    cl.load_process
    return cl.resolved

# METODO get_request_json
def get_request_json():
    return request.get_json()

    
def sql_query(query):
    engine = create_engine(FULL_URL_DB)

    with engine.connect() as conn:
        result = conn.execute(query)
        return result.fetchall()

