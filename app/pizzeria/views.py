import os

from flask import render_template

from app.auth.forms import SubscribeForm
from . import pizzeria


# UPLOAD_FOLDER = 'static/uploads'
# ALLOWED_EXTENSIONS = {'jpeg', 'jpg', 'png', 'gif'}
# current_app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@pizzeria.route('/products')
def products():
    static_folder = os.path.abspath('../Pizzeria/app/static/')
    images = os.listdir(os.path.join(static_folder, 'uploads'))
    return render_template('pizzeria/products.html', images=images, title='Pizza Hub')


@pizzeria.route('/cart')
def cart():
    s_form = SubscribeForm()
    return render_template('pizzeria/cart.html', s_form=s_form)

# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
#
#
# @pizzeria.route('/add_item', methods=['GET', 'POST'])
# def add_item():
#     if request.method == 'POST':
#         name = request.form['name']
#         price = float(request.form['price'])
#         description = request.form['description']
#
#         image = request.files['image']
#         if image and allowed_file(image.filename):
#             filename = secure_filename(image.filename)
#             image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
#         imagename = filename
