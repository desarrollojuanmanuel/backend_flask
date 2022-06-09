from app import db

class Product(db.Model):
    product_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(191), nullable=False)
    product_description = db.Column(db.String(191), nullable=False)
    price = db.Column(db.Float, nullable=False)
    
    def __str__(self):
        return f'id: {self.product_id}, name: {self.name}'

class Customer(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(191), nullable=False)
    email = db.Column(db.String(191), nullable=False)
    
    def __str__(self):
        return f'id: {self.customer_id}, name: {self.name}'

class CustomerProduct(db.Model):
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'),primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'),primary_key=True)

class Order(db.Model):
    order_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'))
    creation_date = db.Column(db.Date,nullable=False)
    delevery_address = db.Column(db.String(191), nullable=False)
    total = db.Column(db.Float, nullable=False)
    
    def __init__(self,customer_id, creation_date,delevery_address,total):
        self.customer_id = customer_id
        self.creation_date = creation_date
        self.delevery_address = delevery_address
        self.total = total

class OrderDetail(db.Model):
    order_detail_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.order_id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'))
    product_description = db.Column(db.String(191), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    
    def __init__(self,order_id, product_id,product_description,price,quantity):
        self.order_id = order_id
        self.product_id = product_id
        self.product_description = product_description
        self.price = price
        self.quantity = quantity
