from flask import Blueprint

pizzeria = Blueprint('pizzeria', __name__)

from . import views
