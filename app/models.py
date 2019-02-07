
from . import db


class Association(db.Model):
    __tablename__ = 'association'
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), primary_key=True)
    extra_data = db.Column(db.String(50))
    customer = db.relationship('Customer', back_populates='orders')
    order = db.relationship('Order', back_populates='customers')


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    customers = db.relationship('Association', back_populates='order', lazy='dynamic')


class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    orders = db.relationship('Association', back_populates='customer', lazy='dynamic')

