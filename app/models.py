from flask import current_app
from flask_login import UserMixin, AnonymousUserMixin, current_user
from itsdangerous import BadSignature, SignatureExpired
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash

from . import db
from . import login_manager


class CartItem(db.Model):
    __tablename__ = 'cartItems'
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), primary_key=True)
    quantity = db.Column(db.Integer)
    product = db.relationship('product')

    @staticmethod
    def get_total_price(cart_items=None):
        if cart_items is None:
            cart_items = current_user.cart_items
        prices = [item.product.price * item.quantity for item in cart_items]
        return sum(prices)

    @staticmethod
    def delete_cart_items(cart_items):
        for item in cart_items:
            db.session.delete(item)


class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    description = db.Column(db.Text)
    price = db.Column(db.Float)
    quantity = db.Column(db.String(1000))
    unit = db.Column(db.String(1000))
    updated = db.Column(db.Integer, default=0)
    available = db.Column(db.Boolean, default=True)
    cart_items = db.relationship('CartItem', backref='products', lazy='dynamic')

    def __init__(self, name, unit, price, available, product_id, description="", quantity=0):
        self.name = name
        self.price = price
        self.unit = unit
        self.description = description
        self.product_id = product_id
        self.quantity = quantity
        self.available = available

    def remove_from_carts(self):
        cart_items = CartItem.query.filter_by(product_id=self.id).all()
        for item in cart_items:
            db.session.delete(item)
        db.session.commit()

    def get_quantity_in_cart(self):
        cart_item = CartItem.query.filter_by(customer_id=current_user.id, product_id=self.id).first()
        if cart_item:
            return cart_item.quantity
        else:
            return 0

    def disable_product(self):
        self.available = False
        self.remove_from_carts()
        db.session.commit()

    def delete_product(self):
        self.remove_from_carts()
        db.session.delete(self)
        db.session.commit()


class Customer(UserMixin, db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    first_name = db.Column(db.String(64), index=True)
    last_name = db.Column(db.String(64), index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    phone_number = db.Column(db.String(64), unique=True)
    news_letter = db.Column(db.Boolean, default=False)
    cart_items = db.relationship('CartItem', backref='customers', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id})

    def generate_change_email_token(self, new_email, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'change_email': self.id, 'new_email': new_email})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except(BadSignature, SignatureExpired):
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def reset_password(self, token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except(BadSignature, SignatureExpired):
            return False
        if data.get('reset') != self.id:
            return False
        self.password = new_password
        db.session.add(self)
        return True

    def change_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except(BadSignature, SignatureExpired):
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        db.session.add(self)
        return True


class AnonymousCustomer(AnonymousUserMixin):
    def can(self, _):
        return False

    def is_admin(self):
        return False


login_manager.anonymous_user = AnonymousCustomer


@login_manager.user_loader
def load_user(customer_id):
    return Customer.query.get(int(customer_id))
