import os

from flask import render_template

from app.auth.forms import SubscribeForm
from . import pizzeria


@pizzeria.route('/products', methods=['GET', 'POST'])
def products():
    static_folder = os.path.abspath('/home/charlson/PycharmProjects/Pizzeria/app/static/uploads')
    images = os.listdir(static_folder)
    return render_template('pizzeria/products.html', images=images, title='Pizza Hub')


@pizzeria.route('/cart')
def cart():
    s_form = SubscribeForm()
    return render_template('pizzeria/cart.html', s_form=s_form)
