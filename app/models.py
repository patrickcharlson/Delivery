from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from . import db
from . import login_manager


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


class Customer(UserMixin, db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    first_name = db.Column(db.String(64), index=True)
    last_name = db.Column(db.String(64), index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    orders = db.relationship('Association', back_populates='customer', lazy='dynamic')
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(customer_id):
    return Customer.query.get(int(customer_id))
