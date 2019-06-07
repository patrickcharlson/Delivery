import os

from flask import render_template, flash, redirect, url_for
from flask_login import login_required, current_user

from app.auth.forms import SubscribeForm
from app.models import CartItem, Customer, Product
from . import bp
from .forms import EditProfileForm
from .. import db


@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.phone_number = form.phone_number.data
        current_user.news_letter = form.news_letter.data
        current_user.email = form.email.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('Your Profile has been updated', 'form-success')
        return redirect(url_for('main.edit_profile'))
    form.first_name.data = current_user.first_name
    form.last_name.data = current_user.last_name
    form.phone_number.data = current_user.phone_number
    form.news_letter.data = current_user.news_letter
    form.email.data = current_user.email
    return render_template('edit-profile.html', form=form)


@bp.route('/products', methods=['GET', 'POST'])
def products():
    static_folder = os.path.abspath('/home/charlson/PycharmProjects/Pizzeria/app/static/uploads')
    images = os.listdir(static_folder)
    return render_template('products.html', images=images, title='Pizza Hub')


@bp.route('/cart')
def cart():
    s_form = SubscribeForm()
    return render_template('cart.html', s_form=s_form)


@bp.route('/add_to_cart')
def add_to_cart():
    product_id = Product.query.get(id)
    customer = Customer.query.get_or_404(id)
    cart_item = CartItem(product_id=product_id,
                         customer_id=customer)
    db.session.add(cart_item)
    db.session.commit()
    return redirect(url_for('.cart'))
