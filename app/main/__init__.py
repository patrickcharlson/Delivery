from flask import Blueprint

bp = Blueprint('main', __name__)

from . import views
from ..models import Permission


@bp.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)
